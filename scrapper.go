package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/PuerkitoBio/goquery"
	"github.com/gocolly/colly"
	"github.com/gocolly/colly/debug"
)

type Torrent struct {
	Name     string   `json:"name"`
	Seeds    int      `json:"seeds"`
	Leeches  int      `json:"leeches"`
	Size     int64    `json:"size"`
	Added    int64    `json:"added"`
	Uploader string   `json:"uploader"`
	Magnet   string   `json:"magnet"`
	Files    []string `json:"files"`
	Provider string   `json:"provider"`
}

type AdditionalTorrentInfo struct {
	Magnet string   `json:"magnet"`
	Files  []string `json:"files"`
}

func parseSizeString(sizeStr string) (int64, error) {
	sizeStr = strings.ToLower(sizeStr)
	parts := strings.Fields(sizeStr)
	if len(parts) != 2 {
		return 0, fmt.Errorf("invalid size string format: %s", sizeStr)
	}

	size, err := strconv.ParseFloat(parts[0], 64)
	if err != nil {
		return 0, fmt.Errorf("failed to parse size: %v", err)
	}

	unit := parts[1]
	var multiplier int64

	switch unit {
	case "gb":
		multiplier = 1024 * 1024 * 1024
	case "mb":
		multiplier = 1024 * 1024
	case "kb":
		multiplier = 1024
	default:
		return 0, fmt.Errorf("unsupported size unit: %s", unit)
	}

	bytes := int64(size * float64(multiplier))
	return bytes, nil
}

func parseInt(intStr string) int {
	intStr = strings.TrimSpace(intStr)
	intValue, err := strconv.Atoi(intStr)
	if err != nil {
		log.Printf("Unable to parse integer value: %s", intStr)
		return 0
	}
	return intValue
}

func formatDate(dateStr string) (int64, error) {
	layout := "2006-01-02 15:04:05"
	dateTime, err := time.Parse(layout, dateStr)
	if err != nil {
		return 0, err
	}
	return dateTime.Unix(), nil
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
	return trimWhiteSpace(magnetUrl)
}

func ExtractTorrentFiles(row *goquery.Selection, files *[]string) {
	cells := row.Find("td")
	if cells.Length() > 0 {
		filesDiv := cells.Eq(1).Find("#files").Find("ul").Find("li")

		filesDiv.Each(func(i int, fileRow *goquery.Selection) {
			file := fileRow.Text()
			*files = append(*files, trimWhiteSpace(file))
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

func extractTorrentInfo(row *goquery.Selection, e *colly.HTMLElement, wg *sync.WaitGroup, mu *sync.Mutex, torrents *[]Torrent) {
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

	added, err := formatDate(trimWhiteSpace(cells.Eq(3).Text()))
	if err != nil {
		added = 0
	}

	size, err := parseSizeString(trimWhiteSpace(cells.Eq(4).Text()))
	if err != nil {
		size = 0
	}

	additionalInfo, err := getAdditionalInfo(absoluteURL)
	if err != nil {
		log.Printf("Failed to get magnet link: %v url: %s", err, absoluteURL)
	}

	torrent := Torrent{
		Name:     trimWhiteSpace(name),
		Added:    added,
		Size:     size,
		Seeds:    parseInt(cells.Eq(5).Text()),
		Leeches:  parseInt(cells.Eq(6).Text()),
		Uploader: trimWhiteSpace(cells.Eq(7).Text()),
		Magnet:   additionalInfo.Magnet,
		Files:    additionalInfo.Files,
		Provider: "Rarbg",
	}

	mu.Lock()
	*torrents = append(*torrents, torrent)
	mu.Unlock()

	// fmt.Println("Added torrent:", torrent.Name)
}

const (
	RARBG_URL  = "https://rargb.to"
	I1337X_URL = "https://1337xx.to"
	TPB_URL    = "https://apibay.org/q.php"
	NYAA_URL   = "https://nyaa.si/?f=0&c=0_0"
)

func BuildCompleteUrl(site string, q string, sort_by string, sort_type string, page string, nsfw bool) string {
	var url string
	switch site {
	case "rarbg":
		url = RARBG_URL + "/search/" + page + "/?search=" + q + "&category[]=movies&category[]=tv&category[]=games&category[]=music&category[]=anime&category[]=apps&category[]=documentaries&category[]=other"

		if nsfw {
			url = RARBG_URL + "/search/" + page + "/?search=" + q
		}

		if sort_by != "" && sort_type != "" {
			if sort_by == "time" {
				sort_by = "data"
			}
			url = url + "&order=" + sort_by + "&by=" + sort_type
		}
	}
	fmt.Println(url)
	return url
}

func main() {
	c := colly.NewCollector(colly.Debugger(&debug.LogDebugger{}))

	startTime := time.Now()

	var torrents []Torrent
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

	err := c.Visit(BuildCompleteUrl("rarbg", "avengers", "", "", "1", false))
	if err != nil {
		log.Fatalf("Failed to start visit: %v", err)
	}

	wg.Wait()

	if err := writeTorrentsToFile("torrents.json", torrents); err != nil {
		log.Fatalf("Failed to write torrents to file: %v", err)
	}

	fmt.Printf("Torrents data has been written to torrents.json in %v", time.Since(startTime))
}

func writeTorrentsToFile(filename string, torrents []Torrent) error {
	file, err := os.Create(filename)
	if err != nil {
		return fmt.Errorf("failed to create file: %v", err)
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetEscapeHTML(false)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(torrents); err != nil {
		return fmt.Errorf("failed to encode torrents to JSON: %v", err)
	}

	return nil
}

func trimWhiteSpace(str string) string {
	return strings.TrimSpace(str)
}
