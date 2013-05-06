#!/bin/bash
#This script should run the experiment with one command.  It also demonstrates the order in which things happen.

#main.sh expects an argument that will determine if it should generate signatures or detect signatures.
#the argument "genSig" will generate signatures.
#the argument "detectSig" will detect signatures.

mode=$1
echo $mode

if [ "$mode" == "all" ]
then
	#serarate training from test set
	rm testingSet/*
	rm trainingSet/*
	./scripts/sampleSegregator.py 70 "lucky"
fi

#for train and test mode I must manually place the apks in the appropriate 
#testingSet of trainingSet
if [ "$mode" == "train" ] || [ "$mode" == "all" ]
then
	#generate signatures with training set
	./scripts/clean.sh
	rm familySignatures/*
	cp trainingSet/* data/apk/
	./scripts/batchDisassemble.sh
	./scripts/makeClassDirs.sh
	./scripts/flattenClasses.sh
	./scripts/listClasses.sh
	./scripts/batchEdges.sh
	./scripts/runCreateModules.sh
	./scripts/featureExtractor.py "genSig" > detectionResults.txt
fi 

if [ "$mode" == "test" ] || [ "$mode" == "all" ]
then
	#detect signatures in test set
	./scripts/clean.sh
	cp testingSet/* data/apk/
	./scripts/batchDisassemble.sh
	./scripts/makeClassDirs.sh
	./scripts/flattenClasses.sh
	./scripts/listClasses.sh
	./scripts/batchEdges.sh
	./scripts/runCreateModules.sh
	./scripts/featureExtractor.py "detectSig" > detectionResults.txt
fi
