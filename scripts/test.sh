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

