#!/usr/bin/env python
#numpy helps with matrix operations
import numpy
#sys is used to handle command line arguments
import sys

np=numpy
inputFile = sys.argv[1]
#the threshold determines when to stop mergin classes.
#If there are no class relationships above 5 then stop combining classes.
threshold = 5

#converts edge list to a dependenct matrix
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
		depMatrix[row][col]=weight
	
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

		#axis represents the dimension (row or column).
		#axis 0 is rows, axis 1 is columns
		#This line deletes the source row where the maximum similarity was found
		nextdepMatrix=numpy.delete(depMatrix, (maxSource), axis=0)
		
		col1=nextdepMatrix[:,maxSource]
		col2=nextdepMatrix[:,maxTarget]

		#adding these two columns combines the edges associated with the modules being combined
		#if A and B are combined and A,C,2 and B,C,2 then AB,C,4
		nextdepMatrix[:,maxTarget]=col1+col2
		
		#This line deletes the source column where the maximum similarity was found
		nextdepMatrix=numpy.delete(nextdepMatrix, (maxSource), axis=1)
		
		#combine the modules in the list of classes
		moduleList[maxTarget]=moduleList[maxTarget]+moduleList[maxSource]
		del moduleList[maxSource]
		
		#keep making sure the dependence of a class on itself is 0
		for i in range(nextdepMatrix.shape[0]):
			nextdepMatrix[i,i]=0

		depMatrix=nextdepMatrix		

	printModules(moduleList)

#prints the moduleList in a readable, intuitive manner
def printModules(moduleList):
	for module in moduleList:
		for c in module:
			print c,
		print ""
		print ""

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
clusterMatrix(depMatrix, moduleList, threshold)


	

