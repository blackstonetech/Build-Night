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

/** Logging MQTT Server **/
#define Log_SERVER      "192.168.127.66"
#define Log_SERVERPORT  1883                   // use 8883 for SSL
#define Log_USERNAME    ""
#define Log_KEY         ""


// ESP8266 WiFiClient to connect to the MQTT server.
WiFiClient client;
// or... use WiFiFlientSecure for SSL
//WiFiClientSecure client;

// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);
// Logging Server Details
Adafruit_MQTT_Client logmqtt(&client, Log_SERVER, Log_SERVERPORT, Log_USERNAME, Log_KEY);

/****************************** Feeds ***************************************/
Adafruit_MQTT_Publish coffeePublish = Adafruit_MQTT_Publish(&mqtt, "/topic/coffee");

/** Feed for logging **/
Adafruit_MQTT_Publish logPublish = Adafruit_MQTT_Publish(&logmqtt, "/topic/coffeeLogs");

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
  MQTT_connect(logmqtt, 1);
  MQTT_connect(mqtt, 3);

  char brewing = dhtSensor();
  int strength = rgbSensor();
  int level = irSensorBreak();
  
  String data = "0|" + String(brewing) + "|" + String(strength) + "|" + String(level);
  Serial.println(data);

  mqtt_send(data);

  // Delay between publish sequences
  delay(5000);

  // ping the server to keep the mqtt connection alive
  if(! mqtt.ping()) {
    mqtt.disconnect();
  }
}

  // Publish the sensor information following the string format requested by the display group.
void mqtt_send(String data)
{
   if (! coffeePublish.publish(data.c_str())) {
    Serial.println(F("Failed"));
  } else {
    Serial.println(F("OK!"));
  }
}

void mqtt_debug_send(String data)
{
  if(logmqtt.connected()){
    if (! logPublish.publish(data.c_str())) {
      Serial.println(F("Failed"));
    } else {
      Serial.println(F("OK!"));
    }
  }
}

/**************************** Humidity Sensor Publish ************************************/
char dhtSensor() {
  // DHT temperature and humidity sensor values
  // Read humidity
  char ret = 'f';
  float h = dht.readHumidity();
  
  /*** Debug Logging ***/
  String data = "Humidity: " + String(h);
  mqtt_debug_send(data);
  
  Serial.println(h);
  if(h > 90){
    ret = 't';
  }
  /*return ret;*/
  return 'f';
}

/**************************** IR Sensor Break Sensor Publish ************************************/

int irSensorBreak(){
// read the state of the pushbutton value:
  sensorState3 = digitalRead(SENSORPIN75);
  sensorState2 = digitalRead(SENSORPIN50);
  sensorState1 = digitalRead(SENSORPIN25);

  /*** Debug Logging ***/
  String data = "IR Sensors - 1:" + String(sensorState1) + " 2:" + String(sensorState2) + " 3:" + String(sensorState3);
  mqtt_debug_send(data);

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

    /*** Debug Logging ***/
  String data = "RGB Sensor - r:" + String(r) + " g:" + String(g) + " b:" + String(b);
  mqtt_debug_send(data);

  Serial.println(c);
    
  if(( c > 6000) && ( c < 6300 )){
    coffeeStrength = 1;}
  else if (( c > 6300 ) && ( c < 7000 )){
    coffeeStrength = 2;}
  else{
    coffeeStrength = 0;}
    
  return coffeeStrength;
}

/**************************** Server Connection ************************************/
// Function to connect and reconnect as necessary to the MQTT server.
// Should be called in the loop function and it will take care if connecting.
void MQTT_connect(Adafruit_MQTT_Client mqtt_client, uint8_t retries) {
  int8_t ret;
  // Stop if already connected.
  if (mqtt_client.connected()) {
    return;
  }
  Serial.print("Connecting to MQTT... ");
  while ((ret = mqtt_client.connect()) != 0) { // connect will return 0 for connected
       Serial.println(mqtt_client.connectErrorString(ret));
       Serial.println("Retrying MQTT connection in 5 seconds...");
       mqtt_client.disconnect();
       delay(5000);  // wait 5 seconds
       retries--;
       if (retries == 0) {
         // basically die and wait for WDT to reset me
         while (1);
       }
  }
  Serial.println("MQTT Connected!");
}
