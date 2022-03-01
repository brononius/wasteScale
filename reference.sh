#!/bin/bash 

scriptPath="/diy/wasteScale"		#Path where the scripts are installed
eventID="/dev/input/event1"		#ID from wiiBoard

logger wasteScale: wiiBoard connected	
/usr/bin/python3 $scriptPath/display.py --kind "Waste scale" --weight "Calibrating"
logger wasteScale: wiiBoard reference is measured
LU=$(timeout 2s /usr/bin/evtest $eventID | grep value | egrep -m 1 "ABS_HAT1X" | awk '{print $11}' | awk -F: '{n+=$1} END {print n}' | awk '{print $1/10}')
RU=$(timeout 2s /usr/bin/evtest $eventID | grep value | egrep -m 1 "ABS_HAT0X" | awk '{print $11}' | awk -F: '{n+=$1} END {print n}' | awk '{print $1/10}')
LB=$(timeout 2s /usr/bin/evtest $eventID | grep value | egrep -m 1 "ABS_HAT1Y" | awk '{print $11}' | awk -F: '{n+=$1} END {print n}' | awk '{print $1/10}')
RB=$(timeout 2s /usr/bin/evtest $eventID | grep value | egrep -m 1 "ABS_HAT0Y" | awk '{print $11}' | awk -F: '{n+=$1} END {print n}' | awk '{print $1/10}')
gross=`echo "scale=4; $LU+$RU+$LB+$RB" | bc`
logger wasteScale: wiiBoard reference value is $gross
echo "$gross" > /dev/shm/wasteScaleTare
if ! awk '{exit $1>1}' /dev/shm/wasteScaleTare; 
then
	/usr/bin/python3 $scriptPath/display.py --kind "Waste scale" --weight "Ready..."
	logger wasteScale: display state is ready
else
	/usr/bin/python3 $scriptPath/display.py --kind "Waste scale" --weight "ERROR 1A"
fi
