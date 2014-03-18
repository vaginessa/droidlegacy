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
