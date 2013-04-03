#!/bin/bash
#This script should run the experiment with one command.  It also demonstrates the order in which things happen.

./scripts/batchDisassemble.sh
./scripts/makeClassDirs.sh
./scripts/flattenClasses.sh
./scripts/listClasses.sh
./scripts/batchEdges.sh
./scripts/runCreateModules.sh
