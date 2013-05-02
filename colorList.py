#!/usr/bin/env python
import copy
import Image


def createColorList():
	#remember to dedicate a color to false positives.  red maybe? or white?
	colorList = []
	for a in range(3):
		color = [0,0,0]
		color[a] = 1
		for b in range(3):
			color[(a+1)%3] = b
			for c in range(3):
				color[(a+2)%3] = c
				colorList.append(copy.deepcopy(color))
	return colorList

def csvToMatrix(fileName):
	f = open(fileName)
	f.readline()
	matrix = f.readlines()
	matrix = map(lambda x: map(lambda y: float(y), x.strip().split(',')[1:]), matrix)
	return matrix
	
def brightness(score, color):
	colorScores = map (lambda c : c * score, color)
	maxColorScore = max(colorScores)
	normalized = map (lambda c : int(c / maxColorScore * 256), colorScores)
	return normalized

def createImage()
	size = (len(matrix),len(matrix[0]))
	print size
	simImage = Image.new('RGB', size)
	 
	for row in range(len(matrix)):
		for col in range(len(matrix[row])):
			(r,g,b) = (brightness(.6,colorList[5]))
			simImage.putpixel((row,col), (r,g,b))

	simImage.save('myImage','PNG')
		
