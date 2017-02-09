#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import os, datetime, time

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/coffee")
  
def on_message(client, userdata, msg):
  epochtime = time.time()
  rawmessage = str(msg.payload.decode("utf-8"))
  quality = 0 #rawmessage[0]  ### Determined by age of coffee
#  brewing = rawmessage[2]
#  strength = rawmessage[4:5]
#  level = rawmessage[6]
#  if brewing == "t":
#    print("It's brewing!")
#    lastbrew = str(epochtime)
#  if brewing != "t":
#     print("It's not brewing")
#    lastbrew = lastbrew

  iocinput = (str(epochtime) + "|" + str(quality) + "|" + str(msg.payload.decode("utf-8")))
#  iocinput = str(epochtime) + "|" + str(lastbrew) + "|" + quality + "|" + brewing + "|" + strength + "|" + level
  print(msg.topic + "|" + str(quality) + "|" + str(msg.payload.decode("utf-8")))
  filepath = os.path.join('/home/pi', 'coffee.log')
  with open(filepath, "a") as f:
    f.write(str((iocinput) + '\n'))
    f.close()
  
client = mqtt.Client()
client.connect("127.0.0.1", 1883,60)
#client.connect("192.168.10.2", 1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
