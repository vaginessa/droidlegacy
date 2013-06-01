#!/bin/bash
#Helps automate aggregateEdges.py by providing the filenames for it to operate on

#Make a list of the edgeList extracted from the smali files
#These lists contain repeated edges as well as edges involving classes not relevant to the APK
#aggregateEdges.py will combine or eliminate such edges.
edgeLists=`ls data/pdg/ | grep "\.raw"`

for edgeList in $edgeLists
do
	#To eliminate edges that use superfluous classes we need a list of all classes in an APK
	classListFile=`echo $edgeList | sed s/"\.raw"/"\.classes"/`
	#The aggregated and pruned edgeList will be saved with a .e.csv extension.  This is almost gephi compatible.
	aggFileName=`echo $edgeList | sed s/"\.raw"/"\.e\.csv"/`
	#pass the unfiltered edgeList and classList as arguments to aggregateEdges.py.
	#Output the results to the .e.csv file
	./scripts/aggregateEdges.py data/pdg/$edgeList data/classLists/$classListFile > data/pdg/$aggFileName
done
