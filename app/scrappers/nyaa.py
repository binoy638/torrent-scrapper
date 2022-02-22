from bs4 import BeautifulSoup
from datetime import datetime
from requests.exceptions import Timeout
import requests
from ..utils import convertDateToTimestamp


def searchNyaa(query):
    url = f"https://nyaa.si/?f=0&c=0_0&q={query}&s=seeders&o=desc"
    try:
        results = requests.get(url, timeout=3)
    except Timeout as excep:
        print("Could not connect to the site...", excep)
        return None

    soup = BeautifulSoup(results.text, "html.parser")

    try:
        table = soup.find("table", class_="table").find("tbody")
    except AttributeError:
        return []

    animes = table.find_all("tr")

    if not animes:
        return []

    anime_list = []

    for anime in animes:

        data = anime.find_all("td")
        try:
            comment = data[1].find("a", class_="comments")
            comment.decompose()
        except Exception as excep:
            title = data[1].text.strip()
        finally:
            title = data[1].text.strip()
            magnet = data[2].find("a").findNext("a")["href"]
            size = data[3].text.strip().replace('i', "")
            added = convertDateToTimestamp(data[4].text.strip())
            seed = data[5].text.strip()
            leech = data[6].text.strip()
            uploader = "unknown"
            anime_list.append({"name": title, "link": magnet, "size": size,
                               "seeds": seed, "leeches": leech, "added": added, "uploader": uploader})
    return anime_list
