from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
import csv
# create Image object with the input image
 
image = Image.open('kayal.png')

draw = ImageDraw.Draw(image)

font = ImageFont.truetype('Roboto-Bold.ttf', size=45)
 
with open('Final.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    next(reader)
    for row in reader:
        lines=list()
        lines.append(row)
        a = str(row[2])
        b = str(row[3])
        (x, y) = (str(a), str(b))
        name = 'Ship'
        color = 'rgb(255,0,0)' 
        #rgb(255, 255, 255) white
        draw.text((str(a), str(b)), name, fill=color, font=font)

image.save('greeting_card.png')