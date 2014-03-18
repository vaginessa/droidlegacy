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
#This script should run the experiment with one command.  It also demonstrates the order in which things happen.

loc=$1   #location where to setup the experiment folder
data=$2  #location of the 'data' folder
folds=$3 #no of folds
SCRIPTS=/home/lad9344/Android_Malware_Classifier/Module_Signature/scripts
echo "Setting up environment at" $loc

cd $loc
mkdir experiment
cd experiment
mkdir data
mkdir toAnalyze
mkdir trainingSet
mkdir testingSet
mkdir results


cd data
mkdir apk
mkdir classLists
mkdir disassembled
mkdir flatClasses
mkdir modules
mkdir pdg 

cd $loc/experiment/results/

for ((i=1;i<=$folds;i++))
do
mkdir csvData_$i
mkdir familySignatures_$i
mkdir signatureExplanations_$i
done

echo "all directories set!"
echo "copying data folder..."
cp $data/* $loc/experiment/data/apk/;
echo "sanitizing file names.."
cd $loc/experiment/data/apk/
for i in $( ls $loc/experiment/data/apk/);
	do
		src=$i
		tgt=$(echo $i | sed 's/-/dash/g' | sed 's/\./dot/g')
		mv $src $tgt
	done
echo "retrieving scripts..."
cp -r $SCRIPTS $loc/experiment/;
echo "setting permissions..."
chmod -R 777 $loc/experiment
echo "all set!"

OPTIONS="APK-to-Modules Quit"
select opt in $OPTIONS; do
	if [ "$opt" = "Quit" ]; then
		echo "Exiting.."
		echo "Thank You :)"
		exit
	elif [ "$opt" = "APK-to-Modules" ]; then
		cd $loc/experiment/scripts/
		./APK2Modules.sh $loc $folds
		opt="Quit"
	else
		echo "incorrect choice"
	fi
done
