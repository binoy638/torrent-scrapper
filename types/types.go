package types

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
	Link     string   `json:"link"`
}

type Site string

const (
	RARBG  Site = "rargb"
	I1337X Site = "1337x"
	TPB    Site = "tpb"
	NYAA   Site = "nyaa"
)

type SiteUrl string

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
