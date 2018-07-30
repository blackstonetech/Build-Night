#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import os, datetime, time

# Internet of Coffee - Subscriber

#TODO: replace with args
CSV_FILE_PATH = '/home/pi'
CSV_FILE_NAME = 'IoCoffee.csv'


def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/coffee")
  
def on_message(client, userdata, msg):
  epochtime = time.time()
  rawMessage = str(msg.payload.decode("utf-8"))
  print("Message Received on " + msg.topic + ": " + rawMessage)
  quality = 0 #rawMessage[0]  ### Determined by age of coffee
#  brewing = rawMessage[2]
#  strength = rawMessage[4:5]
#  level = rawMessage[6]
#  if brewing == "t":
#    print("It's brewing!")
#    lastbrew = str(epochtime)
#  if brewing != "t":
#     print("It's not brewing")
#    lastbrew = lastbrew

#   iocinput = (str(epochtime) + "|" + str(quality) + "|" + str(msg.payload.decode("utf-8")))
  iocinput = (str(epochtime) + "|" + str(quality) + "|" + rawMessage)
#  iocinput = str(epochtime) + "|" + str(lastbrew) + "|" + quality + "|" + brewing + "|" + strength + "|" + level
#  print(msg.topic + "|" + str(quality) + "|" + str(msg.payload.decode("utf-8")))
  print("Message Written: " + iocinput)
#  filepath = os.path.join('/home/pi', 'coffee.log')
  filepath = os.path.join(CSV_FILE_PATH, CSV_FILE_NAME)
  with open(filepath, "a") as f:
    f.write(str((iocinput) + '\n'))
    f.close()
  
client = mqtt.Client()
#client.connect("127.0.0.1", 1883,60)
client.connect("192.168.3.189", 1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
