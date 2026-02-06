# server.py
import os
import logging
import shutil
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Agents
from presentation_agent.agents.input_agent import InputAgent
from presentation_agent.agents.planner_agent import PlannerAgent
from presentation_agent.agents.slide_agent import SlideAgent
from presentation_agent.agents.video_agent import VideoAgent

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Allow CORS for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "workspace/input")
OUTPUT_DIR = os.path.join(BASE_DIR, "workspace/output")
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_video_task(input_file_path: str, output_file_path: str):
    """
    Generates video directly to the output_file_path.
    """
    try:
        logger.info(f"Video generation started for {input_file_path}")

        slides = InputAgent().run(input_file_path)
        logger.info(f"Slides processed: {len(slides)}")

        plan = PlannerAgent().run(slides)
        logger.info(f"Slide plan created with {len(plan)} steps")

        images = SlideAgent().run(plan)
        logger.info(f"Generated {len(images)} slide images")

        # Pass output path directly to VideoAgent
        VideoAgent().run(images, plan, output_path=output_file_path)
        logger.info(f"Video successfully saved to {output_file_path}")

    except Exception as e:
        logger.exception(f"Video generation failed for {input_file_path}: {e}")


@app.post("/generate")
def generate(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    input_file_path = os.path.join(INPUT_DIR, file.filename)
    with open(input_file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    base_name = os.path.splitext(file.filename)[0]
    output_file_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")

    background_tasks.add_task(generate_video_task, input_file_path, output_file_path)

    return {
        "status": "Video generation started!",
        "input_file": file.filename,
        "output_file": f"{base_name}.mp4"
    }


# JSON-based endpoint
class JSONInput(BaseModel):
    fileName: str
    fileText: str


@app.post("/generateFromJson")
def generate_from_json(background_tasks: BackgroundTasks, data: JSONInput):
    input_file_path = os.path.join(INPUT_DIR, data.fileName)
    with open(input_file_path, "w", encoding="utf-8") as f:
        f.write(data.fileText)

    base_name = os.path.splitext(data.fileName)[0]
    output_file_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")

    background_tasks.add_task(generate_video_task, input_file_path, output_file_path)

    return {
        "status": "Video generation started!",
        "input_file": data.fileName,
        "output_file": f"{base_name}.mp4"
    }


@app.get("/download")
def download(file_name: str = Query(..., description="Name of the MP4 file to download")):
    output_file_path = os.path.join(OUTPUT_DIR, file_name)
    if not os.path.exists(output_file_path):
        return {"error": "Video not ready yet. Call /generate or /generateFromJson first."}

    return FileResponse(output_file_path, media_type="video/mp4", filename=file_name)


@app.get("/")
def home():
    return {"status": "AI Presentation Service is live!"}
