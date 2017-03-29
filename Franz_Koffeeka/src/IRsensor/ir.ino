/* 
  IR Breakbeam sensor demo!
*/
  // Pin 13: Arduino has an LED connected on pin 13
  // Pin 11: Teensy 2.0 has the LED on pin 11
  // Pin  6: Teensy++ 2.0 has the LED on pin 6
  // Pin 13: Teensy 3.0 has the LED on pin 13
 
#define SENSORPIN75 14
#define SENSORPIN50 12
#define SENSORPIN25 13
 
// variables will change:
int sensorState3 = 0;         // variable for reading the pushbutton status
int sensorState2 = 0;         // variable for reading the pushbutton status
int sensorState1 = 0;         // variable for reading the pushbutton status
 
void setup() {
  // initialize the LED pin as an output:
  //pinMode(LEDPIN, OUTPUT);      
  // initialize the sensor pin as an input:
  pinMode(SENSORPIN75, INPUT);     
  pinMode(SENSORPIN50, INPUT);
  pinMode(SENSORPIN25, INPUT);
  digitalWrite(SENSORPIN75, HIGH); // turn on the pullup
  digitalWrite(SENSORPIN50, HIGH); // turn on the pullup
  digitalWrite(SENSORPIN25, HIGH); // turn on the pullup
  
  Serial.begin(9600);
}
 
void loop(){
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
  int total=sensorState3 + sensorState2 + sensorState1;
  if (total == 3){
  Serial.println("full");
  } else if (total == 2){
    Serial.println("half");
    } else if (total == 1){
      Serial.println("low");
      } else Serial.println("empty");
    
  /*
  Serial.println(sensorState3);
  Serial.println(sensorState2);
  Serial.println(sensorState1);
  Serial.println("===");
  */
  delay(5000);
  // check if the sensor beam is broken
  // if it is, the sensorState is LOW:
  /*if (sensorState == LOW) {     
    // turn LED on:
    Serial.println("Connected"); 
  } 
  if (sensorState == OFF) {
    // turn LED off:
    Serial.println("Broken"); 
  }*/
}
