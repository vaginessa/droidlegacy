dirList=`ls disassembled/ | grep '.out'`;
for dirName 
in $dirList; 
do 
	classesName=flatClasses/`echo $dirName| sed s/.out/.classes/`;
	mkdir $classesName; done
