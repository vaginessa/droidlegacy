#!/bin/bash
#combines edges between the same nodes into one edge
#with the sum weight of all smaller edges it has replaced.
#for example a,b,2 and a,b,1 would combine to become a,b,3

edges=`grep "." edges.csv`
uniqEdges=`grep -sho ".*," edges.csv| sort | uniq`
for uniqEdge in $uniqEdges
do
	totalWeight=0
	for edge in $edges
	do
		edgeName=`echo $edge | sed s/,[0-9].*/,/`
		edgeWeight=`echo $edge | sed s/.*,.*,//`
		if [ $uniqEdge == $edgeName ]
		then
			totalWeight=$(($totalWeight+$edgeWeight))
		fi
	done
	aggEdges="$aggEdges$uniqEdge$totalWeight\n"
done
echo -e $aggEdges
