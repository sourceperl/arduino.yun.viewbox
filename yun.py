#!/usr/bin/python

# Python script for populate YUN datastore

# misc lib
import time
import json
import threading
# MQTT lib
import paho.mqtt.client as mqtt
# Access to YUN datastore lib (bridge interface ARM <->ATmega)
import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient

# global vars
vig_level = {
1 : 'V',
2 : 'J',
3 : 'O',
4 : 'R',
}

th_lock   = threading.Lock()
store     = bridgeclient()
last_seen = 0
vig_59    = 'I'
vig_62    = 'I'
p_atmo    = 0.0
t_atmo    = 0.0
nb_mail   = 0

def on_connect(client, userdata, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("pub/meteo_vig/dep/59")
  client.subscribe("pub/meteo_vig/dep/62")
  client.subscribe("pub/house/garden/pressure_sea_level")
  client.subscribe("pub/house/garden/temperature")
  client.subscribe("pub/mail/loic.celine/unread")

def on_disconnect(client, userdata, rc):
  print("MQTT disconnect")

def on_message(client, userdata, msg):
  # global vars
  global last_seen
  global vig_59
  global vig_62
  global p_atmo
  global t_atmo
  global vig_level
  global nb_mail
  # thread lock
  th_lock.acquire()
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
  elif (msg.topic == "pub/mail/loic.celine/unread"):
    try:
      nb_mail = int(json.loads(msg.payload)['value'])
    except:
       pass
  # thread unlock
  th_lock.release()

def main():
  # global vars
  global last_seen
  global vig_59
  global vig_62
  global p_atmo
  global t_atmo
  global nb_mail
  # init MQTT client
  client               = mqtt.Client()
  client.on_connect    = on_connect
  client.on_disconnect = on_disconnect
  client.on_message    = on_message
  client.connect("192.168.1.60", port=1883, keepalive=30)
  client.loop_start();
  while(1):
    # main loop run every 300 ms
    time.sleep(0.3)
    # thread lock
    th_lock.acquire()
    # main loop
    # l1
    line1 = str("%7.2f hPa     59:%c" % (p_atmo, vig_59)).ljust(20)[:20]
    # l2
    line2 = str("%7.2f C       62:%c" % (t_atmo, vig_62)).ljust(20)[:20]
    # l3
    line3 = "%7d %s" % (nb_mail, 'e-mails' if (nb_mail > 1) else 'e-mail')
    line3 = line3.ljust(20)[:20]
    # l4
    t_update = int(time.time()) - last_seen
    status = "KO" if (t_update > 240) else "OK"
    datetime = time.strftime("%d/%m/%y %H:%M:%S", time.localtime())
    line4    = (datetime + " " + status).ljust(20)[:20]
    # thread unlock
    th_lock.release()
    # send result to datastore
    store.put("str_bloc", line1+line2+line3+line4)

if __name__ == '__main__':
    main()
    sys.exit(0)
