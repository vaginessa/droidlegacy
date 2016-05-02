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

loc=$1
folds=$2
	#APK to modules....
		cd $loc/experiment/
		echo "Dissasembling APKs..."
		./scripts/batchDisassemble.sh
		echo "Generating Class directories..."
		./scripts/makeClassDirs.sh
		echo "Flattening Classes..."
		./scripts/flattenClasses.sh
		echo "making a list of classes..." 
		./scripts/listClasses.sh
		echo "Generating Edges..." 
		./scripts/batchEdges.sh
		echo "Generating Modules..." 
		./scripts/runCreateModules.sh
		echo "Modules Generated"
OPTIONS="Run-Experiment Quit"
select opt in $OPTIONS; do
	if [ "$opt" = "Quit" ]; then
		echo "Exiting.."
		echo "Thank You :)"
		exit
	elif [ "$opt" = "Run-Experiment" ]; then
		cd $loc/experiment/
		./scripts/main.sh all $folds
		exit
	else
		echo "incorrect choice"
	fi
done

