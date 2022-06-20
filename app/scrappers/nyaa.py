from bs4 import BeautifulSoup
from datetime import datetime
from requests.exceptions import Timeout
import requests
from .utils import convertDateToTimestamp


def searchNyaa(search_key, filter_criteria=None, filter_mode=None, page=1):
    baseUrl = f"https://nyaa.si/?f=0&c=0_0&q={search_key}&p={page}"
    if filter_criteria is not None and filter_mode is not None:
        if filter_criteria == "time":
            filter_criteria = "id"
        baseUrl = baseUrl + f"&s={filter_criteria}&o={filter_mode}"
    try:
        results = requests.get(baseUrl, timeout=3)
    except Exception as e:
        raise Exception(e)

    soup = BeautifulSoup(results.text, "html.parser")

    try:
        table = soup.find("table", class_="table").find("tbody")
    except AttributeError as e:
        return [], 1
    try:
        totalPages = soup.find(
            "ul", class_="pagination").find_all("li")[-2].text
        if not totalPages.isnumeric():
            totalPages = 1
    except Exception as e:
        print(e)
        totalPages = 1

    animes = table.find_all("tr")

    if not animes:
        return [], 1

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
    return anime_list, totalPages
