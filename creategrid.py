#!/usr/bin/env python3
from PIL import Image, ImageDraw
from itertools import cycle

# canvas Resolution
canvasWidth = 1920
canvasHeight = 1080

# LED Tile Parameters
tilePixelWidth = 104
tilePixelHeight = 104

# Array Configuration. Assume nonexisting tiles are included in the rectangle
columns = canvasWidth # tilePixelWidth
rows = canvasHeight # tilePixelHeight

# Colors to Alternate between
colors = ["orange", "green", "red", "blue", "yellow", "purple"]

# Check to see if the columns * tilePixelWidth is smaller than the canvasWidth
# Also check is the rows * tilePixelHeight is smaller than the canvasHeight
if (columns * tilePixelWidth) > canvasWidth:
        print("LED Array exceeds canvasWidth")
        quit()
if (rows * tilePixelHeight) > canvasHeight:
        print("LED Array exceeds canvasHeight")
        quit()



# newImage = Image.new('RGB', (tilePixelWidth * columns, tilePixelHeight * rows), color = 'white')
newImage = Image.new('RGB', (canvasWidth,  canvasHeight), color = 'white')
draw = ImageDraw.Draw(newImage)

# Set initial Color
# currentColor = color01
currentColor = cycle(colors)

# Let's shrink the variable names for uh... Line readability?
tpw = tilePixelWidth
tph = tilePixelHeight

for row in range(rows):
    for column in range(columns):
        draw.rectangle(((column*tpw,row*tph),((column*tpw+tpw)-1,(row*tph+tph)-1)), fill=next(currentColor))

    # This guards against column banding.
    if (columns % len(colors) == 0):
                print("jumping to next color to avoid banding")
                next(currentColor)

# create a filename
generatedFile = "grid - " + str(tilePixelWidth * columns) + "x" + str(tilePixelHeight * rows) + ".png"

newImage.save(generatedFile)

