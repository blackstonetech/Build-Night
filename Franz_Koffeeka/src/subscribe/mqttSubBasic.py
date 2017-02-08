#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import os, datetime, time

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/coffee")
  
def on_message(client, userdata, msg):
  epochtime = time.time()
  iocinput = (str(epochtime) + "|" + str(msg.payload.decode("utf-8")))
  print(msg.topic + " | " + str(msg.payload.decode("utf-8")))
  filepath = os.path.join('/home/pi', 'coffee.log')
  with open(filepath, "a") as f:
    f.write(str((iocinput) + '\n'))
    f.close()
  
client = mqtt.Client()
client.connect("192.168.10.6", 1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
