/***************************************************
Blackstone Internet of Coffee Pub Sub Program
 ****************************************************/

#include <ESP8266WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
#include <Wire.h>
#include "Adafruit_TCS34725.h"


/************** Temperature Sensor ***************/
#include "Adafruit_MLX90614.h"
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

/************** DHT TempHumidity Sensor ***************/
#include "DHT.h"
#define DHTPIN 2     // what digital pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
DHT dht(DHTPIN, DHTTYPE);

/************************* WiFi Access Point *********************************/
#define WLAN_SSID       "BTGDCguest"
#define WLAN_PASS       "Black$tone45"

/************************* MQTT Server Setup *********************************/
#define AIO_SERVER      "192.168.10.2"
#define AIO_SERVERPORT  1883                   // use 8883 for SSL
#define AIO_USERNAME    ""
#define AIO_KEY         ""

// ESP8266 WiFiClient to connect to the MQTT server.
WiFiClient client;
// or... use WiFiFlientSecure for SSL
//WiFiClientSecure client;

// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);
/****************************** Feeds ***************************************/
Adafruit_MQTT_Publish coffeePublish = Adafruit_MQTT_Publish(&mqtt, "/topic/coffee");

void MQTT_connect();

/**************************** WiFi Setup ************************************/
void setup() {
  Serial.begin(115200);
  delay(10);
  Serial.println(("Internet of Coffee!"));
  // Connect to WiFi access point.
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi connected");
  Serial.println("IP address: "); Serial.println(WiFi.localIP());
    // Input from MLX
  mlx.begin();
}

/**************************** Publish Loop ************************************/
void loop() {
  // Ensure the connection to the MQTT server is alive (this will make the first
  // connection and automatically reconnect when disconnected).  See the MQTT_connect
  // function definition further below.
  MQTT_connect();

  // Concatentate temperature sensor.
  float temperature = tempSensor();

  // Concatentate light sensor.
  float light = lightSensor();

  float humidity = dhtSensor();
  
  String data = String(humidity);

  // Publish the sensor information following the string format requested by the display group.
  if (! coffeePublish.publish(data.c_str())) {
    Serial.println(F("Failed"));
  } else {
    Serial.println(F("OK!"));
  }

  // ping the server to keep the mqtt connection alive
  // NOT required if you are publishing once every KEEPALIVE seconds
  /*
  if(! mqtt.ping()) {
    mqtt.disconnect();
  }
  */

  // Delay between publish sequences
  delay(1000);
}

/**************************** Temperature Sensor Publish ************************************/
float tempSensor() {
  // Temperature Sensor
  float tempObject = mlx.readObjectTempC();

  return tempObject;
}


/**************************** Light Sensor Publish ************************************/
int lightSensor() {
  // Analog Input from Light Sensor
  int pin = A0;
  float lightRead = analogRead(pin);

  return lightRead;
}

/**************************** Humidity Sensor Publish ************************************/
float dhtSensor() {
  // DHT temperature and humidity sensor values
  // Read humidity
  float h = dht.readHumidity();

  return h;
}

/**************************** RGB Sensor Publish ************************************/
int rgbSensor() {
  // Analog Input from RGB Sensor
  int coffeeStrength = 0;
  uint16_t r, g, b, c, colorTemp, lux;
  tcs.getRawData(&r, &g, &b, &c);
    
  if(( c > 600) && ( c < 710 )){
    coffeeStrength = 1;}
  else if (( c > 710 ) && ( c < 900 )){
    coffeeStrength = 2;}
  else{
    coffeeStrength = 0;}
    
  return coffeeStrength;
}

/**************************** Server Connection ************************************/
// Function to connect and reconnect as necessary to the MQTT server.
// Should be called in the loop function and it will take care if connecting.
void MQTT_connect() {
  int8_t ret;
  // Stop if already connected.
  if (mqtt.connected()) {
    return;
  }
  Serial.print("Connecting to MQTT... ");
  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected
       Serial.println(mqtt.connectErrorString(ret));
       Serial.println("Retrying MQTT connection in 5 seconds...");
       mqtt.disconnect();
       delay(5000);  // wait 5 seconds
       retries--;
       if (retries == 0) {
         // basically die and wait for WDT to reset me
         while (1);
       }
  }
  Serial.println("MQTT Connected!");
}
