from tools.text_parser import parse_slides

class InputAgent:
    def run(self, path):
        return parse_slides(path)
