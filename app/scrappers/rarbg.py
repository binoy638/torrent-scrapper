from bs4 import BeautifulSoup
from ..utils import get, toInt, convertDateToTimestamp


def searchRarbg(search_key, filter_criteria=None, filter_mode=None):
    baseUrl = f"https://rargb.to/search/?search={search_key}"
    if filter_criteria is not None and filter_mode is not None:
        if filter_mode == "time":
            filter_mode = "data"
        baseUrl = baseUrl + f"&order={filter_criteria}&by={filter_mode}"
    torrents = []
    source = get(baseUrl).text
    soup = BeautifulSoup(source, "lxml")
    for tr in soup.select("tr.lista2"):
        tds = tr.select("td")
        torrents.append({
            "name": tds[1].a.text,
            "seeds": toInt(tds[5].font.text),
            "leeches": toInt(tds[6].text),
            "size": tds[4].text,
            "added": convertDateToTimestamp(tds[3].text[:-3]),
            "uploader": tds[7].text,
            "link": f"http://rargb.to{tds[1].a['href']}",
            "provider": "rarbg"
        })
    return torrents


def getRarbgTorrentData(link):
    data = {}
    source = get(link).text
    soup = BeautifulSoup(source, "lxml")

    trs = soup.select("table.lista > tbody > tr")

    data["magnet"] = trs[0].a.find_next('a')["href"]
    files = []
    for li in trs[6].select("td.lista > div > ul > li"):
        files.append(li.text.strip())
    data["files"] = files
    return data
