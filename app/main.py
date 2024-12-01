from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .utils import fetch_metadata, download_and_convert_to_mp3_stream

# Create FastAPI app
app = FastAPI()

# Enable CORS to handle OPTIONS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; replace with specific URLs for production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define Video URL model
class VideoURL(BaseModel):
    url: str

# Root endpoint
@app.get("/")
def root():
    return {"message": "YouTube to MP3 Converter API"}

# Metadata endpoint
@app.post("/metadata/")
def get_metadata(video: VideoURL):
    try:
        metadata = fetch_metadata(video.url)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Download MP3 endpoint
@app.post("/download/")
def download_mp3(video: VideoURL):
    try:
        mp3_data, filename = download_and_convert_to_mp3_stream(video.url)
        return StreamingResponse(mp3_data, media_type="audio/mpeg", headers={
            "Content-Disposition": f"attachment; filename={filename}"
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
