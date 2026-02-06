from PIL import Image, ImageDraw, ImageFont
import os

WIDTH, HEIGHT = 1280, 720
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (240, 240, 240)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def render_slide(title, bullets, index):

    os.makedirs("workspace/slides", exist_ok=true)

    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(FONT_PATH, 60)
    bullet_font = ImageFont.truetype(FONT_PATH, 38)

    draw.text((60, 50), title, fill=TEXT_COLOR, font=title_font)

    y = 160
    for bullet in bullets:
        draw.text((80, y), f"• {bullet}", fill=TEXT_COLOR, font=bullet_font)
        y += 55

    path = f"workspace/slides/slide_{index}.png"
    img.save(path)
    return path
