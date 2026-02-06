import os
from fastapi import FastAPI
from agents.input_agent import InputAgent
from agents.planner_agent import PlannerAgent
from agents.slide_agent import SlideAgent
from agents.video_agent import VideoAgent

app = FastAPI()

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/generate")
def generate():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "input.txt")

    slides = InputAgent().run(input_file)
    plan = PlannerAgent().run(slides)
    images = SlideAgent().run(plan)
    output = VideoAgent().run(images, plan)

    return {"video": output}
