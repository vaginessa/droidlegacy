#!/bin/bash
#This script should run the experiment with one command.  It also demonstrates the order in which things happen.

#main.sh expects an argument that will determine if it should generate signatures or detect signatures.
#the argument "genSig" will generate signatures.
#the argument "detectSig" will detect signatures.

#toAnalyze needs to be filled with Modules

mode=$1
echo $mode

for fold in {1..10}
do
	if [ "$mode" == "all" ]
	then
		#serarate training from test set
		rm testingSet/*
		rm trainingSet/*
		./scripts/sampleSegregator.py $fold
	fi

	#for train and test mode I must manually place the apks in the appropriate 
	#testingSet of trainingSet
	if [ "$mode" == "train" ] || [ "$mode" == "all" ]
	then
		#generate signatures with training set
		./scripts/clean.sh
		rm results/familySignatures_$fold/*
		rm results/signatureExplanations_$fold/*
		cp trainingSet/* data/experimentData/modules
		echo "creating signatures fold: " $fold
		./scripts/featureExtractor.py "genSig" $fold
	fi 

	if [ "$mode" == "test" ] || [ "$mode" == "all" ]
	then
		#detect signatures in test set
		./scripts/clean.sh
		rm results/csvData_$fold/*
		cp testingSet/* data/experimentData/modules
		echo "detecting signatures fold: " $fold
		./scripts/featureExtractor.py "detectSig" $fold
	fi
done
