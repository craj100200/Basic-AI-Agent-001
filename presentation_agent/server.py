# server.py
import os
import logging
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse

# ✅ Full package imports
from presentation_agent.agents.input_agent import InputAgent
from presentation_agent.agents.planner_agent import PlannerAgent
from presentation_agent.agents.slide_agent import SlideAgent
from presentation_agent.agents.video_agent import VideoAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Output file path
OUTPUT_VIDEO_PATH = "workspace/output/presentation.mp4"

# Ensure output folder exists
os.makedirs(os.path.dirname(OUTPUT_VIDEO_PATH), exist_ok=True)

def generate_video_task(input_file="input.txt"):
    """
    Runs the full pipeline in background with detailed logging.
    """
    try:
        logger.info("===== Video generation started =====")

        # Step 1: Read slides
        slides = InputAgent().run(input_file)
        logger.info(f"Slides processed: {len(slides)}")

        # Step 2: Plan slide flow
        plan = PlannerAgent().run(slides)
        logger.info(f"Slide plan created with {len(plan)} steps")

        # Step 3: Generate slide images
        images = SlideAgent().run(plan)
        logger.info(f"Generated {len(images)} slide images")

        # Step 4: Generate video and save to OUTPUT_VIDEO_PATH
        VideoAgent().run(images, plan, output_path=OUTPUT_VIDEO_PATH)
        logger.info(f"Video successfully saved to {OUTPUT_VIDEO_PATH}")

    except Exception as e:
        logger.exception(f"Video generation failed: {e}")

@app.post("/generate")
def generate(background_tasks: BackgroundTasks):
    """
    Starts video generation in background and returns immediately.
    """
    background_tasks.add_task(generate_video_task)
    return {"status": "Video generation started! Watch logs and check /download when done."}

@app.get("/download")
def download():
    """
    Returns the generated MP4 file if it exists.
    """
    if not os.path.exists(OUTPUT_VIDEO_PATH):
        return {"error": "Video not ready yet. Call /generate first."}

    return FileResponse(
        OUTPUT_VIDEO_PATH,
        media_type="video/mp4",
        filename="presentation.mp4"
    )

@app.get("/")
def home():
    return {"status": "AI Presentation Service is live!"}
