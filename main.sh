#!/bin/bash
#This script should run the experiment with one command.  It also demonstrates the order in which things happen.

#main.sh expects an argument that will determine if it should generate signatures or detect signatures.
#the argument "genSig" will generate signatures.
#the argument "detectSig" will detect signatures.

./scripts/clean.sh
./scripts/batchDisassemble.sh
./scripts/makeClassDirs.sh
./scripts/flattenClasses.sh
./scripts/listClasses.sh
./scripts/batchEdges.sh
./scripts/runCreateModules.sh
./scripts/featureExtractor.py $1 > detectionResults.txt
