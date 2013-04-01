#!/bin/bash

edgeLists=`ls pdg/ | grep ".e.csv"`

for edgeList in $edgeLists
do
	moduleFileName=`echo $edgeList | sed s/".e.csv"/".m.csv"/`
	./scripts/createModules.py pdg/$edgeList > modules/$moduleFileName
done
