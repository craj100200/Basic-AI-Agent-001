from presentation_agent.tools.slide_renderer import render_slide

class SlideAgent:
    def run(self, plan):
        images = []
        for i, slide in enumerate(plan):
            images.append(
                render_slide(slide["title"], slide["bullets"], i)
            )
        return images
