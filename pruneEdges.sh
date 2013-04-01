#!/bin/bash
#remove links to classes not present in the relevant apk

#Make a list of the disassembled apks
apks=`ls disassembled/`
for apk in $apks
do
	#The top of the csv must contain Source,Target,Weight to work with Gephi

	#This line is only used if we are producing data for Gephi
	#pruned="Source,Target,Weight\n"

	#extract the names of each class in the apk in a format comparable to what's used as Source in edges
	classes=`find disassembled/$apk/smali/ -type f | sed s/"[^\/]*\/[^\/]*\/[^\/]*\/"// | sed s/.smali//`
	#replace .out with .classes in the apk name
	apk=`echo $apk | sed s/.out/.classes/`
	#Create list of edges from the .agg file
	edges=`grep "." pdg/$apk.agg`
	for edge in $edges
	do
		#Extract the Target or destination of an edge
		destination=`echo $edge| sed s/[^,]*,// | sed s/,.*//`
		#Present is false until a matching class in the apk is found
		present=false
		for class in $classes
		do
			#Compare the edge's Target/destination to all classes in the apk
			#If the Target/destination is actually in the apk then present becomes true.
			#This weeds out libraries like java and android that could cause silly relationships
			if [ $class == $destination ]
			then
				present=true
			fi
		done
		#If the Target/destination is actually in the apk then add it's edge to $pruned
		if $present
		then
			pruned="$pruned$edge\n"
		fi
	done
	#Gephi expects a .e.csv extension for importing spreadsheet data
	name=`echo $apk | sed s/"\.classes"/"\.e\.csv"/`
	#output the pruned list of edges to a name Gephi will accept
	echo -e $pruned > pdg/$name
done
