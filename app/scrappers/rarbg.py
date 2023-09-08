from bs4 import BeautifulSoup
from .utils import toInt, convertDateToTimestamp, getSource


def searchRarbg(search_key, filter_criteria=None, filter_mode=None, page=1, nsfw=False):
    baseUrl = f"https://rargb.to/search/{page}/?search={search_key}&category[]=movies&category[]=tv&category[]=games&category[]=music&category[]=anime&category[]=apps&category[]=documentaries&category[]=other"
    if nsfw:
        baseUrl = f"https://rargb.to/search/{page}/?search={search_key}"
    if filter_criteria is not None and filter_mode is not None:
        if filter_criteria == "time":
            filter_criteria = "data"
        baseUrl = baseUrl + f"&order={filter_criteria}&by={filter_mode}"
    torrents = []

    try:
        source = getSource(baseUrl)
    except Exception as e:
        raise Exception(e)
    soup = BeautifulSoup(source, "lxml")

    try:
        pageCounts = soup.find(
            "div", attrs={"id": "pager_links"}).find_all("a")
        if pageCounts[-1].text.isnumeric():
            totalPages = pageCounts[-1].text
        elif pageCounts[-2].text.isnumeric():
            totalPages = pageCounts[-2].text
        else:
            totalPages = 1
    except Exception as e:
        print(e)
        totalPages = 1

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
    return torrents, totalPages


def getRarbgTorrentData(link):
    data = {}
    try:
        source = getSource(link)
    except Exception as e:
        raise Exception(e)
    soup = BeautifulSoup(source, "lxml")

    trs = soup.select("table.lista > tbody > tr")
    data["magnet"] = trs[0].find('a')["href"]
    files = []
    for li in trs[6].select("td.lista > div > ul > li"):
        files.append(li.text.strip())
    data["files"] = files
    return data
