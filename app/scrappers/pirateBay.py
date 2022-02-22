from bs4 import BeautifulSoup
from datetime import datetime
import requests
from ..utils import get, toInt, convertBytes, getTPBTrackers


def searchTPB(search_key):
    torrents = []
    resp_json = get(
        f"http://apibay.org/q.php?q={search_key}&cat=100,200,300,400,600").json()
    if(resp_json[0]["name"] == "No results returned"):
        return torrents

    for t in resp_json:
        torrents.append({
            "name": t["name"],
            "seeds": toInt(t["seeders"]),
            "leeches": toInt(t["leechers"]),
            "size": convertBytes(int(t["size"])),
            "added": int(t["added"]),
            "uploader": t["username"],
            "link": f"http://apibay.org/t.php?id={t['id']}",
            "provider": "piratebay"
        })
    return torrents


def getTPBTorrentData(link):
    data = {}
    id = dict(x.split('=')
              for x in requests.utils.urlparse(link).query.split('&'))["id"]
    resp_json = get(f"http://apibay.org/t.php?id={id}").json()
    if(resp_json["name"] == "Torrent does not exsist."):
        data["magnet"] = ""
        data["files"] = []
        return data
    magnet = "magnet:?xt=urn:btih:" + \
        resp_json["info_hash"] + "&dn=" + \
        requests.utils.quote(resp_json["name"]) + getTPBTrackers()
    data["magnet"] = magnet
    resp_json = get(f"http://apibay.org/f.php?id={id}").json()
    files = []
    try:
        for file in resp_json:
            files.append(
                f"{file['name'][0]} ({convertBytes(toInt(file['size'][0]))})")
        data["files"] = files
    except:
        data["files"] = []
    return data
