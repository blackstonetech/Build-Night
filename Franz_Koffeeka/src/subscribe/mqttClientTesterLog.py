#!/usr/bin/env python3

import paho.mqtt.client as mqtt
MQTT_TOPIC_COFFEE = '/topic/coffeeLogs'

# This is the Publisher

client = mqtt.Client()
rc = client.connect("localhost",1883,60)
#rc = client.connect("192.168.10.6",1883,60)

print("Connected with result code "+str(rc))
#client.publish(MQTT_TOPIC_COFFEE, "Hello world!");
#client.publish(MQTT_TOPIC_COFFEE, "Quality|Brewing|Strength|Level");

#TODO Make this an array of messages that is iterated and maybe add a repeat count too
#  array could be a file also, like replaying a log...
testMessage = "0|f|1|3"
client.publish(MQTT_TOPIC_COFFEE, testMessage);
print("Message Published: " + testMessage)
client.disconnect();
