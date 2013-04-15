#!/bin/bash
#Disassembles all apk's in a directory with apktool
#The output includes smali classes, a readable Android Manifest and other files.

#Create a list of all apk's in the apk directory
apkList=`find data/apk/ -type f`;
#Move to the disassemble directory
cd data/disassembled; 
#For each apk
for apkName in $apkList;
do
	#Run apktool on the apk.  This should put the output in disassembled/
	apktool d ../../$apkName;
done;
cd ../..
