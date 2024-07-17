package constants

type Site string

const (
	RARBG_URL  Site = "https://rargb.to"
	I1337X_URL Site = "https://1337xx.to"
	TPB_URL    Site = "https://apibay.org/q.php"
	NYAA_URL   Site = "https://nyaa.si/?f=0&c=0_0"
)

type SortField string

const (
	SEEDERS  SortField = "seeders"
	LEECHERS SortField = "leechers"
	SIZE     SortField = "size"
	TIME     SortField = "time"
)

type SortOrder string

const (
	ASC  SortOrder = "asc"
	DESC SortOrder = "desc"
)
