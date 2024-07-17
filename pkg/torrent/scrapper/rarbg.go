package scraper

import (
	"fmt"
	"log"
	"net/http"
	"strings"
	"sync"
	"time"

	t "github.com/binoy638/torrent-scrapper/pkg/torrent"

	"github.com/binoy638/torrent-scrapper/utils"

	"github.com/PuerkitoBio/goquery"
	"github.com/gocolly/colly"
	"github.com/gocolly/colly/debug"
)

type AdditionalTorrentInfo struct {
	Magnet string   `json:"magnet"`
	Files  []string `json:"files"`
}

func ExtractTorrentMagnetUrl(row *goquery.Selection) string {
	magnetUrl := ""
	cells := row.Find("td")

	if cells.Length() > 0 {
		url, exists := cells.Eq(1).Find("a").Attr("href")
		if !exists {
			fmt.Printf("magnet link not found in second cell")
			return magnetUrl
		}

		if !strings.HasPrefix(url, "magnet:") {
			fmt.Printf("url found is not a magnet link: %s", url)
			return magnetUrl
		}
		magnetUrl = url

	}
	fmt.Println(magnetUrl)
	return utils.TrimWhiteSpace(magnetUrl)
}

func ExtractTorrentFiles(row *goquery.Selection, files *[]string) {
	cells := row.Find("td")
	if cells.Length() > 0 {
		filesDiv := cells.Eq(1).Find("#files").Find("ul").Find("li")

		filesDiv.Each(func(i int, fileRow *goquery.Selection) {
			file := fileRow.Text()

			*files = append(*files, strings.Replace(utils.TrimWhiteSpace(file), "[email protected]", " ", -1))
			fmt.Printf("File found: %s", file)
		})
	}

}

func getAdditionalInfo(url string) (AdditionalTorrentInfo, error) {
	c := colly.NewCollector(colly.Debugger(&debug.LogDebugger{}))
	var magnet string
	var files []string

	var err error
	done := make(chan bool)

	c.OnHTML("table.lista", func(e *colly.HTMLElement) {

		// need this statement coz sometime this block gets executed multiple times if more than one table is found
		if magnet != "" {
			return
		}

		rows := e.DOM.Find("tr")
		if rows.Length() == 0 {
			err = fmt.Errorf("no rows found in the table")
			done <- true
			return
		}
		rows.Each(func(_ int, row *goquery.Selection) {
			// the first cell of each row have the title
			title := row.Find("td").Eq(0).Text()

			if strings.Contains(strings.ToLower(title), strings.ToLower("torrent")) {
				magnet = ExtractTorrentMagnetUrl(row)
			}

			if strings.Contains(strings.ToLower(title), strings.ToLower("files")) {
				ExtractTorrentFiles(row, &files)
			}

		})
		done <- true
	})

	handleCollectorError(c, done, &err)

	go func() {
		_err := c.Visit(url)
		if _err != nil {
			err = _err
		}
		done <- true
	}()

	<-done

	return AdditionalTorrentInfo{
		Magnet: magnet,
		Files:  files,
	}, err
}

func handleCollectorError(c *colly.Collector, done chan bool, errPtr *error) {
	maxRetries := 10
	retryCount := 0

	c.OnError(func(r *colly.Response, err error) {
		fmt.Printf("Request URL: %s failed with response: %v\nError: %v\n", r.Request.URL, r, err)
		if r.StatusCode == http.StatusInternalServerError || r.StatusCode == http.StatusBadGateway || r.StatusCode == 0 {
			if retryCount < maxRetries {
				retryCount++
				time.Sleep(2 * time.Second)
				fmt.Printf("Retrying (%d/%d)...\n", retryCount, maxRetries)
				r.Request.Retry()
			} else {
				fmt.Println("Maximum retries exceeded")
				*errPtr = err
				done <- true
			}
		} else {
			*errPtr = err
			done <- true
		}
	})
}

func extractTorrentInfo(row *goquery.Selection, e *colly.HTMLElement, wg *sync.WaitGroup, mu *sync.Mutex, torrents *[]t.Torrent) {
	defer wg.Done()

	cells := row.Find("td")
	if cells.Length() == 0 {
		log.Println("No cells found in row")
		return
	}

	nameCell := cells.Eq(1)
	name := nameCell.Find("a").Text()
	href, exists := nameCell.Find("a").Attr("href")
	var absoluteURL string
	if exists {
		absoluteURL = e.Request.AbsoluteURL(href)
	} else {
		absoluteURL = ""
	}

	added, err := utils.FormatDate(utils.TrimWhiteSpace(cells.Eq(3).Text()))
	if err != nil {
		added = 0
	}

	size, err := utils.ParseSizeString(utils.TrimWhiteSpace(cells.Eq(4).Text()))
	if err != nil {
		size = 0
	}

	additionalInfo, err := getAdditionalInfo(absoluteURL)
	if err != nil {
		log.Printf("Failed to get magnet link: %v url: %s", err, absoluteURL)
	}

	torrent := t.Torrent{
		Name:     utils.TrimWhiteSpace(name),
		Added:    added,
		Size:     size,
		Seeds:    utils.ParseInt(cells.Eq(5).Text()),
		Leeches:  utils.ParseInt(cells.Eq(6).Text()),
		Uploader: utils.TrimWhiteSpace(cells.Eq(7).Text()),
		Magnet:   additionalInfo.Magnet,
		Files:    additionalInfo.Files,
		Provider: "Rarbg",
		Link:     absoluteURL,
	}

	mu.Lock()
	*torrents = append(*torrents, torrent)
	mu.Unlock()

	// fmt.Println("Added torrent:", torrent.Name)
}

func ScrapeRarbg(url string) ([]t.Torrent, error) {
	c := colly.NewCollector(colly.Debugger(&debug.LogDebugger{}))

	var torrents []t.Torrent
	var mu sync.Mutex
	var wg sync.WaitGroup

	c.OnHTML("table.lista2t", func(e *colly.HTMLElement) {
		rows := e.DOM.Find("tr")
		rows.Slice(1, rows.Length()).Each(func(i int, row *goquery.Selection) {
			wg.Add(1)
			go extractTorrentInfo(row, e, &wg, &mu, &torrents)
		})
	})

	handleCollectorError(c, make(chan bool), new(error))

	err := c.Visit(BuildCompleteUrl("rarbg", "demon slayer", "seeders", "asc", "1", false))
	if err != nil {
		log.Fatalf("Failed to start visit: %v", err)
		return torrents, err
	}

	wg.Wait()

	return torrents, nil
}
