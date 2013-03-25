apks=`ls flatClasses/`
for apk in $apks
do
	echo "" > pdg/$apk.csv
	classes=`ls flatClasses/$apk`
	for class in $classes
	do
		./scripts/generateEdges.sh $apk $class >> pdg/$apk.csv
	done

	grep "." pdg/$apk.csv | sort > tt
	mv tt pdg/$apk.csv

	#get rid of duplicates and aggregate
	edges=`grep "." pdg/$apk.csv`
	totalWeight=0
	currentEdge=`grep -m 1 "." pdg/$apk.csv | sed s/,[0-9].*/,/`
	for edge in $edges
	do
		edgeName=`echo $edge | sed s/,[0-9].*/,/`
		edgeWeight=`echo $edge | sed s/.*,.*,//`
		if [ $currentEdge != $edgeName ]
		then
			aggEdges="$aggEdges$currentEdge$totalWeight\n"
			#get ready for next round
			#make sure the last edge is accounted for
			currentEdge=$edgeName
			totalWeight=$edgeWeight
		else
			totalWeight=$(($totalWeight+$edgeWeight))
		fi
	done
	aggEdges="$aggEdges$currentEdge$totalWeight\n"
	#try to handle the last edge
	echo -e $aggEdges > pdg/$apk.agg
done
./scripts/pruneEdges.sh

	
