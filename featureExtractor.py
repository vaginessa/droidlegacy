#!/usr/bin/env python
#extracts features for each module
#features are based on calls to the android API

import os
import re
import sys
import os

#create dictionary mapping apks to modules to features
"for each apk"
apkDict = {}
for file in os.listdir("data/modules"):
	apkName = re.search('[^\.]*',file).group(0)
	apkDict.update({apkName:{}})
	modData = open("data/modules/"+file).read().strip()
	modBlobs = modData.split("\n")
	
	modules = []
	for blob in modBlobs:
		module = blob.split(",")
		modules.append(module)

	#for each module in this apk
	for i in range(len(modules)):
		featureSet = set()
		outputName = apkName+"."+str(i)+".features"
		#for each class in the module
		for c in modules[i]:
			className = c.replace("/",".")
			prefix = "data/flatClasses/"+apkName+".classes/"
			classData = open(prefix+className).read()
			#look for all ".*, Landroid/.*;->.*\n
			#the weird symbols at the end of the line shouldn't hurt anything
			apiCalls = re.findall(', Landroid/.*;->',classData)
			apiCalls = [x.replace(", Landroid/","") for x in apiCalls]
			apiCalls = [x.replace(";->","") for x in apiCalls]
			apiCalls = set(apiCalls)
			#start unioning the results of patternmatching
			featureSet = featureSet.union(apiCalls)
			if len(featureSet) > 0:
				apkDict[apkName].update({str(i):featureSet})
		
#figure out how many features there are
allFeatures = set()
modList = []
for apk in apkDict:
	for module in apkDict[apk]:
		allFeatures = allFeatures.union(apkDict[apk][module])
		modList.append((apk,module))
allFeatures = list(allFeatures)

#output header
header = "apkName,moduleNumber,"
for f in range(len(allFeatures)):
	header = header + allFeatures[f] + ","
print header[:-1]

#output feature vectors
for mod in modList:
	fVector = mod[0]+','+mod[1]+','
	for feature in allFeatures:
		if feature in apkDict[mod[0]][mod[1]]:
			fVector = fVector + "1,"
		else:
			fVector = fVector + "0,"
	print fVector[:-1]



			
			