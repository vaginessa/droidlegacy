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
	python scripts/aggregateEdges.py data/pdg/$edgeList data/classLists/$classListFile > data/pdg/$aggFileName
done
