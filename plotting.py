from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
import csv
 
image = Image.open('kayal.png')
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('Roboto-Bold.ttf', size=10)
name = 'Ship'
color = 'rgb(255,255,0)'

with open('Final.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    next(reader)
    for row in reader:
        (x,y)=(int(row[2]),int(row[3]))
        draw.text((x,y), name, fill=color, font=font)

image.save('greeting_card.png')
