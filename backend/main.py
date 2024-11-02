import asyncio
import os
from pathlib import Path

import aioredis
import cv2
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from visualize import visualize_detection

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

ROOT = Path(__file__).parent.parent
VIDEO_DIR = ROOT / os.getenv("VIDEO_DIR", "video")
print(f"VIDEO_DIR: {VIDEO_DIR}")

# Initialize Redis connection
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", "6379")
redis_url = f"redis://{redis_host}:{redis_port}"
redis = aioredis.from_url(redis_url)

dataset_dir = os.getenv("DATASET_DIR", "yolo")
path = Path(ROOT / dataset_dir)
all_image_files = [*path.glob("**/*.jpg")]
all_text_files = [*path.glob("**/*.txt")]

image_files = sorted(all_image_files, key=lambda x: int(x.stem.split("_")[1]))
annotation_files = sorted(all_text_files, key=lambda x: int(x.stem.split("_")[1]))


async def video_stream():
    video_files = Path(VIDEO_DIR).glob("*.mp4")
    video_path = next(iter(video_files), None)
    if not os.path.exists(video_path) or not video_path:
        raise FileNotFoundError("No video files found in the specified folder.")
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        logger.info(f"Reading frame number: {frame_number}")

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video if it has ended
            continue

        image_path = next(
            filter(
                lambda img: int(img.stem.split("_")[1]) == frame_number, image_files
            ),
            None,
        )
        annotation_path = next(
            filter(
                lambda txt: int(txt.stem.split("_")[1]) == frame_number,
                annotation_files,
            ),
            None,
        )

        result = visualize_detection(frame_number, image_path, annotation_path)
        if result is not None:
            frame = result

        # Convert the image to bytes
        _, buffer = cv2.imencode(".jpg", frame)

        frame_bytes = buffer.tobytes()
        await redis.rpush("video_frames", frame_bytes)
        await redis.ltrim("video_frames", -100, -1)  # Keep only the last 100 frames


@app.get("/")
def get_root():
    return {"message": "Welcome to the video streamer!"}


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(video_stream())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        frame_bytes = await redis.lpop("video_frames")
        if frame_bytes:
            await websocket.send_bytes(frame_bytes)


if __name__ == "__main__":
    load_dotenv()

    host = os.getenv("FASTAPI_HOST", "localhost")
    port = int(os.getenv("FASTAPI_PORT", 8888))

    uvicorn.run(app, host=host, port=port)
