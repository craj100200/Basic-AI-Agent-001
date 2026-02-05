from tools.video_renderer import make_video

class VideoAgent:
    def run(self, images, plan):
        durations = [p["duration"] for p in plan]
        return make_video(images, durations)
