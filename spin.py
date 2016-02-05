from PIL import Image,ImageOps,ImageTk
import sys
import layout
import numpy


if len(sys.argv)<3:
	print("Usage: python spin.py input output [frames]")
	sys.exit()

if len(sys.argv)>3:
	step = 360/int(sys.argv[3])
else:
	step = 1

image = Image.open(sys.argv[1])

ratio = 700.0/min(image.size)
newSize = (int(ratio*image.size[0]),int(ratio*image.size[1]))

image = image.resize(newSize, Image.ANTIALIAS)

print(image.size)
rows = []
for angle in numpy.arange(0,360,step):
	rotated = image.rotate(angle)
	width, height = rotated.size
	centreX = int(width/2)
	centreY = int(height/2)
	left = centreX - int(layout.width/2)
	top = centreY - int(layout.height/2)
	right = centreX + int((layout.width+1)/2)
	bottom = centreY + int((layout.height+1)/2)
	cropped = rotated.crop((left,top,right,bottom))
	rows.append(layout.create(cropped))

map = numpy.vstack(rows)
im = Image.fromarray(map.reshape(len(rows),layout.numKeys,3), mode="RGB")
im.save(sys.argv[2],"PNG")