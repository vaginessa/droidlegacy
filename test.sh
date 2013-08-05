#! /bin/bash

echo "`date` - start"
date1=$(date +"%s")

sleep 10

date2=$(date +"%s")
diff=$(($date2-$date1))
hours=$(($diff / 3600 ))
minutes1=$(($diff / 60 ))
minutes=$(($minutes1 % 60))
seconds=$(($diff % 60))
echo "`date` - end"
echo "Elapsed time: $hours:$minutes:$seconds"
echo $date1
echo $date2

