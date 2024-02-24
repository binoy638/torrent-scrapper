from bs4 import BeautifulSoup
from .utils import toInt, convertStrToDate, convertDateToTimestamp, getSource
from requests.exceptions import Timeout


def search1337x(search_key, filter_criteria=None, filter_mode=None, page=1, nsfw=False):
    baseUrl = f"https://1337xx.to"
    if filter_criteria is not None and filter_mode is not None:
        baseUrl = baseUrl + \
            f"/sort-search/{search_key}/{filter_criteria}/{filter_mode}/{page}/"
    else:
        baseUrl = baseUrl + f"/search/{search_key}/{page}/"
    torrents = []
    try:
        source = getSource(baseUrl)
    except Exception as e:
        raise Exception(e)

    soup = BeautifulSoup(source, "lxml")

    try:

        pageCounts = soup.select('div.pagination > ul > li')
        if pageCounts[-1].text.isnumeric():
            totalPages = pageCounts[-1].text
        elif pageCounts[-2].text.isnumeric():
            totalPages = pageCounts[-2].text
        elif pageCounts[-3].text.isnumeric():
            totalPages = pageCounts[-3].text
        else:
            totalPages = 1
    except Exception as e:
        print(e)
        totalPages = 1

    for tr in soup.select("tbody > tr"):
        is_nsfw = tr.select("td.coll-1 > a")[0]["href"].split("/")[2] == "xxx"
        if not nsfw and is_nsfw:
            continue
        a = tr.select("td.coll-1 > a")[1]

        date = convertDateToTimestamp(
            convertStrToDate(tr.select("td.coll-date")[0].text))

        torrents.append({
            "name": a.text,
            "seeds": toInt(tr.select("td.coll-2")[0].text),
            "leeches": toInt(tr.select("td.coll-3")[0].text),
            "size": str(tr.select("td.coll-4")[0].text).split('B', 1)[0] + "B",
            "added": date,
            "uploader": tr.select("td.coll-5 > a")[0].text,
            "link": f"http://1337xx.to{a['href']}",
            "provider": "1337x"
        })
    return torrents, totalPages


def get1337xTorrentData(link):
    data = {}
    try:
        source = getSource(link)
    except Exception as e:
        raise Exception(e)
    soup = BeautifulSoup(source, "lxml")
    data["magnet"] = soup.select('ul.dropdown-menu > li')[-1].find('a')['href']
    data["torrent_file"] = soup.select(
        'ul.dropdown-menu > li')[0].find('a')['href']
    files = []
    for li in soup.select('div.file-content > ul > li'):
        files.append(li.text)

    data["files"] = files
    return data
