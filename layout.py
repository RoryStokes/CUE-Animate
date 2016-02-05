import numpy
from PIL import Image
import sys, os
from cue_sdk import *
import tkinter

try:
	cuesdk = r"{}\bin\i386\CUESDK_2013.dll".format(os.environ["CUESDK"])
except KeyError: 
   print("Please set the environment variable CUESDK to the location of the SDK")
   sys.exit(1)

while True:
	try:
		sdk = CUE(cuesdk)
		sdk.RequestControl(CAM_ExclusiveLightingControl)
		break
	except cue_exceptions.ServerNotFound:
		print("Error: This script requires CUE to be currently running. Retrying in 5s")
		time.sleep(5)


numKeys = sdk.GetLedPositions()[0].numberOfLed;
keys = sdk.GetLedPositions()[0].pLedPosition
top = keys[0].top
bottom = keys[0].top - keys[0].height
left = keys[0].left
right = keys[0].left + keys[0].width

for i in range(1,numKeys):
	top = max(top,keys[i].top)
	bottom = min(bottom,keys[i].top - keys[i].height)
	left = min(left,keys[i].left)
	right = max(right,keys[i].left + keys[i].width)

width = int(right-left)
height = int(top-bottom)

def create(sourceImage):
	if sourceImage.size != (width,height):
		print("Image dimensions do not match keyboard dimensions (should be {}x{}). Resizing to fit.".format(width,height))
		
		sourceImage = sourceImage.resize((width,height), Image.ANTIALIAS)

	source =  numpy.asarray(sourceImage)[:,:,:3]

	keyMap = numpy.empty((numKeys,3),dtype="uint8")

	for i in range(numKeys):
		key = keys[i]
		subLeft = int(key.left-left)
		subRight = int(subLeft+key.width)
		subTop = int(key.top)
		subBottom = int(subTop+key.height)
		subImage = source[ subTop:subBottom , subLeft:subRight , :]
		colour = numpy.average(subImage,(0,1))
		keyMap[i] = colour.astype(int)

	return keyMap

if __name__ == '__main__':
	if len(sys.argv)<3:
		print("Usage: python layout.py input output")
		sys.exit()

	sourceImage = Image.open(sys.argv[1])
	layout = create(sourceImage)
	im = Image.fromarray(layout.reshape(1,layout.numKeys,3), mode="RGB")
	im.save(sys.argv[2],"PNG")
