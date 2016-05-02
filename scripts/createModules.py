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
#numpy helps with matrix operations
import numpy
#sys is used to handle command line arguments
import sys
import copy

np=numpy
inputFile = sys.argv[1]
#inputFile = "/home/lad9344/Android_Malware_Classifier/ADRD Test/pdg/ADRD-100.e.csv"
#the threshold determines when to stop mergin classes.
#If there are no class relationships above 5 then stop combining classes.
threshold = 5

#converts edge list to a dependence matrix
def edge2Matrix(inputFile):
	edgeData=open(inputFile).read().strip()
	edgeList=edgeData.split("\n")
	edges=[]
	for edge in edgeList:
		nextEdge=edge.split(",")
		#each edge is a list of three elements separated by commas
		#source,target,weight for example A,B,8
		edges.append(nextEdge)

	moduleList=[]
	for edge in edges:
		#Convert list of three elements to three variables	
		source,target,weight=edge
		moduleList.append(source)
		moduleList.append(target)
	#each source and target has been added to the module list.
	#there are probably duplicates, so the list is converted to a set and back to a list
	#since a list can't contain duplicates, this eliminates them from the moduleList
	moduleList=list(set(moduleList))

	numClasses=len(moduleList)
	#start with a matrix of the right size full of zeros
	depMatrix=np.zeros((numClasses,numClasses),dtype=numpy.int)

	#populate the dependence matrix with data from the edgeList
	for edge in edges:
		source,target,weight=edge
		row=moduleList.index(source)
		col=moduleList.index(target)
		depMatrix[row][col]=int(weight)
	
	#adding the transpose makes the directed dependence graph into and undirected one.
	depMatrix=depMatrix + np.transpose(depMatrix)

	#having classes with dependence on themselves causes problems, so this is set to zero
	for i in range(numClasses):
		depMatrix[i,i]=0

	#each element of the moduleList should be a list containing a single class.
	for i in range(len(moduleList)):
		moduleList[i]=[moduleList[i]]
	
	return depMatrix,moduleList

#finds modules within a Matrix given some threshold
def clusterMatrix(depMatrix,moduleList,threshold):
	#until there are no dependence relations stronger than the threshold keep combining modules
	while(True):	
		#find the strongest dependence relationship in the matrix
		maxDependence=np.amax(depMatrix)
		if maxDependence<threshold:
			break
		maxSource=np.where(depMatrix==maxDependence)[0][0]
		maxTarget=np.where(depMatrix==maxDependence)[1][0]

		if depMatrix[maxSource][maxTarget] != maxDependence:
			print "We have a problem!"
			break

		#combine the modules in the list of classes
		#keep the source remove the target
		moduleList[maxSource]=moduleList[maxTarget]+moduleList[maxSource]
		del moduleList[maxTarget]

		col1=depMatrix[:,maxSource]
		col2=depMatrix[:,maxTarget]

		row1=depMatrix[maxSource,:]
		row2=depMatrix[maxTarget,:]

		#adding these two columns combines the edges associated with the modules being combined
		#if A and B are combined and A,C,2 and B,C,2 then AB,C,4

		#print depMatrix

		depMatrix[:,maxSource]=col1+col2
		depMatrix[maxSource,:]=row1+row2

		#print depMatrix
		
		#This line deletes the target column where the maximum similarity was found
		depMatrix=numpy.delete(depMatrix, (maxTarget), axis=1)

		#axis represents the dimension (row or column).
		#axis 0 is rows, axis 1 is columns
		#This line deletes the source row where the maximum similarity was found
		depMatrix=numpy.delete(depMatrix, (maxTarget), axis=0)

		#print depMatrix
		
		#keep making sure the dependence of a class on itself is 0
		for i in range(depMatrix.shape[0]):
			depMatrix[i,i]=0

		#print depMatrix

	printModules(moduleList)

#prints the moduleList in a readable, intuitive manner
def printModules(moduleList):
	for module in moduleList:
		for c in range(len(module)):
			if c == len(module) - 1:
				print module[c]
			else:
				sys.stdout.write(module[c]+',')

#outputs the matrix in a simple format with one row per line.
def printMatrix(depMatrix):
	numClasses=depMatrix.shape[0]
	for i in range(numClasses):
		for j in range(numClasses):	
			if j==(numClasses-1):
				print depMatrix[i,j]
			else:
				print depMatrix[i,j],


#This is my attempt to look professional by using functions
depMatrix,moduleList = edge2Matrix(inputFile)
#printMatrix(depMatrix)
clusterMatrix(depMatrix, moduleList, threshold)


	

