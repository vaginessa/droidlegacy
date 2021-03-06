#Copyright 2013 Software Research Lab, University of Louisiana at Lafayette
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


#!/usr/bin/env python
#extracts features for each module
#features are based on calls to the android API

import os
import re
import sys
import ast
import Image

#I have no idea what these thresholds should actually be.
signatureThreshold = .5
mode = sys.argv[1]
fold = sys.argv[2]

#returns jaccard similarity
def calcSimilarity(set1,set2):
	cardIntersect = len(set1.intersection(set2))
	cardUnion = len(set1.union(set2))
	return float(cardIntersect) / float(cardUnion)


#this sorted output is for testing.  I actually want max for the real system.
def printSortedScores(moduleToSimilarityScore,chosenApkName,chosenApkDict):
	sortedScores = sorted(moduleToSimilarityScore.items(), key=(lambda (k,v): -(v['score'])))
	print chosenApkName
	for score in sortedScores:
		print score[0],score[1]['score']
		repModule = chosenApkDict[score[0]]
		print repModule["classList"]

#creates a dictionary mapping apk names to modules to class lists and feature sets
def extractFeatures(apkList):
	batchDict = {}

	for file in sorted(apkList):
		print "extracting "+file
		apkName = re.search('[^\.]*',file).group(0)
		batchDict.update({apkName:{}})
		apkData = open("data/experimentData/modules/"+file).read().strip()
		modules = apkData.split("\n")

		for m in range(len(modules)):
			modules[m] = modules[m].split(",")

		#now modules is a list of modules which are lists of classes

		#for each module in this apk
		for i in range(len(modules)):
			moduleNum = str(i)
			featureSet = set()
			outputName = apkName+"."+moduleNum+".features"
			classList = modules[i]
			#for each class in the module
			for c in classList:
				className = c.replace("/",".")
				prefix = "data/flatClasses/"+apkName+".classes/"
				classData = open(prefix+className).read()
				#look for all ".*, Landroid/.*;->.*\n
				#the weird symbols at the end of the line shouldn't hurt anything
				apiCalls = re.findall(', Landroid/.*;->.*',classData)
				apiCalls = [x.replace(", L","") for x in apiCalls]
				apiCalls = set(apiCalls)
				#start unioning the results of patternmatching
				featureSet = featureSet.union(apiCalls)
				if len(featureSet) > 0:
					moduleDict={"classList":classList,"featureSet":featureSet}
					batchDict[apkName].update({moduleNum:moduleDict})

	return batchDict

def generateSignatures():
	#collection maps a family to apk's that belong to that family
	collection = {}
	for file in os.listdir("data/experimentData/modules"):
		familyName = re.search('[^-]*',file).group(0)
		if familyName in collection:
			collection[familyName].append(file)
		else:
			collection.update({familyName:[file]})

	for family in collection:
		print "Generate Signature: " + family
		#create dictionary mapping apks to modules to features
		"for each apk"
		familyDict = extractFeatures(collection[family])

		#familyDict should contain the classList which is accesible at 
		#the same level as featureSet on line 96

		#Find common code among instances of a family
		moduleToSimilarityScore = {}
		#I need to compare one apk to the rest so I'm going to pop.  This will remove the popped element from familyDict
		(chosenApkName,chosenApkDict) = familyDict.popitem()

		for (chosenModuleKey,chosenModuleDict) in chosenApkDict.items():
			chosenFeatureSet=chosenModuleDict["featureSet"]
			chosenClassList=chosenModuleDict["classList"]
			moduleToSimilarityScore.update({chosenModuleKey:{'score':0,'matchList':[chosenFeatureSet],'classList':[chosenClassList]}})
			for apkDict in familyDict.values():
				#compare the chosenFeature set to all the featureSets in each module of this apk and get the highest score found.
				featureSetList = map ((lambda moduleDict: moduleDict["featureSet"]), apkDict.values()) 
				scoresAndSets = map ((lambda featureSet: (calcSimilarity(chosenFeatureSet,featureSet),featureSet)), featureSetList)
				(maxSimilarityScore,matchFeatureSet) = max(scoresAndSets, key=(lambda (score,f_set): score))
				moduleToSimilarityScore[chosenModuleKey]['score'] += maxSimilarityScore
				moduleToSimilarityScore[chosenModuleKey]['matchList'].append(matchFeatureSet)
				#print chosenModuleKey, moduleToSimilarityScore[chosenModuleKey]
			moduleToSimilarityScore[chosenModuleKey]['score'] /= len(familyDict)

		maxScoreKey,maxScoreDict = max(moduleToSimilarityScore.items(), key=(lambda (k,v): v['score']))
		maxScoreSets = maxScoreDict['matchList']
		maxScoreClassList = maxScoreDict['classList']

		expFile = open("results/signatureExplanations_"+fold+"/"+family+".exp",'w')
		expFile.write("Apk used to create signature: " + chosenApkName + "\n")
		expFile.write(str(maxScoreClassList))

		signatureScores = {}
		signatureSet = set()
		for f_set in maxScoreSets:
			for f in f_set:
				if f in signatureScores:
					signatureScores[f] += 1
				else: 
					signatureScores.update({f:1})
		#normalize scores by dividing all of them by the maximum score instead of the average.  Then use the threshold.
		maxSigScore = float(max(signatureScores.values()))
		for f in signatureScores:
			signatureScores[f] /= maxSigScore
			if signatureScores[f] >= signatureThreshold:
				signatureSet = signatureSet.union(set([f]))
			
		sigFile = open("results/familySignatures_"+fold + "/" + family+".sig",'w')
		for f in signatureSet:
			sigFile.write(f+"\n")

