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

Add paho MQTT to your Python lib (test with 0.9 version):

  sudo pip install paho-mqtt

System setup (cron/startup launch) for Python scripts is available on files
headers.

Usage of json Python library is buggy on Yun (conflict with bridge json lib).
More details here https://github.com/arduino/YunBridge/issues/18.

To fix this problem:

  opkg update
  opkg upgrade cpu-mcu-bridge
