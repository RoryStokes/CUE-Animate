import sys
import numpy
from cue_sdk import *
from PIL import Image,ImageEnhance
import time
import ctypes

cuesdk = r"C:\Program Files (x86)\Corsair\Corsair Utility Engine\CUESDK\bin\i386\CUESDK_2013.dll"
while True:
	try:
		sdk = CUE(cuesdk)
		sdk.RequestControl(CAM_ExclusiveLightingControl)
		break
	except cue_exceptions.ServerNotFound:
		print("Error: This script requires CUE to be currently running. Retrying in 5s")
		time.sleep(5)
#device = sdk.device(0)

if len(sys.argv)==1:
	print("Usage: python display.py path_to_target [fps]")
	sys.exit()


ledFrames = []

with Image.open(sys.argv[1]) as image:

	image = ImageEnhance.Color(image).enhance(1.2)
	image = ImageEnhance.Contrast(image).enhance(1.2)

	keys = sdk.GetLedPositions()[0].pLedPosition
	print("Loaded image '{}'".format(sys.argv[1]))
	print("{} frames".format(image.size[1]))

	colours = numpy.asarray(image)
	colours = colours[:,:,:3]

	if colours.shape[0] == 1:
		sleepTime = 5
	elif len(sys.argv)>2:
		sleepTime = 1.0/int(sys.argv[2])
	else:
		sleepTime = 0.1

	ledCount = sdk.GetLedPositions()[0].numberOfLed;
	for frame in range(colours.shape[0]):
		ledFrame = []
		for i in range(ledCount):
			ledFrame.append(CorsairLedColor(keys[i].ledId,*colours[frame,i,:]))

		cLedArray = (CorsairLedColor * len(ledFrame))(*ledFrame)
		ledFrames.append(cLedArray)
	cLedArray=None

Image = None
ImageEnhance = None
numpy = None
colours = None
ctypes = None

while True:
	for ledFrame in ledFrames:
		sdk.SetLedsColorsAsync(ledCount,ledFrame)
		time.sleep(sleepTime)


input()