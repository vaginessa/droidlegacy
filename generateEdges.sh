#!/bin/bash
#uses methods and fields in each class to determine which classes it depends on
#extracts this information from and .smali files and stores it in an edge list
#column 1 is the class that makes a call, column 2 is the class called, column 3
#is the number of times the edge is observed.

targetApk=$1
targetClass=$2
source=`grep "\.class " flatClasses/$targetApk/$targetClass | sed s/.*"\ L"// | sed s/";"//`
inherit=`grep "\.super " flatClasses/$targetApk/$targetClass | sed s/.*"\ L"// | sed s/";"//`

methodDests=`grep -sho "\ "[^"\ "]*";->.*(" flatClasses/$targetApk/$targetClass | sed s/" L"// | sed s/";->.*"//`
fieldDests=`grep -sho "\ "[^"\ "]*";->.*:" flatClasses/$targetApk/$targetClass | sed s/" L"// | sed s/";->.*"//`
#methodDests and fieldDests seem to be working.  Now I just need to get them all in one file as a list.
#I also need to look for class inheritance and consider package homogeny.

if [ $inherit != "java/lang/Object" ]
then
	iEdge="$iEdge$source,$inherit,10\n";
fi

for methodDest in $methodDests;
do
	#I will do edge weights later
	mEdge="$mEdge$source,$methodDest,2\n";
done;

for fieldDest in $fieldDests;
do
	#I will do edge weights later
	fEdge="$fEdge$source,$fieldDest,1\n";
done;

#I should prune out connections to self
#I should combine repeated connections to higher edge weights


echo -e "$iEdge$mEdge$fEdge"
