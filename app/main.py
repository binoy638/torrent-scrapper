from unittest import result

from pyparsing import Regex
from .scrappers.pirateBay import searchTPB, getTPBTorrentData
from .scrappers.i1337x import search1337x, get1337xTorrentData
from .scrappers.nyaa import searchNyaa
from .scrappers.rarbg import searchRarbg, getRarbgTorrentData
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
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
def search1337xRoute(q: Optional[str] = None, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$")):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    result = search1337x(q, filtertype, filtermode)
    return {"results": result}


@app.get("/search/nyaa")
def searchNyaaRoute(q: Optional[str] = None, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$")):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    result = searchNyaa(q, filtertype, filtermode)
    return {"results": result}


@app.get("/search/rarbg")
def searchRarbgRoute(q: Optional[str] = None, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$")):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    result = searchRarbg(q, filtertype, filtermode)
    return {"results": result}


@app.get("/search/tpb")
def searchTPBRoute(q: Optional[str] = None, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$")):
    if not q:
        raise HTTPException(status_code=400, detail="No search query")
    result = searchTPB(q, filtertype, filtermode)
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


handler = Mangum(app)
