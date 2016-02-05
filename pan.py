from PIL import Image,ImageOps,ImageTk
import sys
import layout
import numpy


if len(sys.argv)<3:
	print("Usage: python pan.py input output [frames]")
	sys.exit()

if len(sys.argv)>3:
	step = 360/int(sys.argv[3])
else:
	step = 1

image = Image.open(sys.argv[1])

ratio = 220.0/image.size[1]
width = int(ratio*image.size[0])

image = image.resize((width,layout.height), Image.ANTIALIAS)

copies = int(layout.width/width) + 2

fullImage = Image.new('RGB',(copies*width,220))
for i in range(copies):
	fullImage.paste(image,(i*width,0))

rows = []
for offset in range(0,width,step):
	left = offset
	top = 0
	right = offset+layout.width
	bottom = layout.height
	cropped = fullImage.crop((left,top,right,bottom))
	print(cropped.size)
	rows.append(layout.create(cropped))

map = numpy.vstack(rows)
im = Image.fromarray(map.reshape(len(rows),layout.numKeys,3), mode="RGB")
im.save(sys.argv[2],"PNG")