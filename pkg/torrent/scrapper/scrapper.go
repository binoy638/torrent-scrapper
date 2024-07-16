package scraper

import (
	"fmt"

	t "github.com/binoy638/torrent-scrapper/pkg/torrent"
)

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

func ScrapeBySite(site string) ([]t.Torrent, error) {
	// switch site {
	// case "site1":
	// 	return ScrapeSite1()
	// case "site2":
	// 	return ScrapeSite2()
	// case "site3":
	// 	return ScrapeSite3()
	// case "site4":
	// 	return ScrapeSite4()
	// default:
	// 	return nil, errors.New("unknown site")
	// }
}
