import yt_dlp
import os

def fetch_metadata(url):
    ydl_opts = {"quiet": True,
                'cookiefile': 'cookies.json'
                }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "uploader": info.get("uploader"),
        }



def download_and_convert_to_mp3(url, output_folder="downloads"):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        # "ffmpeg_location": "C:/FFmpeg/bin",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        'cookiefile': 'cookies.json'

    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True, )
        return os.path.join(output_folder, f"{info['title']}.mp3")
    

# download_and_convert_to_mp3("https://youtu.be/E-arMuq4HXA")
