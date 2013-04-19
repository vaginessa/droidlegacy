#!/usr/bin/env python
#extracts features for each module
#features are based on calls to the android API

import os
import re
import sys
import os

#create dictionary mapping apks to modules to features
"for each apk"
familyDict = {}

for file in os.listdir("data/modules"):
	apkName = re.search('[^\.]*',file).group(0)
	familyDict.update({apkName:{}})
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
				#TODO tieBreaker of module is 0 for now.  Make a function to calculate this to break ties in similarity
				moduleDict={"classList":classList,"featureSet":featureSet,"tieBreaker":0}
				familyDict[apkName].update({moduleNum:moduleDict})

#figure out how many features there are
allFeatures = set()
modList = []
for apk in familyDict:
	for module in familyDict[apk]:
		allFeatures = allFeatures.union(familyDict[apk][module]["featureSet"])
		modList.append((apk,module))
allFeatures = list(allFeatures)

#output header
"""
header = "apkName,moduleNumber,"
for f in range(len(allFeatures)):
	header = header + allFeatures[f] + ","
print header[:-1]

#output feature vectors
for mod in modList:
	fVector = mod[0]+','+mod[1]+','
	for feature in allFeatures:
		if feature in familyDict[mod[0]][mod[1]]:
			fVector = fVector + "1,"
		else:
			fVector = fVector + "0,"
	print fVector[:-1]
"""

#Now that I've got the familyDictionary how do I best use it to find shared modules?
# the next line can be used to get the key mapping to the highest score
# key seems to be an option of max.  This takes a list of keys and evaluates them 
#for max by the values they map to instead of the keys themselves.  This could also do sorting.
#max(scoreTable.keys(), key=(lambda x: scoreTable[x]))
#I also need to detect and handle ties...
#sorted(scoreTable.items(), key=(lambda (k,v): v))
#the parameters to lambda represent each element of the list like in a map.

#we only want to run comparisons with the first apk as the source.  The others can be targets.


moduleToSimilarityScore = {}
#I need to compare one apk to the rest so I'm going to pop.  This will remove the popped element from familyDict
(chosenApkName,chosenApkDict) = familyDict.popitem()

def calcSimilarity(set1,set2):
	cardIntersect = len(set1.intersection(set2))
	cardUnion = len(set1.union(set2))
	return float(cardIntersect) / float(cardUnion)

for (chosenModuleKey,chosenModuleDict) in chosenApkDict.items():
	chosenFeatureSet=chosenModuleDict["featureSet"]
	moduleToSimilarityScore.update({chosenModuleKey:0})
	for apkDict in familyDict.values():
		#compare the chosenFeature set to all the featureSets in each module of this apk and get the highest score found.
		featureSetList = map ((lambda moduleDict: moduleDict["featureSet"]), apkDict.values()) 
		maxSimilarityScore = max(map ((lambda featureSet: calcSimilarity(chosenFeatureSet,featureSet)), featureSetList))
		moduleToSimilarityScore[chosenModuleKey] += maxSimilarityScore
		#print chosenModuleKey, moduleToSimilarityScore[chosenModuleKey]
	moduleToSimilarityScore[chosenModuleKey] /= len(familyDict)

#this sorted output is for testing.  I actually want max for the real system.
#how should I handle ties?  Should I combine them into one larger module?  That could interfere when comparing to new modules.
#keep both and search for either?
sortedScores = sorted(moduleToSimilarityScore.items(), key=(lambda (k,v): -v))
print chosenApkName
for score in sortedScores:
	print score
	repModule = chosenApkDict[score[0]]
	print repModule["classList"]
	print repModule["featureSet"]


#TODO I will need a way to go from module number to outputting which classes are in the module.  Another dictionary should work.

			
