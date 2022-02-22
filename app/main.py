from unittest import result
from .scrappers.pirateBay import searchTPB
from .scrappers.i1337x import search1337x
from .scrappers.nyaa import searchNyaa
from .scrappers.rarbg import searchRarbg
from fastapi import FastAPI, HTTPException
from .utils import cache_get, cache_set
from typing import Optional


app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/search/1337x")
def search1337xRoute(q: Optional[str] = None):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    key = f"1337x:{q}"
    result = cache_get(key)
    if not result:
        result = search1337x(q)
        cache_set(key, result)
    return {"results": result}


@app.get("/search/nyaa")
def searchNyaaRoute(q: Optional[str] = None):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    key = f"Nyaa:{q}"
    result = cache_get(key)
    if not result:
        result = searchNyaa(q)
        cache_set(key, result)
    return {"results": result}


@app.get("/search/rarbg")
def searchNyaaRoute(q: Optional[str] = None):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    key = f"Rarbg:{q}"
    result = cache_get(key)
    if not result:
        result = searchRarbg(q)
        cache_set(key, result)
    return {"results": result}


@app.get("/search/piratebay")
def searchNyaaRoute(q: Optional[str] = None):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    key = f"TPB:{q}"
    result = cache_get(key)
    if not result:
        result = searchTPB(q)
        cache_set(key, result)
    return {"results": result}
