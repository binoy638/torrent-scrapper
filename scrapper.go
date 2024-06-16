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
	Name     string `json:"name"`
	Seeds    int    `json:"seeds"`
	Leeches  int    `json:"leeches"`
	Size     int64  `json:"size"`
	Added    int64  `json:"added"`
	Uploader string `json:"uploader"`
	Link     string `json:"link"`
	Provider string `json:"provider"`
}

type TorrentAdditionalInfo struct {
	Magnet string `json:"magnet"`
}

func parseSizeString(sizeStr string) (int64, error) {
	// Convert sizeStr to lowercase for case insensitivity
	sizeStr = strings.ToLower(sizeStr)

	// Split sizeStr into number and unit
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
		multiplier = 1024 * 1024 * 1024 // 1 GB = 1024 * 1024 * 1024 bytes
	case "mb":
		multiplier = 1024 * 1024 // 1 MB = 1024 * 1024 bytes
	case "kb":
		multiplier = 1024 // 1 KB = 1024 bytes
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

	// Parse the date string into a time.Time object
	dateTime, err := time.Parse(layout, dateStr)
	if err != nil {
		return 0, err
	}

	// Convert time.Time to Unix timestamp (seconds since January 1, 1970 UTC)
	unixTimestamp := dateTime.Unix()

	return unixTimestamp, nil
}

func trimWhiteSpace(str string) string {
	return strings.TrimSpace(str)
}

func getMagnetLink(url string) (string, error) {
	// Create a new collector for fetching the magnet link
	c := colly.NewCollector()
	var magnetUrl string
	var magnetErr error
	done := make(chan bool)

	c.OnHTML("table.lista", func(e *colly.HTMLElement) {
		// Find all tr elements inside the table
		rows := e.DOM.Find("tr")
		firstRow := rows.Eq(0)
		firstRowCells := firstRow.Find("td")

		if firstRowCells.Length() > 0 {
			secondCell := firstRowCells.Eq(1)
			var exists bool
			magnetUrl, exists = secondCell.Find("a").Attr("href")
			if !exists {
				magnetErr = fmt.Errorf("magnet link not found")
			}
		} else {
			magnetErr = fmt.Errorf("no rows found in the table")
		}
		done <- true
	})

	maxRetries := 3 // Maximum number of retries
	retryCount := 0 // Retry counter

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
				magnetErr = err
				done <- true
			}
		}

	})

	// Start scraping
	go func() {
		err := c.Visit(url)
		if err != nil {
			magnetErr = err
			done <- true
		}
	}()

	// Wait for the scraping to complete
	<-done

	if magnetErr != nil {
		return "", magnetErr
	}

	return magnetUrl, nil
}

func main() {
	c := colly.NewCollector(colly.Debugger(&debug.LogDebugger{}))

	var torrents []Torrent
	var mu sync.Mutex
	var wg sync.WaitGroup

	c.OnHTML("table.lista2t", func(e *colly.HTMLElement) {
		// Find all tr elements inside the table
		rows := e.DOM.Find("tr")

		// Iterate over each tr element, skipping the first one
		rows.Slice(1, rows.Length()).Each(func(i int, row *goquery.Selection) {
			// Find all td elements inside the current tr element
			cells := row.Find("td")
			if cells.Length() > 0 {
				nameCell := cells.Eq(1)
				name := nameCell.Text()
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
				wg.Add(1)
				go func() {
					defer wg.Done()
					magnetLink, err := getMagnetLink(absoluteURL)
					if err != nil {
						log.Printf("Failed to get magnet link: %v url: %s", err, absoluteURL)
						return
					}
					// Populate the Torrent struct with cell values
					torrent := Torrent{
						Name:     trimWhiteSpace(name),
						Added:    added,
						Size:     size,
						Seeds:    parseInt(cells.Eq(5).Text()),
						Leeches:  parseInt(cells.Eq(6).Text()),
						Uploader: trimWhiteSpace(cells.Eq(7).Text()),
						Link:     magnetLink,
						Provider: "Rarbg",
					}
					mu.Lock()
					torrents = append(torrents, torrent)
					mu.Unlock()
					fmt.Println("Added torrent:", torrent.Name)
				}()
			}
		})
	})

	maxRetries := 3 // Maximum number of retries
	retryCount := 0 // Retry counter

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
			}
		}
	})

	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL.String())
	})

	err := c.Visit("https://rargb.to/search/1/?search=avengers")
	if err != nil {
		log.Fatalf("Failed to start visit: %v", err)
	}

	wg.Wait()

	// Dump the torrents array as JSON to a file
	file, err := os.Create("torrents.json")
	if err != nil {
		log.Fatalf("Failed to create file: %v", err)
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	err = encoder.Encode(torrents)
	if err != nil {
		log.Fatalf("Failed to encode torrents to JSON: %v", err)
	}

	fmt.Println("Torrents data has been written to torrents.json")
}
