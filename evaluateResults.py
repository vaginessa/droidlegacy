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
#Input: big csv file, threshold
#Output: Single Classifier confusion Matrix 

import os
import re
import sys
import ast
from decimal import *

inpfile=sys.argv[1]			#path to csv file
#thresholds=sys.argv[2]		#threshold value

def getmatrix(inpfile):
	thresholds=[0.5,0.6,0.7,0.8,0.9,0.98]
	"""	
	i=0.4
	while(i<1.0):
		i=i+0.02
		thresholds.append(i)
	"""	
	#print sc headers
	print "thresholds used:"
	print thresholds
	print "\nfamilies detected:"
	file=open(inpfile,"r")
	#get list of all families
	families=((file.readline()).strip()).split(",")
	families.remove(families[0])
	x=len(families)
	y=len(thresholds)
	sc=[None]*x
	x=0
	for family in families:
		print family	
		sc[x]=[None]*10
		sc[x][0]=family
		sc[x][1]=[0]*y	#tp
		sc[x][2]=[0]*y	#tn
		sc[x][3]=[0]*y	#fp
		sc[x][4]=[0]*y	#fn
		sc[x][5]=[0]*y	#Precision
		sc[x][6]=[0]*y	#recall
		sc[x][7]=[0]*y	#TNR (true Negative Rate)
		sc[x][8]=[0]*y	#Accuracy
		sc[x][9]=[0]*y	#1- FPrate
		x=x+1


	lines=file.readlines()
	#print "loop begins"
	for line in lines:
		apkData=line.split(",")
		apkFamily=re.search('[^-]*',apkData[0]).group(0)
		if apkFamily in families: #skip benign
			apkData.remove(apkData[0])
			x=0
			for apkValue in apkData:
				if(apkFamily==families[x]):
					#case of TP/FN for families[x]
					#print "case of tp/fn"
					t=0				
					for thresh in thresholds :
						#print apkValue
						if (thresh>=Decimal(apkValue)):
							sc[x][4][t]=sc[x][4][t]+1
							#print "case tp"
						else:
							sc[x][1][t]=sc[x][1][t]+1						
						t=t+1
				else:
					#case of FP/TN for families[x]
					#print "case of fp/tn"
					t=0
					for thresh in thresholds :
						if (thresh>=Decimal(apkValue)):
							sc[x][2][t]=sc[x][2][t]+1
						else:
							sc[x][3][t]=sc[x][3][t]+1						
						t=t+1
				x=x+1
	
	#CalculateStats....
	x=0
	for family in families:
		t=0
		for thresh in thresholds:
			try:
				sc[x][5][t]=(float(sc[x][1][t]))/(sc[x][1][t] + sc[x][3][t])
			except ZeroDivisionError:
				sc[x][5][t]=0
			try:
				sc[x][6][t]=float((sc[x][1][t]))/(sc[x][1][t] + sc[x][4][t])
			except ZeroDivisionError:
				sc[x][6][t]=0
			try:
				sc[x][7][t]=float((sc[x][2][t]))/(sc[x][2][t] + sc[x][3][t])	
			except ZeroDivisionError:
				sc[x][7][t]=0
			try:
				sc[x][8][t]=float((sc[x][1][t] + sc[x][2][t]))/(sc[x][1][t] + sc[x][2][t] + sc[x][3][t] + sc[x][4][t])		
			except ZeroDivisionError:
				sc[x][8][t]=0
			try:
				sc[x][9][t]=1- ( float((sc[x][3][t] ))/(sc[x][3][t] + sc[x][2][t] ))
			except ZeroDivisionError:
				sc[x][8][t]=0
			t=t+1
		x=x+1

	#calculate overall stats		
	y=len(thresholds)
	totalTP=[0]*y
	totalTN=[0]*y
	totalFP=[0]*y
	totalFN=[0]*y
	Precision=[0.0]*y
	Recall=[0.0]*y
	TNR=[0.0]*y
	Accuracy=[0.0]*y
	FPR=[0.0]*y
	for t in range(0,y):
		for x in range(0,len(families)):
			totalTP[t]=totalTP[t]+sc[x][1][t]
			totalTN[t]=totalTN[t]+sc[x][2][t]
			totalFP[t]=totalFP[t]+sc[x][3][t]
			totalFN[t]=totalFN[t]+sc[x][4][t]
	for t in range(0,y):	
		try:
			Precision[t]=float(totalTP[t])/(totalTP[t]+totalFP[t])
		except ZeroDivisionError:
			Precision[t]=0
		try:
			Recall[t]=float(totalTP[t])/(totalTP[t]+totalFN[t])
		except ZeroDivisionError:
			Recall[t]=0
		try:
			TNR[t]=float(totalTN[t])/(totalTN[t]+totalFP[t])
		except ZeroDivisionError:
			TNR[t]=0
		try:
			Accuracy[t]=float(totalTP[t]+totalTN[t])/(totalTP[t]+totalFP[t] + totalTN[t]+totalFN[t])
		except ZeroDivisionError:
			Accuracy[t]=0
		try:
			FPR[t]=1-float(totalFP[t])/(totalFP[t]+totalTN[t])	
		except ZeroDivisionError:
			FPR[t]=1

	#print sc
	print "\n\nPrinting the SC Matrix \n"
	for x in range(0,len(families)):
		print "\n"
		for y in range(0,10):
			if(y==1):
				print "True Positives"
			if(y==2):
				print "True Negatives"
			if(y==3):
				print "False Positives"
			if(y==4):
				print "False Negatives"			
			if(y==5):
				print "Precision (tp/(tp+fp))"			
			if(y==6):
				print "Recall (TPrate) (tp/(tp+fn))"			
			if(y==7):
				print "True Negative Rate (tn/(tn+fp))"			
			if(y==8):
				print "Accuracy ((tp+tn)/(tp+tn+fp+fn))"			
			if(y==9):
				print "1-FPrate (1- fp/(fp+tn))"			
			print sc[x][y] 

	#print overall results
	print "\nOverall Statistics\n"
	print "True Positives"
	print totalTP
	print "True Negatives"
	print totalTN
	print "False Positives"
	print totalFP
	print "False Negatives"
	print totalFN
	print "Precision:"
	print Precision
	print "Recall		"
	print Recall
	print "True Negative Rate"
	print TNR
	print "Accuracy"
	print Accuracy
	print "1-False Positive Rate"
	print FPR
	
	print "\n\n creating PlotData file"
	for x in range(0,len(families)):
		if(x>0):
			print "\n\n"
		print "#family "+families[x]
		for y in range(0,len(thresholds)):
			print (str(thresholds[y]) + " " + str(sc[x][6][y]) + " " + str(1-sc[x][7][y]))

	print "\n\n creating barData file family,TP,FN"
	for x in range(0,len(families)):
		print families[x] + " " + str(sc[x][1][2]) + " " + str(sc[x][4][2])
	print "\n\n creating barData file family,TN,FP"
	for x in range(0,len(families)):
		print families[x] + " " + str(sc[x][2][2]) + " " + str(sc[x][3][2])

#main
print "inputFile: "+ inpfile
getmatrix(inpfile)


"""
		z=families.count(apkFamily)
		if (z==0):
			print "extracted family name "+ apkFamily
"""




