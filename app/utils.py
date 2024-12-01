import yt_dlp
from io import BytesIO
import os

def fetch_metadata(url):
    ydl_opts = {"quiet": True,
                'cookiefile': 'cookies.txt'
                }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "uploader": info.get("uploader"),
        }

def download_and_convert_to_mp3_stream(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        'cookiefile': 'cookies.txt'
    }

    mp3_data = BytesIO()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info)

        ydl.download([url])  # Download the file to local storage
        temp_file = f"{os.path.splitext(filename)[0]}.mp3"
        
        with open(temp_file, "rb") as mp3_file:
            mp3_data.write(mp3_file.read())
        
        os.remove(temp_file)  # Clean up the temporary file

    mp3_data.seek(0)  # Reset the stream pointer for reading
    return mp3_data, f"{info['title']}.mp3"
