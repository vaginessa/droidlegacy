set terminal epslatex
set output "bar1.eps"
#set terminal gif
#set output "bar2.gif"

set style data histograms
set style histogram rowstacked
set boxwidth 1 relative
set style fill pattern border 1.0

set autoscale
set size 0.75, 1.0
set xtics rotate by -45 scale 0 font ",8"

plot "/home/lad9344/vivek/barData1.dat" using 2 t "True Positives", '' using 3:xticlabels(1) t "False Negatives"
