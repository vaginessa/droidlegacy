#!/bin/bash
#Helps automate the createModules.py script to run for multiple APKs

#Make a list of the names of edgelists that were created by aggregateEdges.py
edgeLists=`ls data/pdg/ | grep ".e.csv"`

for edgeList in $edgeLists
do
	#module files have a .m.csv file extension
	moduleFileName=`echo $edgeList | sed s/".e.csv"/".m.csv"/`
	#pass the edgeList as an argument to createModules.py and output the results to a module file
	./scripts/createModules.py data/pdg/$edgeList > data/modules/$moduleFileName
done
