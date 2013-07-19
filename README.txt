Each shell script should be run in the .. directory relative to scripts/.  
It was simpler to write them this way.  In this case ADRD Test is the location these should be run from.
The scripts are written in Bash or Python.  
I added comments, but it will be very hard to understand without familiarity of grep and sed.
It may have been cleaner to do all of this in Python, but it sort of evolved this way.

To run the experiment run ./scripts/main.sh

These are the steps to go from apk to module:
	sanitize names - remove .- and spaces from name.  Also change end to -1.apk 
		For example "mario-party v1.1" becomes "mariopartyv11-1.apk" this is closer to the AMGP format
	disassemble apk's - batchDisassemble.sh
	make class directories - makeClassDirs.sh
	flatten classes - flattenClasses.sh
	make lists of classes (helps with aggregating edges) - listClasses.sh
	generate edges - batchEdges.sh
	create modules - runCreateModules.sh
	
	
