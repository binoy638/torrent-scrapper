import requests
from datetime import datetime, date
import cloudscraper


scrapper = cloudscraper.create_scraper()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45",
    "Accept-Encoding": "*"
}


def getSource(url):
    source = scrapper.get(url, headers=headers, timeout=5)
    source.raise_for_status()
    return source.text


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

    try:
        month = monthNo[Str.split()[0][:-1]]
        day = Str.split()[1][:-2]
        year = "20"+Str.split()[2][1:]
        torrentDate = f"{year}-{month}-{day} 00:00"
    except Exception as e:
        print(e)
        torrentDate = date.today().strftime("%Y-%m-%d %H:%M")
    finally:
        return torrentDate
