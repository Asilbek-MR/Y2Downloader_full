import youtube_dl


def download_video(url):
    ydl_opts = {
        'format': 'best[height<=360]'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

download_video('https://www.youtube.com/shorts/DTjPAsJl8Gk')