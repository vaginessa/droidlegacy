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
#Creates a directory for each apk where it's classes can be stored without package hierarchies.

#Make a list of disassembled apks.
dirList=`ls data/disassembled/ | grep '.out'`;
for dirName in $dirList; 
do
	#Create a directory for each apk replacing the .out extension with .classes.
	#Also put them in the flatClasses directory 
	classesName=data/flatClasses/`echo $dirName| sed s/.out/.classes/`;
	mkdir $classesName; 
done
