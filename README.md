# wasteScale
A waste scale, based on wiiboard &amp; RP Zero with pHAT. The global idea is to weight your waste, before you throw it away. You should just push a button (fe glass, paper...), and the weight is logged. This data will be shown on a display, and collected by a server. This way, you'll have a view how much waste you throw away.
I had an old wiiboard laying around that wasn't used anymore. And I found several old projects to connect this board to a linux server. Sadly, the scripts are outdated, and not 100% what I needed.


## 1. Normal sequence (user manual).

1. Boot up Raspberry Zero
   Shows message on display (fe Waste scale, Offline)

2. Connect wiiBoard with the frontbutton. 
   Shows a message on display (Waste scale, Ready). This can take a while (max 10sec), because it'll calibrate your board.
   If you move the board afterwards, you should recalibrate it! 

3. Put your waste on the board, and push a button.
   The result (kind and weight) should be shown on the display.
   After a while, the result will be erased.

4. The data is sent towards an external server (fe openHAB)


## 2. Error codes
- 1A:	No calibration, try reconnecting wiiboard or restart raspberry.
- 1B: Start measuring without wiiboard? Check wiiBoard connection, or ID
- 2A: Negative weight, check scale, recalibrate.

<br>

---

## 3. Technical blabla
I create all my scripts in a folder /diy. I use for this setup the folder /diy/wasteScale. 
If you want to change this folder, feel free. Just update all corresponding paths.

### 1. Software to installed?
   - evtest (wil get your data)
   - bc 

### 2. Display reset
The file resetDisplay.sh will reset the display when the raspberryPI is booted. It'll shows the enduser a message that the board is not (yet) connected.

```
vim /etc/crontab
@reboot root /diy/wasteScale/displayOffline.sh 
```

### 3. wiiBoard connection
Let your board be trusted to the raspberry Zero bluetooth. If this works out, you should only push the front button on your wiiboard to connect it. I don't have the issue that the button next to the batteries must be pushed. I works with the front button.
I've noticed that I sometimes I need to push 3 time on the button, but it works.

```
bluetoothctl
scan on   		(push button, and look for your boards ID)
trust XXX 		(XXX = board ID)
```

udev triggers a file to start reference, and changes display to 'ready'.
I had to create a workaround. Triggering script by udev caused 'freezes and timeouts'.
Change the address (DEVPATH) with your setup (check your /var/log/syslog for details).

```
vim /etc/udev/rules.d/1-rules
ACTION=="add", DEVPATH=="/devices/platform/soc/3f201000.serial/tty/ttyAMA0/hci0/hci0:11", SUBSYSTEM=="bluetooth", RUN+="/bin/sh /diy/wasteScale/wiiboardConnected.sh"
ACTION=="remove", DEVPATH=="/devices/platform/soc/3f201000.serial/tty/ttyAMA0/hci0/hci0:11", SUBSYSTEM=="bluetooth", RUN+="/bin/sh /diy/wasteScale/displayOffline.sh"
```

Restart udev

```
udevadm control --reload-rules && udevadm trigger
```

Put in a cron 

```
vim /etc/crontab
@reboot		root	/diy/wasteScale/wiiboardReference.sh 
```

### 4. Measure weight
Change the proper pins where you've connected the buttons
You can also change the description of the kind of waste.

```
vim /diy/wasteScale/buttonListen.py
```

Put this file into a cron so it's always listening:

```
vim /etc/crontab
@reboot		root	/usr/bin/python /diy/wasteScale/buttonListen.py
```

If needed, update the ID of your board (fe event1 or event2 or...).
You can find the ID by run the command evtest. Be carefull, this change with amount of USB devices.

```
vim /diy/wasterScale/currentWeight.sh
```
  


### 5. Transfer data

The data is been transfered over your network by MQTT. These are very small packages, and simple to pick up by other servers. Personally I use openHAB, but you can use whatever server you want. If you don't want to log the data, you can disable/erase the line in currentWeight.sh with the 'mosquitoo_pub' command. 

Example of my dashboard:
<p align="center">
<img src="https://user-images.githubusercontent.com/22466675/156196749-e7f0e3bd-a963-48a3-a426-beae8b0af28f.png" width="50%" />
</p>

To install MQTT, just install mosquitto on your raspberry:

```
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl daemon-reload
sudo systemctl enable mosquitto
```

You can test it with following command. The listener will stop once you reboot the RP, or if you kill the command manually.

```
mosquitto_sub -v -h broker_ip -p 1883 -t '#' & 
mosquitto_pub -h localhost -t TEST -m 123321
mosquitto_pub -h localhost -t TEST -m 15
mosquitto_pub -h localhost -t TEST2 -m 5
```



## 4. Documentation

Tools that give a good idea if your setup is working:
- bluetoothctl, fe ```bluetoothctl``` > ```scan on```
- evtest, fe ```evtest /dev/input/event1```
- xwiishow, , fe ```xwiishow list```, followed by ```xwiishow 1```
- Check your logs for wasteScale, fe ```grep wasteScale /var/log/syslog```

  


## 5. ToDo
- [ ] create hardware box
- [ ] Clean up code
- [ ] Make more flexible to installation path? Something else then /diy/.
- [ ] Find a better way for initial calibration, based on UDEV
- [ ] Clear screen before shutdown? Else always 'Ready/offline/...'?
- [ ] check for auto disconnect? Save batteries wiiboard!?
- [ ] Log battery levels?
- [ ] Doublecheck the weight values, seems to have a difference when weight is left, middle or right? I've got the feeling that his can be improved somehow.
