import requests
from .utils import get, toInt, convertBytes, getTPBTrackers

PAGE_COUNT = 20


def sort_torrents(torrents, sort_criteria, sort_mode):
    if sort_criteria == "seeders":
        if sort_mode == "asc":
            return sorted(torrents, key=lambda x: x["seeds"])
        else:
            return sorted(torrents, key=lambda x: x["seeds"], reverse=True)
    elif sort_criteria == "leechers":
        if sort_mode == "asc":
            return sorted(torrents, key=lambda x: x["leeches"])
        else:
            return sorted(torrents, key=lambda x: x["leeches"], reverse=True)
    elif sort_criteria == "size":
        if sort_mode == "asc":
            return sorted(torrents, key=lambda x: x["sizeInt"])
        else:
            return sorted(torrents, key=lambda x: x["sizeInt"], reverse=True)
    elif sort_criteria == "time":
        if sort_mode == "asc":
            return sorted(torrents, key=lambda x: x["added"])
        else:
            return sorted(torrents, key=lambda x: x["added"], reverse=True)
    else:
        return torrents


def searchTPB(search_key, sort_criteria=None, sort_mode=None, page=1, nsfw=False):
    torrents = []

    baseUrl = f"https://apibay.org/q.php?q={search_key}&cat=100,200,300,400,600"

    if nsfw:
        baseUrl = f"https://apibay.org/q.php?q={search_key}&cat=100,200,300,400,500,600"

    resp_json = get(baseUrl).json()

    if(resp_json[0]["name"] == "No results returned"):
        return torrents, 1

    for t in resp_json:
        torrents.append({
            "name": t["name"],
            "seeds": toInt(t["seeders"]),
            "leeches": toInt(t["leechers"]),
            "size": convertBytes(int(t["size"])),
            "sizeInt": int(t["size"]),
            "added": int(t["added"]),
            "uploader": t["username"],
            "link": f"http://apibay.org/t.php?id={t['id']}",
            "provider": "tpb"
        })

    if sort_criteria is not None and sort_mode is not None:
        torrents = sort_torrents(torrents, sort_criteria, sort_mode)

    totalPages = len(torrents) // PAGE_COUNT

    return torrents[PAGE_COUNT * (page-1):PAGE_COUNT * page], totalPages


def getTPBTorrentData(link):
    data = {}
    id = dict(x.split('=')
              for x in requests.utils.urlparse(link).query.split('&'))["id"]
    resp_json = get(f"https://apibay.org/t.php?id={id}").json()
    if(resp_json["name"] == "Torrent does not exsist."):
        data["magnet"] = ""
        data["files"] = []
        return data
    print(getTPBTrackers())
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
