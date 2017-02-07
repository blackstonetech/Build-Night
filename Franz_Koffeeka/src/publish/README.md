# Franz Koffeeka

## Internet of Coffee Project - Monitor the Office Coffee Pot

### publish - code for message publishing (runs on Arduino)

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
