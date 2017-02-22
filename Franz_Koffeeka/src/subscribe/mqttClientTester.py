#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

client = mqtt.Client()
rc = client.connect("localhost",1883,60)
#rc = client.connect("192.168.10.6",1883,60)

print("Connected with result code "+str(rc))
#client.publish("topic/coffee", "Hello world!");
#client.publish("topic/coffee", "Quality|Brewing|Strength|Level");

#TODO Make this an array of messages that is iterated and maybe add a repeat count too
#  array could be a file also, like replaying a log...
testMessage = "0|f|1|3"
client.publish("topic/coffee", testMessage);
# client.publish("topic/coffee", "0|f|1|3");
print("Message Published: " + testMessage)
client.disconnect();
