from fastapi import FastAPI, Request, Form, File
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pytube import YouTube
from fastapi.responses import RedirectResponse, StreamingResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import os
from io import BytesIO
from pathlib import Path
app = FastAPI()

# origins = ['*']

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# ) 

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return RedirectResponse("/")

@app.get("/", response_class=HTMLResponse)
async def download_q(request: Request):
    return templates.TemplateResponse("index.html",{"request": request} )


@app.post("/about",response_class=HTMLResponse)
async def about(request: Request):
    global test_url
    try:
        form_date = await request.form()
        youtubeUrl = form_date["url"]
        print(youtubeUrl)
        test_url=YouTube(youtubeUrl)
        
        test_title = test_url.title
        videos = test_url.streams.filter(progressive=True)
        audio = test_url.streams.filter(only_audio=True)
        img_url=test_url.thumbnail_url
        mesage = '++++++++++++++++'
    except:
        mesage = 'Enter Valid YouTube Video URL!'
        return templates.TemplateResponse("about.html" ,{"request":request, "mesage":mesage})
    return templates.TemplateResponse("about.html", {"request":request, "mesage":mesage,"videos":videos,"test_title":test_title,"img_url":img_url,"audio":audio})

@app.post("/done", response_class=HTMLResponse)
async def download_vid(request: Request,download: str = Form(...)):
    global test_url
    
    buffer = BytesIO()
    try:
        message = "No audio is available in this format!!"
        video = test_url.streams.get_by_resolution(download)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        headers = {
                "Content-Disposition": f'attachment; filename="{test_url.title}.mp4"'
            }
        return StreamingResponse(buffer,media_type="video/mp4", headers=headers)
    except:
        return templates.TemplateResponse("index.html",{"request":request,"message":message})
    # return templates.TemplateResponse("index.html",{"request":request})