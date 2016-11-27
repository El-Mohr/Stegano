import os,sys
import Image
import numpy

def mergeData(image,data,numberBits):
	if(numberBits > 8):
		print "Error: number of bits should not be larger than 8"
	if(len(data)>(len(image)*numberBits*3)):
		print "Too much data to hide!!"
	for index in range(0,len(image)-1):
		tempPixel = list(image[index]) # convert to list to be able to change it
		tempPixel[0] = (tempPixel[2] &0xFF << numberBits) | 1
		tempPixel[1] = (tempPixel[2] & 0xFF << numberBits) | 2
		tempPixel[2] = (tempPixel[2] & 0xFF << numberBits) | 3
		image[index] = tuple(tempPixel) #right the data
	return image

def getData(image,numberBits):
	allData = [0]
	for index in range(0,len(image)-1):
		tempPixel = list(image[index]) 
		allData.append(tempPixel[0] & ~(0xFF << numberBits))
		allData.append(tempPixel[1] & ~(0xFF << numberBits))
		allData.append(tempPixel[2] & ~(0xFF << numberBits))
	return allData

imageMat = Image.open("./../samples/sample1.png") #read the image, 8 bit per pixel
pixels = list(imageMat.getdata()) #the content of images (list of tupels)
print bin(pixels[30000][0]) + "  "  + bin(pixels[30000][1]) + "  "+ bin(pixels[30000][2]) #checking before
imageHidden =  mergeData(pixels,[1, 1, 1],2) #call the function that merges the data 
print bin(pixels[30000][0]) + "  "  + bin(pixels[30000][1]) + "  "+ bin(pixels[30000][2]) #checking after 
imageData = getData(imageHidden,2)
print imageData

