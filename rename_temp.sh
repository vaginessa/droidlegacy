for i in $( ls ~/vivek/experiment/data/pdg/);
	do
		src=$i
		tgt=$(echo $i | sed 's/dash/-/')
		mv $src $tgt
	done

