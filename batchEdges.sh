#Copyright 2013 Software Research Lab, University of Louisiana at Lafayette
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

#!/bin/bash
#Generates edges between classes for multiple apk's.
#Currently is being used on one family for testing.
#Minor adjustments can be made to automate use on multiple families.

#Eack apk should have a directory of classes in flatClasses/
apks=`ls data/flatClasses/`
#remove any previous files in the pdg directory
rm -f data/pdg/*

for apk in $apks
do
	#The raw edge results will be saved as a .raw file
	rawEdgeFile=`echo $apk | sed s/"\.classes"/"\.raw"/`
	#Create a list of all classes in the apk
	classes=`ls data/flatClasses/$apk`
	for class in $classes
	do
		#Run generateEdges for each class and accumulate the output in the .raw file
		./scripts/generateEdges.sh $apk $class | grep "." >> data/pdg/$rawEdgeFile
	done
done

#Aggregate similar edges and throw out irrelevant edges
./scripts/runAggregate.sh
