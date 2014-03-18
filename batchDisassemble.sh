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
#Disassembles all apk's in a directory with apktool
#The output includes smali classes, a readable Android Manifest and other files.

#Create a list of all apk's in the apk directory
apkList=`find data/apk/ -type f`;
#Move to the disassemble directory
cd data/disassembled; 
#For each apk
for apkName in $apkList;
do
	#Run apktool on the apk.  This should put the output in disassembled/
	apktool d ../../$apkName;
done;
cd ../..
