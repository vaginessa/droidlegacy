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
#Helps automate the createModules.py script to run for multiple APKs

#ensure output directory exists
mkdir -p data/modules;
#Make a list of the names of edgelists that were created by aggregateEdges.py
edgeLists=`ls data/pdg/ | grep ".e.csv"`

for edgeList in $edgeLists
do
	#module files have a .m.csv file extension
	moduleFileName=`echo $edgeList | sed s/".e.csv"/".m.csv"/`
	#pass the edgeList as an argument to createModules.py and output the results to a module file

			echo "`date` - start $edgeList"
			date1=$(date +"%s")

	python scripts/createModules.py data/pdg/$edgeList > data/modules/$moduleFileName

			date2=$(date +"%s")
			diff=$(($date2-$date1))
			hours=$(($diff / 3600 ))
			minutes1=$(($diff / 60 ))
			minutes=$(($minutes1 % 60))
			seconds=$(($diff % 60))
      echo "$edgeList time: $hours:$minutes:$seconds"


done
