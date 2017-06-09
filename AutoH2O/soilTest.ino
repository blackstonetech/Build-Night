int moistureLevel = 0;
int motor = 0;
char moistureBuffer[1000];

void setup() {
  pinMode(2, OUTPUT);
  digitalWrite(2, motor);
  Serial.begin(115200);
}

void loop() {
  moistureLevel = analogRead(A0);
  Serial.println(moistureLevel);
  sprintf(moistureBuffer, "Moisture level is: %d", moistureLevel);
  //Serial.println(moistureBuffer);

  if (moistureLevel > 370){
    motor = 1;
  } else{
    motor = 0;
  }

  digitalWrite(2, motor);

  delay(1000);
}
