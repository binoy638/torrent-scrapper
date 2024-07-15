package main

import (
	"fmt"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/gocolly/colly"
	"github.com/gocolly/colly/debug"
)

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

	return magnetUrl
}

func ExtractTorrentFiles(row *goquery.Selection) []string {
	var files []string
	cells := row.Find("td")
	if cells.Length() > 0 {
		filesDiv := cells.Eq(1).Find("#files").Find("ul").Find("li")

		filesDiv.Each(func(i int, fileRow *goquery.Selection) {
			file := fileRow.Text()
			files = append(files, file)
			fmt.Printf("File found: %s", file)
		})
	}

	return files
}

func main() {
	c := colly.NewCollector(colly.Debugger(&debug.LogDebugger{}))
	var magnetUrl string
	// tableFound := false
	c.OnHTML("table.lista", func(e *colly.HTMLElement) {
		if magnetUrl != "" {
			return
		}
		// if tableFound {
		// 	return
		// }
		// tableFound = true
		rows := e.DOM.Find("tr")

		if rows.Length() == 0 {
			fmt.Println("no rows found in the table")
			return
		}
		fileRow := rows.Eq(10)

		files := ExtractTorrentFiles(fileRow)

		fmt.Println(files)

		// filesRowCells := fileRow.Find("td")

		// if filesRowCells.Length() > 0 {
		// 	filesDiv := filesRowCells.Eq(1).Find("#files").Find("ul")

		// 	// filesDiv.Each(func(i int, fileRow *goquery.Selection){
		// 	// 	file :=
		// 	// })

		// 	fmt.Println(secondCell)

		// }

		magnetLinkRow := rows.Eq(0)
		magnetLinkRowCells := magnetLinkRow.Find("td")

		if magnetLinkRowCells.Length() > 0 {
			firstCellText := magnetLinkRowCells.Eq(0).Text()
			println(firstCellText)
			if firstCellText != "Torrent:" {
				return
			}
			secondCell := magnetLinkRowCells.Eq(1)
			var exists bool
			magnetUrl, exists = secondCell.Find("a").Attr("href")
			fmt.Println(exists)

			if !exists {
				fmt.Println("magnet link not found")

			}
		} else {
			fmt.Println("no rows found in the table")
		}
		fmt.Println(magnetUrl)

	})

	c.Visit("https://rargb.to/torrent/lego-marvel-super-heroes-avengers-reassembled-2015-1080p-nf-webrip-dd-5-1-x265-edge2020-6106583.html")

}
