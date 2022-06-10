from bs4 import BeautifulSoup
from .utils import scrapper, toInt, convertStrToDate, convertDateToTimestamp, getSource
from requests.exceptions import Timeout


def search1337x(search_key, filter_criteria=None, filter_mode=None):
    baseUrl = f"https://1337xx.to"
    if filter_criteria is not None and filter_mode is not None:
        baseUrl = baseUrl + \
            f"/sort-search/{search_key}/{filter_criteria}/{filter_mode}/1/"
    else:
        baseUrl = baseUrl + f"/search/{search_key}/1/"
    torrents = []

    try:
        source = getSource(baseUrl)
    except Exception as e:
        raise Exception(e)

    soup = BeautifulSoup(source, "lxml")
    for tr in soup.select("tbody > tr"):
        a = tr.select("td.coll-1 > a")[1]
        try:
            # use regex to extract the date
            date = convertDateToTimestamp(
                convertStrToDate(tr.select("td.coll-date")[0].text))
        except Exception as e:
            print('exception while extracting date from 1337x')
            print(e)
            date = 1531699200
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
    return torrents


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
