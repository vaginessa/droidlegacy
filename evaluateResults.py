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
	thresholds=[0.5,0.7,0.9]
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
		sc[x]=[None]*5
		sc[x][0]=family
		sc[x][1]=[0]*y #tp
		sc[x][2]=[0]*y	#tn
		sc[x][3]=[0]*y	#fp
		sc[x][4]=[0]*y #fn
		x=x+1
	#print sc
	

	lines=file.readlines()
	#print "loop begins"
	for line in lines:
		apkData=line.split(",")
		apkFamily=re.search('[^-]*',apkData[0]).group(0)
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
	
	#print sc		
	print "Printing the SC Matrix \n\n"
	for x in range(0,len(families)):
		print "\n"
		for y in range(0,5):
			if(y==1):
				print "True Positives"
			if(y==2):
				print "True Negatives"
			if(y==3):
				print "False Positives"
			if(y==4):
				print "True Positives"			
			print sc[x][y] 

			

#main
getmatrix(inpfile)


"""
		z=families.count(apkFamily)
		if (z==0):
			print "extracted family name "+ apkFamily
"""




