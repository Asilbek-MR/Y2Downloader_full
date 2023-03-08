from fastapi import FastAPI, Request,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pytube import YouTube
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import os
from pathlib import Path
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return RedirectResponse("/")

@app.get("/", response_class=HTMLResponse)
async def download_q(request: Request):
    return templates.TemplateResponse("index.html",{"request": request} )


@app.post("/about",response_class=HTMLResponse)
async def about(request: Request,url: str = Form(...)):
    global test_url
    try:
        form_date = await request.form()
        youtubeUrl = form_date["url"]
        test_url=YouTube(youtubeUrl)
        test_title = test_url.title
        videos = test_url.streams.filter()
        img_url=test_url.thumbnail_url
        return templates.TemplateResponse("about.html" ,{"request":request, "videos":videos,"img_url":img_url,"test_title":test_title})
    except:
        mesage = 'Enter Valid YouTube Video URL!'
    return templates.TemplateResponse("about.html", {"request":request, "mesage":mesage})

@app.post("/done", response_class=HTMLResponse)
async def download_vid(request: Request,Download: str = Form(...)):
    global test_url
    try:
        print(Download)
        downloadFolder = str(os.path.join(Path.home(), "Downloads"))
        test_url.streams.get_by_resolution(Download).download(downloadFolder)
        mesage = 'Please see the Downloads folder of the device... '
    except:
        mesage = 'Downloading the video in this format is prohibited by the author !!!'
    return templates.TemplateResponse("done.html",{"request": request, "mesage" : mesage} )
