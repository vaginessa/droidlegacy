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
	#print sc headers
	print "thresholds used:"
	print thresholds
	print "\nPositive=Malware\nNegative=Benign"
	file=open(inpfile,"r")
	#get list of all families
	families=((file.readline()).strip()).split(",")
	families.remove(families[0])
	x=len(families)
	y=len(thresholds)

	totalTP=[0]*y
	totalTN=[0]*y
	totalFP=[0]*y
	totalFN=[0]*y

	lines=file.readlines()
	#print "loop begins"
	for line in lines:
		apkData=line.split(",")
		apkFamily=re.search('[^-]*',apkData[0]).group(0)
		apkData.remove(apkData[0])
		if (families.count(apkFamily)>0) :
			#case of tp/fn (Malware sample)
			for t in range(0,len(thresholds)):			
				temp=0
				for apkValue in apkData:			
					if (Decimal(apkValue)>=thresholds[t]): #case of TP
						temp=1
						break
			 	if (temp==1):
					totalTP[t]=totalTP[t]+1
				else:
					totalFN[t]=totalFN[t]+1										
		else:
			#case of fp/tn (Benign Sample)
			for t in range(0,len(thresholds)):			
				temp=0
				for apkValue in apkData:			
					if (Decimal(apkValue)>=thresholds[t]): #case of FP
						temp=1
						break
			 	if (temp==1):
					totalFP[t]=totalFP[t]+1
				else:
					totalTN[t]=totalTN[t]+1
	#calculate overall stats		
	y=len(thresholds)
	Precision=[0.0]*y
	Recall=[0.0]*y
	TNR=[0.0]*y
	Accuracy=[0.0]*y
	FPR=[0.0]*y
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


#main
print "inputFile: "+ inpfile
getmatrix(inpfile)


"""
		z=families.count(apkFamily)
		if (z==0):
			print "extracted family name "+ apkFamily
"""




