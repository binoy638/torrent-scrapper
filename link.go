// package main

// import (
// 	"fmt"
// 	"strings"

// 	"github.com/PuerkitoBio/goquery"
// 	"github.com/gocolly/colly"
// 	"github.com/gocolly/colly/debug"
// )

// func ExtractTorrentMagnetUrl(row *goquery.Selection) string {
// 	magnetUrl := ""
// 	cells := row.Find("td")

// 	if cells.Length() > 0 {
// 		url, exists := cells.Eq(1).Find("a").Attr("href")
// 		if !exists {
// 			fmt.Printf("magnet link not found in second cell")
// 			return magnetUrl
// 		}

// 		if !strings.HasPrefix(url, "magnet:") {
// 			fmt.Printf("url found is not a magnet link: %s", url)
// 			return magnetUrl
// 		}
// 		magnetUrl = url

// 	}

// 	return magnetUrl
// }

// func ExtractTorrentFiles(row *goquery.Selection, files *[]string) {
// 	cells := row.Find("td")
// 	if cells.Length() > 0 {
// 		filesDiv := cells.Eq(1).Find("#files").Find("ul").Find("li")

// 		filesDiv.Each(func(i int, fileRow *goquery.Selection) {
// 			file := fileRow.Text()
// 			*files = append(*files, file)
// 			fmt.Printf("File found: %s", file)
// 		})
// 	}

// }

// func main() {
// 	c := colly.NewCollector(colly.Debugger(&debug.LogDebugger{}))
// 	var magnetUrl string
// 	var files []string
// 	// tableFound := false
// 	c.OnHTML("table.lista", func(e *colly.HTMLElement) {
// 		if magnetUrl != "" {
// 			return
// 		}
// 		// if tableFound {
// 		// 	return
// 		// }
// 		// tableFound = true
// 		rows := e.DOM.Find("tr")

// 		if rows.Length() == 0 {
// 			fmt.Println("no rows found in the table")
// 			return
// 		}

// 		rows.Each(func(_ int, row *goquery.Selection) {
// 			// the first cell of each row have the title
// 			title := row.Find("td").Eq(0).Text()

// 			if strings.Contains(strings.ToLower(title), strings.ToLower("torrent")) {
// 				magnetUrl = ExtractTorrentMagnetUrl(row)
// 			}

// 			if strings.Contains(strings.ToLower(title), strings.ToLower("files")) {
// 				ExtractTorrentFiles(row, &files)
// 			}

// 		})

// 	})

// 	c.Visit("https://rargb.to/torrent/lego-marvel-super-heroes-avengers-reassembled-2015-1080p-nf-webrip-dd-5-1-x265-edge2020-6106583.html")

// }
