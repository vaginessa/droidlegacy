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

Requirements:
APKTool: http://ibotpeaches.github.io/Apktool/install/
APKtool requires java version atleast 1.7
python 2.7

Directory Structure:
droidLegacy: main working directory. Scripts are meant to be executed from this directory.
  --scripts: contains scripts
  --data
    --apk: Should contain all apk files sanitized to AGMP naming format.
    --disassembled: output generated from running apktool on apks. 
 

Each shell script should be run in the .. directory relative to scripts/.  
It was simpler to write them this way.  In this case ADRD Test is the location these should be run from.
The scripts are written in Bash or Python.  
I added comments, but it will be very hard to understand without familiarity of grep and sed.
It may have been cleaner to do all of this in Python, but it sort of evolved this way.

To run the experiment run ./scripts/main.sh <mode> <folds>
<mode> can be one of "genSig", "detectSig" or "all"
<folds> is the value 'k' in k-fold cross validation. (See paper for details)

These are the steps to go from apk to module:
	sanitize names - remove .- and spaces from name.  Also change end to -1.apk 
		For example "mario-party v1.1" becomes "mariopartyv11-1.apk" this is closer to the AMGP format
	disassemble apk's - batchDisassemble.sh
	make class directories - makeClassDirs.sh
	flatten classes - flattenClasses.sh
	make lists of classes (helps with aggregating edges) - listClasses.sh
	generate edges - batchEdges.sh
	create modules - runCreateModules.sh
