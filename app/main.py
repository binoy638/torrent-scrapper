from .scrappers.pirateBay import searchTPB, getTPBTorrentData
from .scrappers.i1337x import search1337x, get1337xTorrentData
from .scrappers.nyaa import searchNyaa
from .scrappers.rarbg import searchRarbg, getRarbgTorrentData
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def errors_handling(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        return JSONResponse(status_code=500, content={'reason': str(exc)})


@app.get("/")
def read_root():
    return {"message": "ok"}


@app.get("/search/1337x")
def search1337xRoute(q: str, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$"), page: Optional[int] = Query(1, gt=0), nsfw: Optional[bool] = Query(False)):
    return {"results": search1337x(q, filtertype, filtermode, page, nsfw)}


@app.get("/search/nyaa")
def searchNyaaRoute(q: str, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$"), page: Optional[int] = Query(1, gt=0)):
    return {"results": searchNyaa(q, filtertype, filtermode, page)}


@app.get("/search/rarbg")
def searchRarbgRoute(q: str, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$"), page: Optional[int] = Query(1, gt=0), nsfw: Optional[bool] = Query(False)):
    return {"results": searchRarbg(q, filtertype, filtermode, page, nsfw)}


@app.get("/search/tpb")
def searchTPBRoute(q: str, filtertype: Optional[str] = Query(None, regex="^time$|^size$|^seeders$|^leechers$"), filtermode: Optional[str] = Query(None, regex="^asc$|^desc$")):
    return {"results": searchTPB(q, filtertype, filtermode)}


@app.get("/get/1337x")
def get1337xRoute(link: str):
    return {"data": get1337xTorrentData(link)}


@app.get("/get/rarbg")
def getRarbgRoute(link: str):
    return {"data": getRarbgTorrentData(link)}


@app.get("/get/tpb")
def getTPBRoute(link: str):
    return {"data": getTPBTorrentData(link)}


handler = Mangum(app)
