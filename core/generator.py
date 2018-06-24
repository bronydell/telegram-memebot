# -*- coding: utf-8 -*-
import sys

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

PADDING = 20
FONT_NAME_LINUX = "/Library/Fonts/Impact.ttf"
FONT_NAME_WINDOWS = "impact.ttf"


def get_font(font_size):
    if sys.platform == 'win32':
        return ImageFont.truetype(FONT_NAME_WINDOWS, font_size)
    return ImageFont.truetype(FONT_NAME_LINUX, font_size)


def make_meme(top_string,
              bottom_string,
              filename,
              caps=False,
              font_scale=1.0):
    img = Image.open('images/in_' + str(filename) + '.jpg')
    image_size = img.size

    if caps:
        top_string = to_upper_case(top_string)
        bottom_string = to_upper_case(bottom_string)

    # find biggest font size that works
    font_size = int(image_size[1] / 8)
    font = get_font(font_size)
    top_text_size = font.getsize(top_string)
    bottom_text_size = font.getsize(bottom_string)
    while top_text_size[0] > image_size[0] - PADDING or bottom_text_size[0] > image_size[0] - PADDING:
        font_size = font_size - 1
        font = get_font(font_size)
        top_text_size = font.getsize(top_string)
        bottom_text_size = font.getsize(bottom_string)

    font_size = round(font_size * font_scale)
    font = get_font(font_size)
    top_text_size = font.getsize(top_string)
    bottom_text_size = font.getsize(bottom_string)
    # find top centered position for top text
    top_text_position_x = (image_size[0] / 2) - (top_text_size[0] / 2)
    top_text_position_y = 0
    top_text_position = (top_text_position_x, top_text_position_y)

    # find bottom centered position for bottom text
    bottom_text_position_x = (image_size[0] / 2) - (bottom_text_size[0] / 2)
    bottom_text_position_y = image_size[1] - bottom_text_size[1]
    bottom_text_position = (bottom_text_position_x, bottom_text_position_y - font_size / 6)

    draw = ImageDraw.Draw(img)

    outline_range = int(font_size * 0.1)

    for x in range(-outline_range, outline_range + 1):
        for y in range(-outline_range, outline_range + 1):
            draw.text((top_text_position[0] + x, top_text_position[1] + y), top_string, (0, 0, 0), font=font)
            draw.text((bottom_text_position[0] + x, bottom_text_position[1] + y), bottom_string, (0, 0, 0), font=font)

    draw.text(top_text_position, top_string, (255, 255, 255), font=font)
    draw.text(bottom_text_position, bottom_string, (255, 255, 255), font=font)
    output_filename = 'images/out_{}.jpg'.format(filename)
    img.save(output_filename)
    return output_filename


def to_upper_case(some_string):
    try:
        return some_string.decode("utf-8").upper()
    except:
        return some_string.upper()
