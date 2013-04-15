#!/bin/bash
#Extracts all classes from a disassembled apk and puts them in a single directory
#essentially flattening the package hierarchy.  This makes it easier to perform
#operations on all classes in an apk.

#List all files in dirList that have the .out extension
dirList=`ls data/disassembled/ | grep '.out'`;
for dirName in $dirList;
do
	#use find to list all the classes in the current apk
	classes=`find data/disassembled/$dirName/smali/ -type f`
	for class in $classes
	do
		#Replace the .out extension with .classes for the name of the directory holding an apk's classes
		classDirName=`echo $dirName| sed s/.out/.classes/`;
		#Create a name for each class based on its package hierarchy.  Dots seperate each level.
		#For example com/xxx/yyy/adad become com.xxx.yyy.adad
		name=`echo $class | sed s/"[^\/]*\/[^\/]*\/[^\/]*\/"// | sed s/"smali\/"// | sed s/"\.smali"// | sed s/"\/"/"\."/g`
		#Copy the class into the flattened directory with its new name.		
		cp $class data/flatClasses/$classDirName/$name;
	done;
done;
