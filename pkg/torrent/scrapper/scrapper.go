package scraper

import (
	"errors"
	"fmt"

	t "github.com/binoy638/torrent-scrapper/pkg/torrent"
	"github.com/binoy638/torrent-scrapper/types"
)

func BuildCompleteUrl(site types.Site, q string, sortField types.SortField, sortOrder types.SortOrder, page string, nsfw bool) string {
	var url string
	switch site {
	case types.RARBG_URL:
		url = string(types.RARBG_URL) + "/search/" + page + "/?search=" + q + "&category[]=movies&category[]=tv&category[]=games&category[]=music&category[]=anime&category[]=apps&category[]=documentaries&category[]=other"

		if nsfw {
			url = string(types.RARBG_URL) + "/search/" + page + "/?search=" + q
		}

		if sortField != "" && sortOrder != "" {
			if sortField == types.TIME {
				sortField = types.SortField("data") // Convert to string for concatenation
			}
			url = url + "&order=" + string(sortField) + "&by=" + string(sortOrder)
		}
	}
	fmt.Println(url)
	return url
}

func ScrapeBySite(site types.Site, q string, sortField types.SortField, sortOrder types.SortOrder, page string, nsfw bool) ([]t.Torrent, error) {
	switch site {
	case "site1":
		return ScrapeRarbg(BuildCompleteUrl(site, q, sortField, sortOrder, page, nsfw))
	default:
		return nil, errors.New("unknown site")
	}
}
