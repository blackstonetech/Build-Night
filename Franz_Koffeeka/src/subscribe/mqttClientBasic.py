#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

client = mqtt.Client()
#rc = client.connect("localhost",1883,60)
rc = client.connect("192.168.10.6",1883,60)

print("Connected with result code "+str(rc))
client.publish("topic/coffee", "Hello world!");
print("Message Published")
client.disconnect();
