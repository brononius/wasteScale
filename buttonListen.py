import os
import requests
import time
import RPi.GPIO as GPIO

#Buttons 5 6 12 24 25 26 


gpio_pinA=5     # The GPIO pin the button is attached to
pinWasteA="Rest"
cmdWasteA= "/usr/bin/bash /diy/wasteScale/currentWeight.sh "+ pinWasteA
gpio_pinB=6     # The GPIO pin the button is attached to
pinWasteB="PMD"
cmdWasteB= "/usr/bin/bash /diy/wasteScale/currentWeight.sh "+ pinWasteB
gpio_pinC=12     # The GPIO pin the button is attached to
pinWasteC="Papier"
cmdWasteC= "/usr/bin/bash /diy/wasteScale/currentWeight.sh "+ pinWasteC
gpio_pinD=24     # The GPIO pin the button is attached to
pinWasteD="Glas"
cmdWasteD= "/usr/bin/bash /diy/wasteScale/currentWeight.sh "+ pinWasteD
gpio_pinE=25     # The GPIO pin the button is attached to
pinWasteE="GFT"
cmdWasteE= "/usr/bin/bash /diy/wasteScale/currentWeight.sh "+ pinWasteE
gpio_pinF=26     # The GPIO pin the button is attached to
pinWasteF="Varia"
cmdWasteF= "/usr/bin/bash /diy/wasteScale/currentWeight.sh "+ pinWasteF

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_pinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_pinC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_pinD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_pinE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_pinF, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(0.2)
    if GPIO.input(gpio_pinA) == False: # Listen for the press, the loop until it steps
        os.system(cmdWasteA)
    if GPIO.input(gpio_pinB) == False: # Listen for the press, the loop until it steps
        os.system(cmdWasteB)
    if GPIO.input(gpio_pinC) == False: # Listen for the press, the loop until it steps
        os.system(cmdWasteC)
    if GPIO.input(gpio_pinD) == False: # Listen for the press, the loop until it steps
        os.system(cmdWasteD)
    if GPIO.input(gpio_pinE) == False: # Listen for the press, the loop until it steps
        os.system(cmdWasteE)
    if GPIO.input(gpio_pinF) == False: # Listen for the press, the loop until it steps
        os.system(cmdWasteF)


