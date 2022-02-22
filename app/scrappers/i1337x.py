from bs4 import BeautifulSoup
from ..utils import scrapper, toInt, convertStrToDate, convertDateToTimestamp


def search1337x(search_key):
    torrents = []
    source = scrapper.get(f"https://1337x.to/search/{search_key}/1/").text
    soup = BeautifulSoup(source, "lxml")
    for tr in soup.select("tbody > tr"):
        a = tr.select("td.coll-1 > a")[1]
        torrents.append({
            "name": a.text,
            "seeds": toInt(tr.select("td.coll-2")[0].text),
            "leeches": toInt(tr.select("td.coll-3")[0].text),
            "size": str(tr.select("td.coll-4")[0].text).split('B', 1)[0] + "B",
            "added": convertDateToTimestamp(convertStrToDate(tr.select("td.coll-date")[0].text)),
            "uploader": tr.select("td.coll-5 > a")[0].text,
            "link": f"http://1337x.to{a['href']}",
            "provider": "1337"
        })
    return torrents


def get1337xTorrentData(link):
    data = {}
    source = scrapper.get(link).text
    soup = BeautifulSoup(source, "lxml")
    data["magnet"] = soup.select('ul.dropdown-menu > li')[-1].find('a')['href']
    data["torrent_file"] = soup.select(
        'ul.dropdown-menu > li')[0].find('a')['href']
    files = []
    for li in soup.select('div.file-content > ul > li'):
        files.append(li.text)

    data["files"] = files
    return data
