#!/bin/bash
apkList=`find apk/ -type f`;
cd disassembled; 
for apkName in $apkList;
do
	apktool d ../$apkName;
done;
