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

set terminal gif
set output "new.gif"
set xlabel "1-TNR"
set ylabel "Threshold"
set zlabel "Recall"
splot "/home/lad9344/vivek/data1.dat" ind 0:0 u 3:1:2 ti "ADRD" w lines,\
"/home/lad9344/vivek/data1.dat" ind 1:1 u 3:1:2 ti "AnserverBot" w lines,\
"/home/lad9344/vivek/data1.dat" ind 2:2 u 3:1:2 ti "BaseBridge" w lines,\
"/home/lad9344/vivek/data1.dat" ind 3:3 u 3:1:2 ti "DroidDream" w lines,\
"/home/lad9344/vivek/data1.dat" ind 4:4 u 3:1:2 ti "DroidDreamLight" w lines,\
"/home/lad9344/vivek/data1.dat" ind 5:5 u 3:1:2 ti "DroidKungFu1" w lines,\
"/home/lad9344/vivek/data1.dat" ind 6:6 u 3:1:2 ti "DroidKungFu2" w lines,\
"/home/lad9344/vivek/data1.dat" ind 7:7 u 3:1:2 ti "DroidKungFu3" w lines,\
"/home/lad9344/vivek/data1.dat" ind 8:8 u 3:1:2 ti "DroidKungFu4" w lines,\
"/home/lad9344/vivek/data1.dat" ind 9:9 u 3:1:2 ti "Geinimi" w lines,\
"/home/lad9344/vivek/data1.dat" ind 10:10 u 3:1:2 ti "GoldDream" w lines,\
"/home/lad9344/vivek/data1.dat" ind 11:11 u 3:1:2 ti "Pjapps" w lines,\
"/home/lad9344/vivek/data1.dat" ind 12:12 u 3:1:2 ti "Zsone" w lines,\
"/home/lad9344/vivek/data1.dat" ind 13:13 u 3:1:2 ti "jSMSHider" w lines

