from bs4 import BeautifulSoup
from datetime import datetime
from ..utils import get, toInt, convertDateToTimestamp


def searchRarbg(search_key):
    torrents = []
    source = get(
        f"http://rargb.to/search/?search={search_key}"
        "&category[]=movies&category[]=tv&category[]=games&"
        "category[]=music&category[]=anime&category[]=apps&"
        "category[]=documentaries&category[]=other"
    ).text
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
    data["magnet"] = trs[0].a["href"]
    files = []
    for li in trs[6].select("td.lista > div > ul > li"):
        files.append(li.text.strip())
    data["files"] = files
    return data
