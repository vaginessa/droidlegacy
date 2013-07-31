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

