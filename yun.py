# Python script for populate YUN datastore
# add (sleep 10; python /root/test/mqtt.py >/dev/null 2>/dev/null)&
# in /etc/rc.local to launch at startup

# misc lib
import time
import json
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
last_seen = 0
vig_59    = 'I'
vig_62    = 'I'
p_atmo    = 0.0
t_atmo    = 0.0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("pub/meteo_vig/dep/59")
  client.subscribe("pub/meteo_vig/dep/62")
  client.subscribe("pub/house/garden/pressure_sea_level")
  client.subscribe("pub/house/garden/temperature")

def on_disconnect(client, userdata, rc):
  value.put("line_1", "MQTT disconnect".ljust(20))

def on_message(client, userdata, msg):
  global last_seen
  global vig_59
  global vig_62
  global p_atmo
  global t_atmo
  global vig_level

  # log update
  last_seen = int(time.time())

  # process topic
  if (msg.topic == "pub/meteo_vig/dep/59"):
    try:
      index = int(json.loads(msg.payload)['value'])
      vig_59 = vig_level[index]
    except:
      pass
  elif (msg.topic == "pub/meteo_vig/dep/62"):
    try:
      index = int(json.loads(msg.payload)['value'])
      vig_62 = vig_level[index]
    except:
      pass
  elif (msg.topic == "pub/house/garden/pressure_sea_level"):
    try:
      p_atmo = float(json.loads(msg.payload)['value'])
    except:
      pass
  elif (msg.topic == "pub/house/garden/temperature"):
    try:
      t_atmo = float(json.loads(msg.payload)['value'])
    except:
      pass

# init MQTT client
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
    value.put("line_1", line1.ljust(20)[:20])
    # l2
    line2 = str("%7.2f C       62:%c" % (t_atmo, vig_62))
    value.put("line_2", line2.ljust(20)[:20])
    # l3 for email
    # blank process by another script
    # l4
    t_update = int(time.time()) - last_seen
    status = "KO" if (t_update > 180) else "OK"
    datetime = time.strftime("%d/%m/%y %H:%M:%S", time.localtime())
    line4    = datetime + " " + status
    value.put("line_4", line4.ljust(20)[:20])
    print(line4.ljust(20)[:20])
