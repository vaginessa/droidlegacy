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
#Creates a list of classes present in the apk as they would appear in the edge list
#This helps when removing edges to classes that aren't in the apk

#List all files in dirList that have the .out extension
dirList=`ls data/flatClasses/ | grep '.classes'`;
for dirName in $dirList;
do
	#use find to list all the classes in the current apk
	classes=`ls data/flatClasses/$dirName | grep "." | sed s/"\."/"\/"/g`
	classList=''
	for class in $classes
	do
		classList="$classList$class\n"
	done
	echo -e $classList > data/classLists/$dirName
done
