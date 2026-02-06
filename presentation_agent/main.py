




from presentation_agent.agents.input_agent import InputAgent
from presentation_agent.agents.planner_agent import PlannerAgent
from presentation_agent.agents.slide_agent import SlideAgent
from presentation_agent.agents.video_agent import VideoAgent


import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


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
