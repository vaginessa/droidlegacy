#!/bin/bash
dirList=`ls disassembled/ | grep '.out'`;
for dirName in $dirList;
do
	classes=`find disassembled/$dirName/smali/ -type f`
	for class in $classes
	do
		classDirName=`echo $dirName| sed s/.out/.classes/`;
		cp $class flatClasses/$classDirName/;
	done;
done;
