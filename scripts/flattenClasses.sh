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
#Extracts all classes from a disassembled apk and puts them in a single directory
#essentially flattening the package hierarchy.  This makes it easier to perform
#operations on all classes in an apk.

#List all files in dirList that have the .out extension
dirList=`ls data/disassembled/ | grep '.out'`;
for dirName in $dirList;
do
	#use find to list all the classes in the current apk
	classes=`find data/disassembled/$dirName/smali/ -type f`
	for class in $classes
	do
		#Replace the .out extension with .classes for the name of the directory holding an apk's classes
		classDirName=`echo $dirName| sed s/.out/.classes/`;
		#Create a name for each class based on its package hierarchy.  Dots seperate each level.
		#For example com/xxx/yyy/adad become com.xxx.yyy.adad
		name=`echo $class | sed s/"[^\/]*\/[^\/]*\/[^\/]*\/"// | sed s/"smali\/"// | sed s/"\.smali"// | sed s/"\/"/"\."/g`
		#Copy the class into the flattened directory with its new name.		
		cp $class data/flatClasses/$classDirName/$name;
	done;
done;
