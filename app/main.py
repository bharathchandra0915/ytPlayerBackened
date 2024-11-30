from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .utils import fetch_metadata, download_and_convert_to_mp3

app = FastAPI()

class VideoURL(BaseModel):
    url: str

@app.get("/")
def root():
    return {"message": "YouTube to MP3 Converter API"}

@app.post("/metadata/")
def get_metadata(video: VideoURL):
    try:
        metadata = fetch_metadata(video.url)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/download/")
def download_mp3(video: VideoURL):
    try:
        file_path = download_and_convert_to_mp3(video.url)
        return {"message": "Download complete", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
