from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .utils import fetch_metadata, download_and_convert_to_mp3_stream

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
        mp3_data, filename = download_and_convert_to_mp3_stream(video.url)
        return StreamingResponse(mp3_data, media_type="audio/mpeg", headers={
            "Content-Disposition": f"attachment; filename={filename}"
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
