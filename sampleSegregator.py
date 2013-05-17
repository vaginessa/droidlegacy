#!/usr/bin/env python
#separates

import os
import re
import sys
import random
import numpy

#trainingPercent = int(sys.argv[1]) / 100.0
fold = int(sys.argv[1])
folds = 10
#the second argument is the seed for random apk selection and should make experiment repeatable
#hash lets me use anything as a seed including strings.
#random.seed(hash(sys.argv[2]))

#make dictionary of family names to apk names
collection = {}
for apkName in os.listdir("toAnalyze"):
	familyName = re.search('[^-]*',apkName).group(0)
	if familyName in collection:
		collection[familyName].append(apkName)
	else:
		collection.update({familyName:[apkName]})

#use a seed and ratio to randomly segregate test samples from training samples
trainingList = []
testingList = []
for (familyName,apkList) in collection.items():
	#break apkList into ten equal parts
	#there is a problem with just rounding up chunkSize especially with small numbers
	#consider 16 elements and a chunkSize of 16 / 10 with ceiling.  You get a size
	#of 2 which runs out of elements before hitting 10 chunks...
	
	avg = len(apkList) / float(folds)
	out = []
	last = 0.0
	while last < len(apkList):
		out.append(apkList[int(last):int(last + avg)])
		last += avg
	chunks = out

	for i in range(folds):
		toAdd = chunks[i]
		print toAdd
		if i+1 == fold:
			testingList.extend(toAdd)
		else:
			trainingList.extend(toAdd)
	"""
	#calculate how many apks from each family will be used for training or testing
	trainingSize = int(len(apkList) * trainingPercent)
	#The system will fail if the training set is less than 2
	if trainingSize == 1:
		trainingSize = 2
	#There must be at least one apk left for the testing set
	if trainingSize == len(apkList):
		trainingSize = len(apkList) -1
	testSize = len(apkList) - trainingSize
	if trainingSize + testSize != len(apkList):
		print "ERROR IN TRAINING AND TEST SIZE"
	if len(apkList) < 3:
		print "NOT ENOUGH INSTANCES OF FAMILY "+familyName

	#seperate training from testing sets
	#random.shuffle(apkList)
	trainingList.extend(apkList[:trainingSize])
	testingList.extend(apkList[trainingSize:])
	"""	
#copy the apks to appropriate directories
for trainingApk in trainingList:
	os.system("cp toAnalyze/"+trainingApk+" trainingSet/")

for testingApk in testingList:
	os.system("cp toAnalyze/"+testingApk+" testingSet/")


