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
	echo "cleaning"
	./scripts/clean.sh
	echo "moving to data/apk/"
	cp testingSet/* data/apk/
	echo "disassembling"
	./scripts/batchDisassemble.sh
	echo "making class directories"
	./scripts/makeClassDirs.sh
	echo "flattening classes"
	./scripts/flattenClasses.sh
	echo "listing classes"
	./scripts/listClasses.sh
	echo "creating edges"
	./scripts/batchEdges.sh
	echo "creating modules"
	./scripts/runCreateModules.sh
	echo "detecting signatures"
	./scripts/featureExtractor.py "detectSig"
fi

cp *.png ~/Dropbox/
