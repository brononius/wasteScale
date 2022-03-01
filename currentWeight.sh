#!/bin/bash 

scriptPath='/diy/wasteScale'
eventID='/dev/input/event1'		#ID from wiiBoard
kind=$1					#Value is given by the command paramaeter (fe currentweight.sh PMD)

if [ -e $eventID ]
then
	#Log that measuring has start
	logger wasteScale: Measuring
	/usr/bin/python3  $scriptPath/display.py --kind "$kind" --weight "Measuring"

	#Measure & calculate
	LU=$(timeout 1s /usr/bin/evtest $eventID | grep value | egrep -m 1 "ABS_HAT1X" | awk '{print $11}' | awk -F: '{n+=$1} END {print n}' | awk '{print $1/10}')
	RU=$(timeout 1s /usr/bin/evtest $eventID | grep value | egrep -m 1 "ABS_HAT0X" | awk '{print $11}' | awk -F: '{n+=$1} END {print n}' | awk '{print $1/10}')
	LB=$(timeout 1s /usr/bin/evtest $eventID | grep value | egrep -m 1 "ABS_HAT1Y" | awk '{print $11}' | awk -F: '{n+=$1} END {print n}' | awk '{print $1/10}')
	RB=$(timeout 1s /usr/bin/evtest $eventID | grep value | egrep -m 1 "ABS_HAT0Y" | awk '{print $11}' | awk -F: '{n+=$1} END {print n}' | awk '{print $1/10}')
	gross=`echo "scale=4; $LU+$RU+$LB+$RB" | bc`
	tare=$(cat /dev/shm/wasteScaleTare)
	net=$(bc <<< $gross'-'$tare)
	netKG=`echo "scale=2; $net/6" | bc`
	logger wasteScale: current $kind weight is $netKG

	#Display values
	if ! awk '{exit $1>0}' /dev/shm/wasteScaleNet; 
	then
		/usr/bin/python3 $scriptPath/display.py --kind "$kind" --weight "$netKG KG"
#!!!		mosquitto_pub -h localhost -t $kind -m $netKG
		sleep 10
		/usr/bin/python3  $scriptPath/display.py --kind "Waste scale" --weight "Ready..."
	else
		/usr/bin/python3  $scriptPath/display.py --kind "Waste scale" --weight "ERROR 2A"
		sleep 5
		/usr/bin/python3  $scriptPath/display.py --kind "Waste scale" --weight "Ready..."
	fi
	logger wasteScale: ready for next measuring.
else
	#Seems that no wiiBoard was properly connected?
	logger wasteScale: No ID present, wiiBoard not connected?
	/usr/bin/python3  $scriptPath/display.py --kind "Waste scale" --weight "ERROR 1B"
fi