#given a group of apks look for the presence of a malware family's signature in any of them
def detectSignatures():
	fileList = os.listdir("data/experimentData/modules")
	batchDictionary = extractFeatures(fileList)
	#make a dictionary for malicious signatures
	familySigDict = {}
	for file in os.listdir("results/familySignatures_"+fold+"/"):
		#this should create a dictionary from the file data and load it into signature
		signature = set(open("results/familySignatures_"+fold+"/"+file).read().strip().split("\n"))
		familyName = re.search('[^\.]*',file).group(0)
		familySigDict.update({familyName:signature})

	matchDict = {} #maps apks to their matchDict
	for familyName in familySigDict.keys(): #family names are listed here
		matchDict.update({familyName:{}})
	matchDict.update({"benign":{}})		

	for (apkName,apkDict) in batchDictionary.items():
		print "detecting "+apkName
		family = re.search('[^-]*',apkName).group(0) #this regular expression gets the family name but
		if family not in matchDict:
			family = "benign" #this will break if I get a malware family named benign
			apkName = "benign"+apkName
		#does not get the family for benign apps.  Where is the list of families created?
		matchDict[family].update({apkName:{}}) #maps apks to max matches of modules for each signature.
		
		for (familyName, signature) in familySigDict.items(): 
			moduleScoreList = []
			for (moduleName,moduleDict) in apkDict.items():
				#I need to find the highest scoring module for this signature and add it to the dictionary
				similarityScore = calcSimilarity(moduleDict['featureSet'],signature)
				moduleScoreList.append(similarityScore)
			maxModuleScore = max(moduleScoreList)
			matchDict[family][apkName].update({familyName:maxModuleScore})
	visualizeResults(matchDict,familySigDict)
	calculateAverages(matchDict,familySigDict)
				 

def createColorList(falseColor):
	colorList = []
	granularity = 4
	for r in range(granularity):
		for g in range(granularity):
			for b in range(granularity):
				maxColor = float(max([r,g,b]))
				if maxColor != 0:
					color = (r/maxColor,g/maxColor,b/maxColor)
					colorList.append(color)
	print len(colorList)
	colorList = list(set(colorList))
	colorList.remove(falseColor)
	print len(colorList)
	return colorList

def brightness(score, color):
	colorScores = map (lambda c : int(c * score * 256), color)
	return colorScores

