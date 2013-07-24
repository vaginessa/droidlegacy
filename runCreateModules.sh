#!/bin/bash
#Helps automate the createModules.py script to run for multiple APKs

#Make a list of the names of edgelists that were created by aggregateEdges.py
edgeLists=`ls data/pdg/ | grep ".e.csv"`

for edgeList in $edgeLists
do
	#module files have a .m.csv file extension
	moduleFileName=`echo $edgeList | sed s/".e.csv"/".m.csv"/`
	#pass the edgeList as an argument to createModules.py and output the results to a module file

			echo "`date` - start $edgeList"
			date1=$(date +"%s")

	./scripts/createModules.py data/pdg/$edgeList > data/modules/$moduleFileName

			date2=$(date +"%s")
			diff=$(($date2-$date1))
			hours=$(($diff / 3600 ))
			minutes1=$(($diff / 60 ))
			minutes=$(($minutes1 % 60))
			seconds=$(($diff % 60))
      echo "$edgeList time: $hours:$minutes:$seconds"


done
