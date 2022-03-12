from unittest import result

from pyparsing import Regex
from .scrappers.pirateBay import searchTPB, getTPBTorrentData
from .scrappers.i1337x import search1337x, get1337xTorrentData
from .scrappers.nyaa import searchNyaa
from .scrappers.rarbg import searchRarbg, getRarbgTorrentData
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .utils import cache_get, cache_set
from typing import Optional


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/search/1337x")
def search1337xRoute(q: Optional[str] = None, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$"), cache: Optional[bool] = True):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    if cache == False:
        result = search1337x(q, filtertype, filtermode)
        return {"results": result}
    key = f"1337x:{q}:{filtertype if filtertype else ''}:{filtermode if filtermode else ''}"
    result = cache_get(key)
    if not result:
        result = search1337x(q, filtertype, filtermode)
        cache_set(key, result, 3600)
    return {"results": result}


@app.get("/search/nyaa")
def searchNyaaRoute(q: Optional[str] = None, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$"), cache: Optional[bool] = True):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    if cache == False:
        result = searchNyaa(q, filtertype, filtermode)
        return {"results": result}
    key = f"Nyaa:{q}:{filtertype if filtertype else ''}:{filtermode if filtermode else ''}"
    result = cache_get(key)
    if not result:
        result = searchNyaa(q, filtertype, filtermode)
        cache_set(key, result, 3600)
    return {"results": result}


@app.get("/search/rarbg")
def searchRarbgRoute(q: Optional[str] = None, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$"), cache: Optional[bool] = True):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    if cache == False:
        result = searchRarbg(q, filtertype, filtermode)
        return {"results": result}
    key = f"Rarbg:{q}:{filtertype if filtertype else ''}:{filtermode if filtermode else ''}"
    result = cache_get(key)
    if not result:
        result = searchRarbg(q, filtertype, filtermode)
        cache_set(key, result, 3600)
    return {"results": result}


@app.get("/search/tpb")
def searchTPBRoute(q: Optional[str] = None, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$"), cache: Optional[bool] = True):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    if cache == False:
        result = searchTPB(q, filtertype, filtermode)
        return {"results": result}
    key = f"TPB:{q}:{filtertype if filtertype else ''}:{filtermode if filtermode else ''}"
    result = cache_get(key)
    if not result:
        result = searchTPB(q, filtertype, filtermode)
        cache_set(key, result, 3600)
    return {"results": result}


@app.get("/get/1337x")
def get1337xRoute(link: Optional[str] = None, cache: Optional[bool] = True):
    if not link:
        raise HTTPException(status_code=400, detail="link is required")
    if cache == False:
        result = get1337xTorrentData(link)
        return {"data": result}
    key = f"1337x:{link}"
    result = cache_get(key)
    if not result:
        result = get1337xTorrentData(link)
        cache_set(key, result)
    return {"data": result}


@app.get("/get/rarbg")
def getRarbgRoute(link: Optional[str] = None, cache: Optional[bool] = True):
    if not link:
        raise HTTPException(status_code=400, detail="link is required")
    if cache == False:
        result = getRarbgTorrentData(link)
        return {"data": result}
    key = f"Rarbg:{link}"
    result = cache_get(key)
    if not result:
        result = getRarbgTorrentData(link)
        cache_set(key, result)
    return {"data": result}


@app.get("/get/tpb")
def getTPBRoute(link: Optional[str] = None, cache: Optional[bool] = True):
    if not link:
        raise HTTPException(status_code=400, detail="link is required")
    if cache == False:
        result = getTPBTorrentData(link)
        return {"data": result}
    key = f"TPB:{link}"
    result = cache_get(key)
    if not result:
        result = getTPBTorrentData(link)
        cache_set(key, result)
    return {"data": result}
