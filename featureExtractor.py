#!/usr/bin/env python
#extracts features for each module
#features are based on calls to the android API

import os
import re
import sys
import os
import ast

#I have no idea what these thresholds should actually be.
detectionThreshold = .8
signatureThreshold = .5
mode = sys.argv[1]

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

	for file in apkList:
		apkName = re.search('[^\.]*',file).group(0)
		batchDict.update({apkName:{}})
		apkData = open("data/modules/"+file).read().strip()
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
	for file in os.listdir("data/modules"):
		familyName = re.search('[^-]*',file).group(0)
		if familyName in collection:
			collection[familyName].append(file)
		else:
			collection.update({familyName:[file]})

	for family in collection:
		#create dictionary mapping apks to modules to features
		"for each apk"
		familyDict = extractFeatures(collection[family])

		#Find common code among instances of a family
		moduleToSimilarityScore = {}
		#I need to compare one apk to the rest so I'm going to pop.  This will remove the popped element from familyDict
		(chosenApkName,chosenApkDict) = familyDict.popitem()

		for (chosenModuleKey,chosenModuleDict) in chosenApkDict.items():
			chosenFeatureSet=chosenModuleDict["featureSet"]
			moduleToSimilarityScore.update({chosenModuleKey:{'score':0,'matchList':[chosenFeatureSet]}})
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

		signatureScores = {}
		signatureSet = set()
		for f_set in maxScoreSets:
			for f in f_set:
				if f in signatureScores:
					signatureScores[f] += 1
				else: 
					signatureScores.update({f:1})
		for f in signatureScores:
			signatureScores[f] /= len(maxScoreSets)
			if signatureScores[f] >= signatureThreshold:
				signatureSet = signatureSet.union(set([f]))
			
		sigFile = open("familySignatures/" + family+".sig",'w')
		for f in signatureSet:
			sigFile.write(f+"\n")

#given a group of apks look for the presence of a malware family's signature in any of them
def detectSignatures():
	fileList = os.listdir("data/modules")
	batchDictionary = extractFeatures(fileList)
	#make a dictionary for malicious signatures
	familySigDict = {}
	for file in os.listdir("familySignatures/"):
		#this should create a dictionary from the file data and load it into signature
		signature = set(open("familySignatures/"+file).read().strip().split("\n"))
		familyName = re.search('[^\.]*',file).group(0)
		familySigDict.update({familyName:signature})

	for (apkName,apkDict) in batchDictionary.items():
		for (moduleName,moduleDict) in apkDict.items():
			for (familyName, signature) in familySigDict.items():
				#I only need to do something if the signature or something close to it is detected
				similarityScore = calcSimilarity(moduleDict['featureSet'],signature)
				if similarityScore >= detectionThreshold:
					print "match detected in "+apkName+" for malware family: "+familyName
					print "classes involved are: " + str(moduleDict['classList'])
					print "similarity score of "+str(similarityScore)
					for f in signature:
						print f
				 

#main
if mode == "genSig":
	generateSignatures()
if mode == "detectSig":
	detectSignatures()
			
