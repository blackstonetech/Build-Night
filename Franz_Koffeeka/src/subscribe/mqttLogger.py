#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import os, datetime, time

# Internet of Coffee - Logger

#TODO: replace with args
LOG_FILE_PATH = '/home/iotadmin'
LOG_FILE_NAME = 'IoCoffee.log'


def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/coffeeLogs")
  
def on_message(client, userdata, msg):
  epochtime = time.time()
  rawMessage = str(msg.payload.decode("utf-8"))
  print("Message Received on " + msg.topic + ": " + rawMessage)
  logoutput = (str(epochtime) + " " + rawMessage)
  print("Message Written: " + logoutput)
  filepath = os.path.join(LOG_FILE_PATH, LOG_FILE_NAME)
  with open(filepath, "a") as f:
    f.write(str((logoutput) + '\n'))
    f.close()
  
client = mqtt.Client()
client.connect("127.0.0.1", 1883,60)
#client.connect("192.168.10.2", 1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
