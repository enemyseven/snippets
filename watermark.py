#! /usr/bin/env python3
"""
Create a new image for use as a
watermark and save it to disk.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def setup():
    # Check to see if directory exists.
    if not os.path.isdir("watermarks"):
        # If not create it.
        os.makedirs("watermarks")

def make_watermark(text):
    image = Image.new('RGBA', (1920, 1080), color = (255, 0, 0, 0))
    width, height = image.size

    draw = ImageDraw.Draw(image)

    # Set Font parameters
    font = ImageFont.truetype('HelveticaNeue.ttc', 108, 1)
    textwidth, textheight = draw.textsize(text, font)

    margin = 0
    x = (width - textwidth) / 2 # - Centered
    y = (height - textheight) / 2 - 339 # - Centered

    # Finally draw the watermark in the bttom right corner
    draw.text((x,y), text, font=font, fill=(12,32,116,255))
    # Open temporary file
    image.show()

    # Show mode info
    print("Mode: ", image.mode)

    # Save watermarked Image
    image.save('watermarks/watermark.png')

def main():
    setup()
    
    name = "Esmerelda Gillespie" + "\'s"
    make_watermark(name)

if __name__ == "__main__":
    # execcute only if run as a script
    main()
