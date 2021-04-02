#! /usr/bin/env python3
"""
Create a new image for use as a
watermark and save it to disk.
"""
from PIL import Image, ImageDraw, ImageFont

image = Image.new('RGBA', (1920, 1080), color = (255, 0, 0, 0))
width, height = image.size

draw = ImageDraw.Draw(image)
text = "Mock Data Text"

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
image.save('images/watermark.png')
