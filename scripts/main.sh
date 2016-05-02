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

#main.sh expects an argument that will determine if it should generate signatures or detect signatures.
#the argument "genSig" will generate signatures.
#the argument "detectSig" will detect signatures.

#toAnalyze needs to be filled with Modules

mode=$1
folds=$2
echo $mode

for ((fold=1;fold<=folds;fold++)) 
do
	if [ "$mode" == "all" ]
	then
		#serarate training from test set
		rm testingSet/*
		rm trainingSet/*
		./scripts/sampleSegregator.py $fold $folds
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
		cp benignModules/* data/experimentData/modules
		echo "detecting signatures fold: " $fold
		./scripts/featureExtractor.py "detectSig" $fold
	fi

done
