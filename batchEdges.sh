#!/bin/bash
#Generates edges between classes for multiple apk's.
#Currently is being used on one family for testing.
#Minor adjustments can be made to automate use on multiple families.

#Eack apk should have a directory of classes in flatClasses/
apks=`ls flatClasses/`
#remove any previous files in the pdg directory
rm -f pdg/*

for apk in $apks
do
	#The raw edge results will be saved as a .raw file
	rawEdgeFile=`echo $apk | sed s/".classes"/".raw"/`
	#Create a list of all classes in the apk
	classes=`ls flatClasses/$apk`
	for class in $classes
	do
		#Run generateEdges for each class and accumulate the output in the .raw file
		./scripts/generateEdges.sh $apk $class | grep "." >> pdg/$rawEdgeFile
	done
done

#Aggregate similar edges and throw out irrelevant edges
./scripts/runAggregate.sh
