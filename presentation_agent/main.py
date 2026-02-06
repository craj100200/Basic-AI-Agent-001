from agents.input_agent import InputAgent
from agents.planner_agent import PlannerAgent
from agents.slide_agent import SlideAgent
from agents.video_agent import VideoAgent


import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "input.txt")

os.makedirs(os.path.join(BASE_DIR, "workspace/slides"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "workspace/output"), exist_ok=True)



def main():
    slides = InputAgent().run(INPUT_FILE)
    plan = PlannerAgent().run(slides)
    images = SlideAgent().run(plan)
    output = VideoAgent().run(images, plan)
    print("VIDEO CREATED:", output)

if __name__ == "__main__":
    main()
