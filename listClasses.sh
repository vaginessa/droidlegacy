#!/bin/bash
#Creates a list of classes present in the apk as they would appear in the edge list
#This helps when removing edges to classes that aren't in the apk

#List all files in dirList that have the .out extension
dirList=`ls data/flatClasses/ | grep '.classes'`;
for dirName in $dirList;
do
	#use find to list all the classes in the current apk
	classes=`ls data/flatClasses/$dirName | grep "." | sed s/"\."/"\/"/g`
	classList=''
	for class in $classes
	do
		classList="$classList$class\n"
	done
	echo -e $classList > data/classLists/$dirName
done
