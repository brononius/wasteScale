#!/bin/bash 

kind=$1   #Value is given by command paramaeter (fe currentweight.sh PMD)

#Log that measuring has start
logger wasteScale: Measuring
/usr/bin/python3 /diy/wasteScale/display.py --kind "$kind" --weight "Measuring"


#Measure & calculate
LU=$(timeout 1s /usr/bin/evtest /dev/input/event1 | grep value | egrep -m 1 "ABS_HAT1X" | awk '{print $11}' | awk -F: '{n+=$1} END {print n}' | awk '{print $1/10}')
RU=$(timeout 1s /usr/bin/evtest /dev/input/event1 | grep value | egrep -m 1 "ABS_HAT0X" | awk '{print $11}' | awk -F: '{n+=$1} END {print n}' | awk '{print $1/10}')
LB=$(timeout 1s /usr/bin/evtest /dev/input/event1 | grep value | egrep -m 1 "ABS_HAT1Y" | awk '{print $11}' | awk -F: '{n+=$1} END {print n}' | awk '{print $1/10}')
RB=$(timeout 1s /usr/bin/evtest /dev/input/event1 | grep value | egrep -m 1 "ABS_HAT0Y" | awk '{print $11}' | awk -F: '{n+=$1} END {print n}' | awk '{print $1/10}')
gross=`echo "scale=4; $LU+$RU+$LB+$RB" | bc`
tare=$(cat /dev/shm/wasteScaleTare)
net=$(bc <<< $gross'-'$tare)
netKG=`echo "scale=2; $net/6" | bc`
echo "$netKG" > /dev/shm/wasteScaleNet                          #put value in memory file for further use
logger wasteScale: current $kind weight is $netKG

#Display values
if ! awk '{exit $1>0}' /dev/shm/wasteScaleNet; 
        then
                /usr/bin/python3 /diy/wasteScale/display.py --kind "$kind" --weight "$netKG KG"
                sleep 10
                /usr/bin/python3 /diy/wasteScale/display.py --kind "Waste scale" --weight "Ready..."
        else
                /usr/bin/python3 /diy/wasteScale/display.py --kind "$kind" --weight "ERROR 2A"
                sleep 10
                /usr/bin/python3 /diy/wasteScale/display.py --kind "Waste scale" --weight "Ready..."
        fi
