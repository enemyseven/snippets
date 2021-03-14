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
font = ImageFont.truetype('HelveticaNeue.ttc', 82)
textwidth, textheight = draw.textsize(text, font)

margin = 10
x = width - textwidth - margin
y = height - textheight - margin

# Finally draw the watermark in the bttom right corner
draw.text((x,y), text, font=font, fill=(220,220,220,255))
# Open temporary file
image.show()

# Show mode info
print("Mode: ", image.mode)

# Save watermarked Image
image.save('images/watermark.png')
