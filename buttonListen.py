import os
import requests
import time
import RPi.GPIO as GPIO

scriptPath="/diy/wasteScale"		#Path where the scripts are installed

gpio_pinA=5                         # The GPIO pin your the button is attached to
pinWasteA="Rest"                    # Corresponding name (waste) for that button

gpio_pinB=6                         # The GPIO pin the button is attached to
pinWasteB="PMD"                     # Corresponding name (waste) for that button

gpio_pinC=12                        # The GPIO pin the button is attached to
pinWasteC="Papier"                  # Corresponding name (waste) for that button

gpio_pinD=24                        # The GPIO pin the button is attached to
pinWasteD="Glas"                    # Corresponding name (waste) for that button

gpio_pinE=25                        # The GPIO pin the button is attached to
pinWasteE="GFT"                     # Corresponding name (waste) for that button

gpio_pinF=26                        # The GPIO pin the button is attached to
pinWasteF="Varia"                   # Corresponding name (waste) for that button


cmdWasteA= "/usr/bin/bash "+ scriptPath +"/currentWeight.sh "+ pinWasteA
cmdWasteB= "/usr/bin/bash "+ scriptPath +"/currentWeight.sh "+ pinWasteB
cmdWasteC= "/usr/bin/bash "+ scriptPath +"/currentWeight.sh "+ pinWasteC
cmdWasteD= "/usr/bin/bash "+ scriptPath +"/currentWeight.sh "+ pinWasteD
cmdWasteE= "/usr/bin/bash "+ scriptPath +"/currentWeight.sh "+ pinWasteE
cmdWasteF= "/usr/bin/bash "+ scriptPath +"/currentWeight.sh "+ pinWasteF

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

