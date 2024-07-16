package torrent

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
