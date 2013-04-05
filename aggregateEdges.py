#!/usr/bin/env python
#takes a list of edges and combines the weights of matching edges for a simpler list.
#also removes edges involving classes outside the APK

#sys is used to handle command line arguments
import sys

#inputFile is an unfiltered list of edges containing redundant information and connections to classes outside of the APK
inputFile = sys.argv[1]
#list of classes in the APK
classListFile = sys.argv[2]

def aggEdges(inputFile,classListFile):
	#create a list of classes in the APK
	classData=open(classListFile).read().strip()
	classList=classData.split("\n")
	
	#extract edges from inputFile
	edgeData=open(inputFile).read().strip()
	edgeList=edgeData.split("\n")
	edges=[]
	edgeDictionary={}
	for edge in edgeList:
		edge=edge.split(",")
		#extract source,target, and weight from each edge
		source,target,weight=edge
		weight = int(weight)
		#make sure the classes involved are actually in the APK
		if target in classList:
			#check if source and target are already in dictionary
			#If source is in the dictionary
			if edgeDictionary.has_key(source):
				#If target is in dictionary
				if edgeDictionary[source].has_key(target):
					#add the edges weight to the appropriate dictionary entry
					edgeDictionary[source][target] = edgeDictionary[source][target] + weight
				#source is in dictionary, but target is not
				else:
					#add the target with it's weight to the source's dictionary
					edgeDictionary[source].update({target:weight})
			#Neither are in the dictionary
			else:
				#Add the source to the dictionary
				edgeDictionary.update({source:{}})
				#Add the target and associated weight to the source's dictionary
				#The edgeDictionary is a dictionary of dictionaries that map to weights.
				edgeDictionary[source].update({target:weight})
	
	#output the dictionaries as a readable edgelist formatted as source,target,weight
	for source in edgeDictionary:
		for target in edgeDictionary[source]:
			print source + "," + target + "," + str(edgeDictionary[source][target])

aggEdges(inputFile,classListFile)
