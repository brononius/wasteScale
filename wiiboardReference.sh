#!/bin/bash
while true; do
	FILE="/dev/shm/wasteScaleConnects"
	if [ -f "$FILE" ]
	then
		rm $FILE
		/diy/wasteScale/reference.sh
	fi
  sleep 3;
done
