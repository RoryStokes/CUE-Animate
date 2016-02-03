import sys
import numpy
from cuepy import CorsairSDK
from PIL import Image,ImageOps
from defs import *


sdk = CorsairSDK(cuesdk)
device = sdk.device(0)

print(sys.argv)
if len(sys.argv)==1:
	print("Usage: python main.py path_to_target")
	sys.exit()

sourceImage = Image.open(sys.argv[1])
if(sourceImage.size != (660,220)):
	print("Image has incorrect dimensions (should be 660x220). Resizing to fit.")
	
	sourceImage = sourceImage.resize((660,220), Image.ANTIALIAS)

source =  numpy.asarray(sourceImage)
source = source.reshape(145200,source.shape[2])
source = source[:,:3]
display = Image.new("RGB", (660,220),"black")

print('ready')


for key in keys:
	maskImage = Image.open(maskFormat.format(key))
	mask = numpy.asarray(maskImage).flatten()
	colour = numpy.average(source,0,mask)
	device.set_led(key,colour.astype(int))
	colourImage = Image.new("RGB", (660,220),tuple(colour.astype(int)))
	display = Image.composite(colourImage,display,maskImage)

#display.show()
#display.save("keyboard.png","PNG")

input()