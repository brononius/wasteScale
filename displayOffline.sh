#!/bin/bash 

logger wasteScale: wiiboard disconnected
/usr/bin/python3 /diy/wasteScale/display.py --kind "Waste scale" --weight "- Offline -" 
