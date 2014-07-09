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

vig_level = {
1 : 'V',
2 : 'J',
3 : 'O',
4 : 'R',
}

value     = bridgeclient()
last_seen = int(time.time())
vig_59    = 'I'
vig_62    = 'I'
p_atmo    = 0.0
t_atmo    = 0.0

def on_connect(client, userdata, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("rfm12/18/#")
  client.subscribe("pub/meteo_vig/#")

def on_disconnect(client, userdata, rc):
  value.put("line_1", "MQTT disconnect".ljust(20))

def on_message(client, userdata, msg):
  global last_seen
  global vig_59
  global vig_62
  global p_atmo
  global t_atmo
  global vig_level
  # topic process
  if (msg.topic == "pub/meteo_vig/dep/59"):
    try:
      vig_59 = vig_level[int(msg.payload)]
    except KeyError:
      vig_59 = 'E'
  if (msg.topic == "pub/meteo_vig/dep/62"):
    try:
      vig_62 = vig_level[int(msg.payload)]
    except KeyError:
      vig_62 = 'E'
  if (msg.topic == "rfm12/18/lastseen"):
    last_seen = int(msg.payload)
  if (msg.topic == "rfm12/18/float/1"):
    # normalize at see level (measure point is at 25m)
    p_atmo = float(msg.payload) / 0.997275
  if (msg.topic == "rfm12/18/float/2"):
    t_atmo = float(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect("192.168.1.60", port=1883, keepalive=30)

_now = 0.0

while(1):
  # process message
  client.loop(timeout=0.1)
  # main loop run every 0.5s
  now = time.time()
  if (now > _now + 0.5):
    _now = time.time()
    # main loop
    # l1
    line1  = str("%7.2f hPa     59:%c" % (p_atmo, vig_59))
    value.put("line_1", line1.ljust(20))
    # l2
    line2 = str("%7.2f C       62:%c" % (t_atmo, vig_62))
    value.put("line_2", line2.ljust(20))
    # l3 for email
    # blank process by another script
    # l4
    t_update = int(time.time()) - last_seen
    datetime = time.strftime("%H:%M %d/%m", time.localtime())
    line4    = datetime + " age: " + str(t_update)
    #line4 = time.strftime("%a, %d %b %y %H:%M", time.localtime())
    value.put("line_4", line4.ljust(20))
    print(line4.ljust(20))
