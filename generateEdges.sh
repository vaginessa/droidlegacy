#uses methods and fields in each class to determine which classes it depends on
#extracts this information from and .smali files and stores it in an edge list
#column 1 is the class that makes a call, column 2 is the class called, column 3
#is the number of times the edge is observed.

source=`grep ".class " adad.smali | sed s/.*"\ L"// | sed s/";"//`
destinations=`grep -sho "\ "[^"\ "]*";->" adad.smali | sed s/" L"// | sed s/";->"//`
edge=""
for destination in $destinations;
do
	#I will do edge weights later
	$edge=$source,$destination\n;
done;
echo $edge>edges.csv


