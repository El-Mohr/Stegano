import os,sys
import Image
import numpy
import math
#import binascii
#import bitarray


def divideData(image,rawData,numberBits):
	if(numberBits > 8):
		print "Error: Number of bits should not be larger than 8"
	#print(len(rawData))
	#print(len(image))
	div = int(math.ceil(len(rawData) / (len(image)*numberBits*3.0)))
	#print(div)
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
	#print (blockedData)
	return blockedData
	

def mergeData(image,data,numberBits):
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
	allData = []
	for index in range(0,len(image)):
		tempPixel = list(image[index]) 
		allData.append(tempPixel[0] & ~(0xFF << numberBits))
		allData.append(tempPixel[1] & ~(0xFF << numberBits))
		allData.append(tempPixel[2] & ~(0xFF << numberBits))
	return allData


imageMat = Image.open("./../samples/sample1.png") #read the image, 8 bit per pixel
pixels = list(imageMat.getdata()) #the content of images (list of tupels)

stMsg = "hello world"
inputData=''
for x in stMsg:
	inputData=inputData+format(ord(x), 'b')

blockedData=divideData(pixels,inputData,2)
print bin(pixels[0][0]) + "  "  + bin(pixels[0][1]) + "  "+ bin(pixels[0][2]) #checking before
imageHidden =  mergeData(pixels,blockedData[0],2) #call the function that merges the data , Should be iterated if data is large

image_out = Image.new(imageMat.mode,imageMat.size)
image_out.putdata(imageHidden)
image_out.save('../outputs/out1.png')

modImageMat = Image.open("./../outputs/out1.png") #read the image, 8 bit per pixel
modPixels = list(modImageMat.getdata()) #the content of images (list of tupels)
print bin(modPixels[0][0]) + "  "  + bin(modPixels[0][1]) + "  "+ bin(modPixels[0][2]) #checking after 
imageData = getData(modPixels,2)
#print imageData

