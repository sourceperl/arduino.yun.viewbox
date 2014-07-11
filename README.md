Arduino YUN ViewBox
===================

An Arduino Yun with an 20 chars x 4 lines I2C LCD screen (with PCF8574 chip).

The viewbox display temperature, pressure from a garden weather station, it
display also the level of "vigilance meteo" (weather alert french system). All
this informations are available on a local MQTT broker.

A script check regulary the number of unread mail on an IMAP server. The result
is also display on the panel.

Every data process and formating is doing by Python script. Each lines of the
LCD is a datastore value (key "line\_1" to "line\_4"). The arduino skecth read
datastores values and send it to the LCD I2C interface.

Files
-----

* **yun.py** format data from MQTT broker send it to datastore
* **email.py** check unread mail number on IMAP server send it to datastore
* **Yun\_LCD\_I2C.ino** is ATmega 32U4 sketch, do datastore to LCD transfer.

Requirements
------------

## Python

### MQTT lib

Add paho MQTT to your Python lib (test with 0.9 version):

  sudo pip install paho-mqtt

### json lib

Usage of json Python library is buggy on Yun (conflict with bridge json lib).
More details here https://github.com/arduino/YunBridge/issues/18.

To fix this problem:

    opkg update
    opkg upgrade cpu-mcu-bridge

## System setup

    mkdir /root/bin/
    cp yun.py /root/bin/
    cp email.py /root/bin/

### **yun.py** call at Yun startup

    root@Arduino:~/bin# cat /etc/rc.local
    # Put your custom commands here that should be executed once
    # the system init finished. By default this file does nothing.

    wifi-live-or-reset
    boot-complete-notify
    # add this to /etc/rc.local
    (sleep 10; python /root/bin/yun.py >/dev/null 2>/dev/null)&

    exit 0

### **email.py** call by cron every 5 mins

    root@Arduino:~/bin# cat /etc/crontabs/root
    #format [min] [hour] [day of month] [month] [day of week] [program to be run]
    # add this to /etc/crontabs/root
    */5 * * * * /usr/bin/python /root/bin/email.py

