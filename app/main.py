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


# @app.middleware("http")
# async def check_query_param(request: Request, call_next):
#     print("inside middleware")
#     response = await call_next(request)
#     return response


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/search/1337x")
def search1337xRoute(q: str, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$")):
    try:
        result = search1337x(q, filtertype, filtermode)
        return {"results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/nyaa")
def searchNyaaRoute(q: str, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$")):
    try:
        result = searchNyaa(q, filtertype, filtermode)
        return {"results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/rarbg")
def searchRarbgRoute(q: str, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$")):
    try:
        result = searchRarbg(q, filtertype, filtermode)
        return {"results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/tpb")
def searchTPBRoute(q: str, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$")):
    try:
        result = searchTPB(q, filtertype, filtermode)
        return {"results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get/1337x")
def get1337xRoute(link: str):
    try:
        result = get1337xTorrentData(link)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get/rarbg")
def getRarbgRoute(link: str):
    try:
        result = getRarbgTorrentData(link)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get/tpb")
def getTPBRoute(link: str):
    try:
        result = getTPBTorrentData(link)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


handler = Mangum(app)
