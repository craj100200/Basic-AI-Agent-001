from agents.input_agent import InputAgent
from agents.planner_agent import PlannerAgent
from agents.slide_agent import SlideAgent
from agents.video_agent import VideoAgent


import os

os.makedirs("workspace/slides", exist_ok=True)
os.makedirs("workspace/output", exist_ok=True)



def main():
    slides = InputAgent().run("input.txt")
    plan = PlannerAgent().run(slides)
    images = SlideAgent().run(plan)
    output = VideoAgent().run(images, plan)
    print("VIDEO CREATED:", output)

if __name__ == "__main__":
    main()
