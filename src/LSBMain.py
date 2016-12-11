import os,sys
import Image
import numpy
import math


def divideData(image,rawData,numberBits):
	if(numberBits > 8):
		print "Error: Number of bits should not be larger than 8"
	div = int(math.ceil(len(rawData) / (len(image)*numberBits*3.0)))
	blockedData = [[[0 for x in range(3)] for y in range(len(image))] for z in range(div)] 
	i=0	
	for index in range(div):
		for pixel in range(len(image)):
			for color in range(3):
				tempData=b''
				for bit in range(numberBits):
					if(i<len(rawData)):
						tempData = tempData + rawData[i]
					else:
						tempData = tempData + b'0'
					i= i + 1
				blockedData[index][pixel][color] = tempData	
	return blockedData
	

def hideData(image,data,numberBits):
	if(numberBits > 8):
		print "Error: Number of bits should not be larger than 8"
	if(len(data)>(len(image))):
		print "Error: Too much data to hide!!"
	for index in range(0,len(image)):
		tempPixel = list(image[index]) # convert to list to be able to change it
		tempPixel[0] = (tempPixel[0] & 0xFF << numberBits) | int(data[index][0],2)
		tempPixel[1] = (tempPixel[1] & 0xFF << numberBits) | int(data[index][1],2)
		tempPixel[2] = (tempPixel[2] & 0xFF << numberBits) | int(data[index][2],2)
		image[index] = tuple(tempPixel) #right the data
	return image


def getData(image,numberBits):
	allData = ''
	for index in range(0,len(image)):
		tempPixel = list(image[index]) 
		allData=allData+(format(int(tempPixel[0] & ~(0xFF << numberBits)), 'b').zfill(numberBits))
		allData=allData+(format(int(tempPixel[1] & ~(0xFF << numberBits)), 'b').zfill(numberBits))
		allData=allData+(format(int(tempPixel[2] & ~(0xFF << numberBits)), 'b').zfill(numberBits))
	return allData





############Encoding message in image###############
stMsg = "hello world"
for i in range(200000) :
	stMsg = stMsg + 'x'
#print stMsg
inputData=''
for x in stMsg:
	inputData=inputData+format(ord(x), 'b').zfill(8)

imageMat = Image.open("./../samples/sample1.png") #read the image, 8 bit per pixel
pixels = list(imageMat.getdata()) #the content of images (list of tupels)

blockedData=divideData(pixels,inputData,2)
for div in range(len(blockedData)):
	imageHidden =  hideData(pixels,blockedData[div],2) #call the function that merges the data
	image_out = Image.new(imageMat.mode,imageMat.size)
	image_out.putdata(imageHidden)
	image_out.save('../outputs/out%d.png' % div)




##########Decoding modified Image#############
modImageMat = Image.open("./../outputs/out0.png") #read the image, 8 bit per pixel
modPixels = list(modImageMat.getdata()) #the content of images (list of tupels)
imageData = getData(modPixels,2)

msg=''
for bit in range(0,len(imageData),8):
	msg = msg + chr(int(imageData[bit:bit+8], 2))

print msg
