#!/usr/bin/env python3
import argparse
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky.auto import auto

try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")
parser = argparse.ArgumentParser()
parser.add_argument('--weight', type=str, required=True, help="Gewicht")
parser.add_argument('--kind', type=str, required=True, help="kind of waste")
args, _ = parser.parse_known_args()
img = Image.new("P", inky_display.resolution)
draw = ImageDraw.Draw(img)
intuitive_font = ImageFont.truetype(Intuitive, int(60))
hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(32))
weight = args.weight
kind = args.kind
y_top = int(inky_display.height * (3.0 / 10.0))
y_bottom = y_top + int(inky_display.height * (7.0 / 10.0))
for y in range(0, y_top):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.BLACK) 
for y in range(y_top, y_bottom):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.WHITE)

# Calculate the positioning and draw the "kind" text
kind_w, kind_h = hanken_bold_font.getsize(kind)
kind_x = int((inky_display.width - kind_w) / 2)
kind_y = 0 
draw.text((kind_x, kind_y), kind, inky_display.WHITE, font=hanken_bold_font)

# Calculate the positioning and draw the weight text
weight_w, weight_h = intuitive_font.getsize(weight)
weight_x = int((inky_display.width - weight_w) / 2)
weight_y = int(y_top + ((y_bottom - y_top - weight_h) / 2))
draw.text((weight_x, weight_y), weight, inky_display.BLACK, font=intuitive_font)

# Display the completed weight badge
inky_display.set_image(img)
inky_display.show()
