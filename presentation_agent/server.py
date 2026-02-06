# server.py
import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse

# ✅ Full package imports for Render
from presentation_agent.agents.input_agent import InputAgent
from presentation_agent.agents.planner_agent import PlannerAgent
from presentation_agent.agents.slide_agent import SlideAgent
from presentation_agent.agents.video_agent import VideoAgent

app = FastAPI()

# Output file path
OUTPUT_VIDEO_PATH = "workspace/output/presentation.mp4"

# Ensure workspace/output exists
os.makedirs(os.path.dirname(OUTPUT_VIDEO_PATH), exist_ok=True)

def generate_video_task(input_file="input.txt"):
    """
    The heavy video generation pipeline.
    Runs in background.
    """
    # Step 1: Read slides from input file
    slides = InputAgent().run(input_file)
    
    # Step 2: Plan slide flow
    plan = PlannerAgent().run(slides)
    
    # Step 3: Generate images for slides
    images = SlideAgent().run(plan)
    
    # Step 4: Generate final video
    VideoAgent().run(images, plan, output_path=OUTPUT_VIDEO_PATH)

@app.post("/generate")
def generate(background_tasks: BackgroundTasks):
    """
    Starts video generation in the background.
    Returns immediately to avoid 502 timeout.
    """
    background_tasks.add_task(generate_video_task)
    return {"status": "Video generation started! Check /download when done."}

@app.get("/download")
def download():
    """
    Downloads the generated MP4 video.
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
