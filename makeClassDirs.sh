#!/bin/bash
#Creates a directory for each apk where it's classes can be stored without package hierarchies.

#Make a list of disassembled apks.
dirList=`ls disassembled/ | grep '.out'`;
for dirName in $dirList; 
do
	#Create a directory for each apk replacing the .out extension with .classes.
	#Also put them in the flatClasses directory 
	classesName=flatClasses/`echo $dirName| sed s/.out/.classes/`;
	mkdir $classesName; 
done
