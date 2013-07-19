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
		done
	else
		echo "incorrect choice"
	fi
done

