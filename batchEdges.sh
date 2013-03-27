#!/bin/bash
#Generates edges between classes for multiple apk's.
#Currently is being used on one family for testing.
#Minor adjustments can be made to automate use on multiple families.

#Eack apk should have a directory of classes in flatClasses/
apks=`ls flatClasses/`
for apk in $apks
do
	#Create an empty .raw file named after that apk that will later contain raw class to class edges
	echo "" > pdg/$apk.raw
	#Create a list of all classes in the apk
	classes=`ls flatClasses/$apk`
	for class in $classes
	do
		#Run generateEdges for each class and accumulate the output in the .raw file
		./scripts/generateEdges.sh $apk $class >> pdg/$apk.raw
	done
	#Get all the non-empty lines in the .raw file and sort them
	grep "." pdg/$apk.raw | sort > tt
	#Replace the old .raw file with this sorted one.
	mv tt pdg/$apk.raw

	#get rid of duplicates and aggregate
	#Create a list of edges from the .raw file
	edges=`grep "." pdg/$apk.raw`
	#Initialize totalWeight to 0
	totalWeight=0
	#Start the currentEdge as the first edge.
	#This will break if the .raw file has no edges, but that would indicate a bigger problem.
	currentEdge=`grep -m 1 "." pdg/$apk.raw | sed s/,[0-9].*/,/`
	for edge in $edges
	do
		#Edges are comma seperated into Source, Target, and Weight
		#Extract Source and Target to edgeName
		edgeName=`echo $edge | sed s/,[0-9].*/,/`
		#Extract Weight to edgeWeight
		edgeWeight=`echo $edge | sed s/.*,.*,//`
		#Edges with the same Source and Target are grouped together because they had been sorted
		#Therefore when a different Source and Target are detected there should be no more edgeweights to add to the total
		if [ $currentEdge != $edgeName ]
		then
			#add currentEdge and it's accumulated weight to addEdges
			aggEdges="$aggEdges$currentEdge$totalWeight\n"
			#get ready for next Source and Target
			currentEdge=$edgeName
			totalWeight=$edgeWeight
		#else add the edge's weigth to the totalWeight
		else
			totalWeight=$(($totalWeight+$edgeWeight))
		fi
	done
	#This must be done to handle the last edge in a file
	aggEdges="$aggEdges$currentEdge$totalWeight\n"
	#output aggregated edges to a .agg file
	echo -e $aggEdges > pdg/$apk.agg
done
#run pruneEdges.sh which will look for connections involving classes that aren't in the apk and remove them.
#such classes include java and android libraries.  These would stay in if the apk were statically linked.
./scripts/pruneEdges.sh

	
