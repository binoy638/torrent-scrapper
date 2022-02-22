from unittest import result
from .scrappers.pirateBay import searchTPB, getTPBTorrentData
from .scrappers.i1337x import search1337x, get1337xTorrentData
from .scrappers.nyaa import searchNyaa
from .scrappers.rarbg import searchRarbg, getRarbgTorrentData
from fastapi import FastAPI, HTTPException
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
def search1337xRoute(q: Optional[str] = None, cache: Optional[bool] = True):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    if cache == False:
        result = search1337x(q)
        return {"results": result}
    key = f"1337x:{q}"
    result = cache_get(key)
    if not result:
        result = search1337x(q)
        cache_set(key, result, 3600)
    return {"results": result}


@app.get("/search/nyaa")
def searchNyaaRoute(q: Optional[str] = None, cache: Optional[bool] = True):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    if cache == False:
        result = searchNyaa(q)
        return {"results": result}
    key = f"Nyaa:{q}"
    result = cache_get(key)
    if not result:
        result = searchNyaa(q)
        cache_set(key, result, 3600)
    return {"results": result}


@app.get("/search/rarbg")
def searchRarbgRoute(q: Optional[str] = None, cache: Optional[bool] = True):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    if cache == False:
        result = searchRarbg(q)
        return {"results": result}
    key = f"Rarbg:{q}"
    result = cache_get(key)
    if not result:
        result = searchRarbg(q)
        cache_set(key, result, 3600)
    return {"results": result}


@app.get("/search/tpb")
def searchTPBRoute(q: Optional[str] = None, cache: Optional[bool] = True):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    if cache == False:
        result = searchTPB(q)
        return {"results": result}
    key = f"TPB:{q}"
    result = cache_get(key)
    if not result:
        result = searchTPB(q)
        cache_set(key, result, 3600)
    return {"results": result}


@app.get("/get/1337x")
def get1337xRoute(link: Optional[str] = None):
    if not link:
        raise HTTPException(status_code=400, detail="link is required")
    result = get1337xTorrentData(link)
    return {"data": result}


@app.get("/get/rarbg")
def getRarbgRoute(link: Optional[str] = None):
    if not link:
        raise HTTPException(status_code=400, detail="link is required")
    result = getRarbgTorrentData(link)
    return {"data": result}


@app.get("/get/tpb")
def getTPBRoute(link: Optional[str] = None):
    if not link:
        raise HTTPException(status_code=400, detail="link is required")
    result = getTPBTorrentData(link)
    return {"data": result}
