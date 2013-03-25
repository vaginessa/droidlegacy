#!/bin/bash
#remove links to classes not present in apk
apks=`ls disassembled/`
for apk in $apks
do
	classes=`find disassembled/$apk/smali/ -type f | sed s/"[^\/]*\/[^\/]*\/[^\/]*\/"// | sed s/.smali//`
	apk=`echo $apk | sed s/.out/.classes/`
	edges=`grep "." pdg/$apk.agg`
	for edge in $edges
	do
		destination=`echo $edge| sed s/[^,]*,// | sed s/,.*//`
		present=false
		for class in $classes
		do
			if [ $class == $destination ]
			then
				present=true
			fi
		done
		if $present
		then
			pruned="$pruned$edge\n"
		fi
	done
	echo -e $pruned > pdg/$apk.pru
done
