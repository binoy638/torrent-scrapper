import requests
import redis
from datetime import datetime
import cloudscraper
from redis.commands.json.path import Path

redisClient = redis.Redis(host='redis-json', port=6379, db=0)

scrapper = cloudscraper.create_scraper()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45",
    "Accept-Encoding": "*"
}


def cache_set(key, value):
    redisClient.json().set(key, Path.rootPath(), value)


def cache_get(key):
    return redisClient.json().get(key)


def toInt(value):
    return int(value.replace(',', ''))


def convertBytes(num):
    step_unit = 1000.0
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit


def get(url):
    return requests.get(url, headers=headers)


def convertDateToTimestamp(value):
    dt = datetime.strptime(value, "%Y-%m-%d %H:%M")
    return int(dt.timestamp())


def convertStrToDate(Str):
    monthNo = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }
    month = monthNo[Str.split()[0][:-1]]
    day = Str.split()[1][:-2]
    year = "20"+Str.split()[2][1:]
    date = f"{year}-{month}-{day} 00:00"
    return date


def getTPBTrackers():
    tr = "&tr=" + \
        requests.utils.quote("udp://tracker.coppersurfer.tk:6969/announce")
    tr += "&tr=" + requests.utils.quote("udp://9.rarbg.to:2920/announce")
    tr += "&tr=" + requests.utils.quote("udp://tracker.opentrackr.org:1337")
    tr += "&tr=" + \
        requests.utils.quote(
            "udp://tracker.internetwarriors.net:1337/announce")
    tr += "&tr=" + \
        requests.utils.quote(
            "udp://tracker.leechers-paradise.org:6969/announce")
    tr += "&tr=" + \
        requests.utils.quote("udp://tracker.coppersurfer.tk:6969/announce")
    tr += "&tr=" + \
        requests.utils.quote("udp://tracker.pirateparty.gr:6969/announce")
    tr += "&tr=" + \
        requests.utils.quote("udp://tracker.cyberia.is:6969/announce")
    return tr
