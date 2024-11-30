from yt_dlp import YoutubeDL

# url = "https://www.youtube.com/watch?v=your_video_id"
url = "https://youtu.be/E-arMuq4HXA"
options = {"format": "bestaudio"}
with YoutubeDL(options) as ydl:
    info_dict = ydl.extract_info(url, download=False)
    audio_url = info_dict['url']
    print(f"Audio URL: {audio_url}")
