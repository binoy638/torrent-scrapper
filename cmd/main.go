package main

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/binoy638/torrent-scrapper/pkg/torrent"
	"github.com/binoy638/torrent-scrapper/types"

	"github.com/gin-gonic/gin"
)

func GetTorrents(c *gin.Context) {
	site := c.Query("site")

	q := c.Query("q")

	sortField := c.DefaultQuery("sort_field", "")

	sortOrder := c.DefaultQuery("sort_order", "")

	page := c.DefaultQuery("page", "1")

	nsfwParam := c.DefaultQuery("nsfw", "false")

	nsfw, err := strconv.ParseBool(nsfwParam)

	if err != nil {
		nsfw = false
	}

	torrents, err := torrent.ScrapeBySite(types.Site(site), q, types.SortField(sortField), types.SortOrder(sortOrder), page, nsfw)

	if err != nil {
		fmt.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{"error": "Error scraping torrents"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": http.StatusOK, "data": torrents})
}

func main() {

	router := gin.Default()

	router.GET("/torrents", GetTorrents)

	router.Run(":8080")

}
