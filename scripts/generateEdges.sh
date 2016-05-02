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
#uses methods, fields, and inheritance in each class to determine which classes it depends on
#extracts this information from and .smali files and stores it in an edge list
#column 1 is the Source, column 2 is the Target, and column 3 is the edge Weight.
#There is a lot of repeated code here that should be combined... later.

#The first passed argument is the apk to use.
targetApk=$1
#The second passed argument is the class in that apk to use.
targetClass=$2

#The following values are easy to extract because of the syntax used in smali.
#extract the name of the class being analyzed and use it as the Source for its edges

#the source should be found in the first line
source=`head -1 data/flatClasses/$targetApk/$targetClass | grep "\.class " | sed s/.*"\ L"// | sed s/";"//`

#figure out which class this one inherits.  It might just inherit the default Java object class
inherit=`grep "\.super " data/flatClasses/$targetApk/$targetClass | sed s/.*"\ L"// | sed s/";"//`

#extract method calls
methodDests=`grep -sho "\ "[^"\ "]*";->.*(" data/flatClasses/$targetApk/$targetClass | sed s/" L"// | sed s/";->.*"//`
#extract field calls
fieldDests=`grep -sho "\ "[^"\ "]*";->.*:" data/flatClasses/$targetApk/$targetClass | sed s/" L"// | sed s/";->.*"//`

#Ignore classes that inherit java/lang/Object.  This is not a class we are interested in links to.
if [ $inherit != "java/lang/Object" ]
then
	#For inheritance of other classes add an edge from the source to that class with weight 10.
	iEdge="$iEdge$source,$inherit,10\n";
fi

#For each method call add an edge from the source to the class containing that method with weigth 2.
for methodDest in $methodDests;
do
	mEdge="$mEdge$source,$methodDest,2\n";
done;

#For each method call add an edge from the source to the class containing that method with weigth 2.
for fieldDest in $fieldDests;
do
	fEdge="$fEdge$source,$fieldDest,1\n";
done;

#I should prune out connections to self... later.

#output the results with echo.  This should get picked up by batchEdges.sh.
echo -e "$iEdge$mEdge$fEdge"
