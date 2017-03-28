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

/************************* WiFi Access Point *********************************/
#define WLAN_SSID       "BTGDCguest"
#define WLAN_PASS       "Black$tone45"
/************************* MQTT Server Setup *********************************/
#define AIO_SERVER      "192.168.3.82"
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

/************** DHT TempHumidity Sensor ***************/
#include "DHT.h"
#define DHTPIN 2     // what digital pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
DHT dht(DHTPIN, DHTTYPE);

/************** IR Sensor Inputs ***************/
#define SENSORPIN75 14
#define SENSORPIN50 12
#define SENSORPIN25 13

/************** TCS Sensor Inputs ***************/
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_700MS, TCS34725_GAIN_1X);

/************** Variables for reading the pushbutton status ***************/
int sensorState3 = 0;         
int sensorState2 = 0;         
int sensorState1 = 0;  

void MQTT_connect();

/**************************** WiFi Setup ************************************/
void setup() {
// initialize the sensor pin as an input:
  pinMode(SENSORPIN75, INPUT);     
  pinMode(SENSORPIN50, INPUT);
  pinMode(SENSORPIN25, INPUT);
// Turn on the pullup
  digitalWrite(SENSORPIN75, HIGH);
  digitalWrite(SENSORPIN50, HIGH);
  digitalWrite(SENSORPIN25, HIGH); 
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

void loop() {
  // Ensure the connection to the MQTT server is alive (this will make the first
  // connection and automatically reconnect when disconnected).  See the MQTT_connect
  // function definition further below.
  MQTT_connect();

  boolean brewing = dhtSensor();
  int strength = rgbSensor();
  int level = irSensorBreak();
  
  String data = String(brewing) + "|" + String(strength) + "|" + String(level);
  Serial.println(data);

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
  delay(500);
}

/**************************** Humidity Sensor Publish ************************************/
boolean dhtSensor() {
  // DHT temperature and humidity sensor values
  // Read humidity
  boolean ret = false;
  float h = dht.readHumidity();
  if(h > 45){
    ret = true;
  }
  return ret;
}

/**************************** IR Sensor Break Sensor Publish ************************************/

int irSensorBreak(){
// read the state of the pushbutton value:
  sensorState3 = digitalRead(SENSORPIN75);
  sensorState2 = digitalRead(SENSORPIN50);
  sensorState1 = digitalRead(SENSORPIN25);

  /*
   * 3 = full
   * 2 = half
   * 1 = low
   * 0 = empty
   */
  int total = sensorState3 + sensorState2 + sensorState1;
  return total;
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