def calculateAverages(resultDict,familySigDict):
	familyAverages = {}
	apkCount = 0

	#print header
	header = ""
	header += "apk,"
	for familyName in sorted(familySigDict.keys()):		
		header += familyName+","
	header = header [:-1]

	csvString = header + "\n"	

	#calculate counts and totals
	for (apkFamily,familyDict) in resultDict.items():
		#initialize family dictionary for averages
		familyAverages.update({apkFamily:{}})
		for (apkName,apkDict) in familyDict.items():
			#each apk has a score for each signature
			for (sigFamily,score) in apkDict.items():		
				if sigFamily in familyAverages[apkFamily]:
					familyAverages[apkFamily][sigFamily]["count"] += 1
					familyAverages[apkFamily][sigFamily]["totalScore"] += score
				else:
					familyAverages[apkFamily].update({sigFamily:{"count":1,"totalScore":score,"averageScore":0}})

	#calculate averages
	for (apkFamily,sigAveDict) in sorted(familyAverages.items(),key=(lambda (name,dict): name)):
		csvString += apkFamily + ","
		for (sigFamily,aveDict) in sorted(sigAveDict.items(),key=(lambda (name,dict): name)):
			count = familyAverages[apkFamily][sigFamily]["count"]
			total = familyAverages[apkFamily][sigFamily]["totalScore"]
			try:
				familyAverages[apkFamily][sigFamily]["averageScore"] = total / float(count)
			except ZeroDivisionError:
				familyAverages[apkFamily][sigFamily]["averageScore"]=0
			csvString += str(familyAverages[apkFamily][sigFamily]["averageScore"]) + ","
		csvString = csvString[:-1] + "\n"

	#output csv
	sigAveMatrix = open("results/csvData_"+str(fold)+"/SigAveMatrix.csv",'w')
	sigAveMatrix.write(csvString)

	
	#Print overall averages
	#print header
	header = "Family,IntraAverage,InterAverage"
	csvString = header + "\n"

	overInterCount = 0
	overIntraCount = 0
	overInterScore = 0
	overIntraScore = 0	
	for (apkFamily,sigAveDict) in sorted(familyAverages.items(),key=(lambda (name,dict): name)):
		interCount = 0
		intraCount = 0
		interScore = 0
		intraScore = 0
		for (sigFamily,aveDict) in sorted(sigAveDict.items(),key=(lambda (name,dict): name)):
			if sigFamily==apkFamily:
				overIntraCount += familyAverages[apkFamily][sigFamily]["count"]
				overIntraScore += familyAverages[apkFamily][sigFamily]["totalScore"]
				intraCount += familyAverages[apkFamily][sigFamily]["count"]
				intraScore += familyAverages[apkFamily][sigFamily]["totalScore"]
			else:
				overInterCount += familyAverages[apkFamily][sigFamily]["count"]
				overInterScore += familyAverages[apkFamily][sigFamily]["totalScore"]
				interCount += familyAverages[apkFamily][sigFamily]["count"]
				interScore += familyAverages[apkFamily][sigFamily]["totalScore"]
		try:
			intraAverage = intraScore / float(intraCount)
		except ZeroDivisionError:
			intraAverage = 0
		try:
			interAverage = interScore / float(interCount)
		except ZeroDivisionError:
			interAverage = 0
		csvString += apkFamily+","+str(intraAverage)+","+str(interAverage)+"\n"
	try:	
		overIntraAverage = overIntraScore / float(overIntraCount)
	except ZeroDivisionError:
		overIntraAverage =0
	try:
		overInterAverage = overInterScore / float(overInterCount)
	except ZeroDivisionError:
		overInterAverage = 0
	csvString += "\n\nOverall," + str(overIntraAverage) + "," + str(overInterAverage)+"\n"

	#output csv
	ovAveMatrix = open("results/csvData_"+fold+"/ovAveMatrix.csv",'w')
	ovAveMatrix.write(csvString)
			


#creates an apk to signature matrix that should provide an intuitive
#evaluation of our results.  We will need to tweak parameters until
#this program outputs a matrix with publishable results.
def visualizeResults(resultDict,familySigDict):
	#print header
	header = ""
	header += "apk,"
	for familyName in sorted(familySigDict.keys()):
		header += familyName+","
	header = header [:-1]

	#print data and produce image for evaluation

	falseColor = (1.0,0.0,0.0)
	colorList = createColorList(falseColor)

	print colorList
	imageMatrix = []

	csvString = header + "\n"	

	#for each family
	for (apkFamily,familyDict) in sorted(resultDict.items(),key=(lambda (name,dict): name)):
		familyNumber = sorted(resultDict.keys()).index(apkFamily)
		#for each apk
		for (apkName,apkDict) in sorted(familyDict.items(),key=(lambda (name,dict): name)):
			#update count in family dictionary for averages
			if apkFamily in familySigDict:
				csvString += apkName + ","
			else: 
				csvString += "benign" + apkName + ","
			imageRow = []
			for (sigFamily,score) in sorted(apkDict.items(),key=(lambda (name,score): name)):		
				if sigFamily==apkFamily:
					csvString += str(score) + ","
					imageRow.append(brightness(score,colorList[familyNumber]))
				else: #remember to dedicate a color to false positives such as red or white
					csvString += str(score) + ","
					imageRow.append(brightness(score,falseColor))
			csvString = csvString[:-1] + "\n"
			imageMatrix.append(imageRow)

	#output csv
	sigSimMatrix = open("results/csvData_"+fold+"/sigSimMatrix.csv",'w')
	sigSimMatrix.write(csvString)
	sigSimMatrix = open("results"+"/SigSimMatrix.csv",'a')
	csvString=csvString[csvString.find("\n")+1:]#csvString[2:]	
	sigSimMatrix.write(csvString)

	"""
	#create image with imageMatrix
	size = (len(imageMatrix),len(imageMatrix[0]))
	simImage = Image.new('RGB', size)
	for row in range(len(imageMatrix)):
		for col in range(len(imageMatrix[row])):
			(r,g,b) = (imageMatrix[row][col])
			simImage.putpixel((col,row), (r,g,b))
	simImage = simImage.resize((512,512))
	simImage.save('myImage.png','PNG')
	"""

#main
if mode == "genSig":
	generateSignatures()
if mode == "detectSig":
	detectSignatures()
			
