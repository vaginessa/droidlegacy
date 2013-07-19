#!/bin/bash
#This script should run the experiment with one command.  It also demonstrates the order in which things happen.

loc=$1   #location where to setup the experiment folder
data=$2  #location of the 'data' folder
folds=$3 #no of folds
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
cp -r /home/lad9344/Android_Malware_Classifier/Module_Signature/scripts $loc/experiment/;
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
