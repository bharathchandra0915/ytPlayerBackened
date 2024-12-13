import yt_dlp
from io import BytesIO
import os
import tempfile


def fetch_metadata(url):
    ydl_opts = {
        "quiet": True,
        "cookiefile": "cookies.txt",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail"),
                "uploader": info.get("uploader"),
            }
        except yt_dlp.utils.DownloadError as e:
            print(f"Error fetching metadata: {e}")
            return None


def get_best_audio_format(info):
    """
    Finds the best available audio format.
    """
    formats = info.get("formats", [])
    audio_formats = [f for f in formats if f.get("acodec") != "none"]
    if not audio_formats:
        raise Exception("No audio formats available")
    # Sort by audio quality
    audio_formats.sort(key=lambda f: f.get("abr", 0), reverse=True)
    return audio_formats[0]["format_id"]


def download_and_convert_to_mp3_stream(url):
    mp3_data = BytesIO()

    with tempfile.TemporaryDirectory() as temp_dir:
        ydl_opts = {
            "cookiefile": "cookies.txt",
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Fetch video info
                info = ydl.extract_info(url, download=False)
                
                # Determine the best audio format
                best_audio_format = get_best_audio_format(info)

                # Update options to download the best available audio format
                ydl_opts.update({
                    "format": best_audio_format,
                    "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                })

                # Reinitialize ydl with updated options
                with yt_dlp.YoutubeDL(ydl_opts) as ydl_download:
                    ydl_download.download([url])

                # Find the downloaded MP3 file
                temp_file = os.path.join(temp_dir, f"{info['title']}.mp3")

                if os.path.exists(temp_file):
                    with open(temp_file, "rb") as mp3_file:
                        mp3_data.write(mp3_file.read())
                else:
                    raise Exception("MP3 file was not created.")

            except yt_dlp.utils.DownloadError as e:
                print(f"Error downloading file: {e}")
                return None, None
            except Exception as e:
                print(f"Error: {e}")
                return None, None

    mp3_data.seek(0)  # Reset the stream pointer for reading
    return mp3_data, f"{info['title']}.mp3"
