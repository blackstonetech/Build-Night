# Franz Koffeeka

## Internet of Coffee Project - Monitor the Office Coffee Pot

### publish - code for message publishing (runs on Arduino)

When starting you must first edit:

The WiFi connection strings:

* WLAN_SSID
* WLAN_PASS

The MQTT server connection strings:
* AIO_SERVER
* AIO_SERVERPORT
* AIO_USERNAME
* AIO_KEY

The topic you are publishing to:

      Adafruit_MQTT_Publish coffeePublish = Adafruit_MQTT_Publish(&mqtt, "/topic/coffee");

### Sensor Teams

Each sensor should create a function following the publish loop.

For example:

      /**************************** Temperature Sensor Publish ************************************/
      float tempSensor() {
        // Temperature Sensor
        float tempObject = mlx.readObjectTempC();

        Serial.print("Temperature Sensor: ");
        Serial.print(tempObject);

        return tempObject;
      }

The values will be concatenated in the publish loop.

Notes:
* Ensure that a value separator is used.
* Convert non-string values to strings.
