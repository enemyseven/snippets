#! /usr/bin/env python3
"""
Create a new image for use as a
watermark and save it to disk.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def setup():
    # Check to see if directory exists.
    if not os.path.isdir("watermark-images"):
        # If not create it.
        os.makedirs("watermark-images")

def make_watermark(text, filepath):
    scale = 1
    image = Image.new('RGBA', (1920 * scale, 1080 * scale), color = (255, 0, 0, 0))
    width, height = image.size

    draw = ImageDraw.Draw(image)
    draw.fontmode = "L"

    # Set Font parameters
    if len(text) > 22:
        fontsize = 90
    else:
        fontsize = 108
    font = ImageFont.truetype('HelveticaNeue.ttc', fontsize * scale, 1)
    textwidth, textheight = draw.textsize(text, font)

    margin = 0
    x = (width - textwidth) / 2 # - Centered
    y = (height - textheight) / 2 - (339 * scale) # - Centered

    # Finally draw the watermark in the bttom right corner
    draw.text((x,y), text, font=font, fill=(12,32,116,255))
    
    image_resized = image.resize((1280,720), Image.LANCZOS)
    
    # only do this if running as a script
    if __name__ == "__main__":
        # Open temporary file
        image.show()

        # Show mode info
        print("Mode: ", image.mode)
    else:
        # Save watermarked Image
        image_resized.save(filepath)

def main():
    setup()
    
    text = "Esmerelda Gillespie" + "\'s"
    filepath = "./watermark-images/watermark_test.png"
    make_watermark(text, filepath)

if __name__ == "__main__":
    # execcute only if run as a script
    main()
