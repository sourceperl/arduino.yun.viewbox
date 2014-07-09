# Python script for populate YUN datastore
# add (sleep 10; python /root/test/mqtt.py >/dev/null 2>/dev/null)&
# in /etc/rc.local to launch at startup

# misc lib
import time
# MQTT lib
import paho.mqtt.client as mqtt
# Access to YUN datastore lib (bridge interface ARM <->ATmega)
import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient

value = bridgeclient()

def on_connect(client, userdata, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("rfm12/18/#")

def on_message(client, userdata, msg):
  if (msg.topic == "rfm12/18/float/1"):
    # normalize at see level
    p_atmo = float(msg.payload) / 0.9972
    line1  = str("%7.2f hPa" % p_atmo)
    value.put("line_1", line1.ljust(20))
  if (msg.topic == "rfm12/18/float/2"):
    line2 = str("%7.2f C" % float(msg.payload))
    value.put("line_2", line2.ljust(20))
  print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.1.60", 1883, 60)

client.loop_start()

while(1):
  line4 = time.strftime("%a, %d %b %y %H:%M", time.localtime())
  value.put("line_4", line4.ljust(20))
  time.sleep(1)
