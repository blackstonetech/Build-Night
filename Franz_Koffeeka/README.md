# Franz Koffeeka

The Internet of Coffee Project - Monitor the Office Coffee Pot

## Objective

Monitor the state of the Office Coffee Maker

* report on the amount of coffee in the pot
* report on when the pot was brewed
* report on the strength of the coffee in the pot
* other stretch goals like temperature of the coffee

## Architecture

The coffee IoT project is comprised of 4 logical elements.

* Coffee Sensor Array (publish)
* MQTT Message Broker (Open-Source Mosquitto)
* Python Subscription Service (subscribe)
* Python Presentation Service (present)

The sensor array is powered by an Adafruit feather, which is programmed in Arduino C. The sensor array collects information about the coffee pot based on sensors attached around the pot.

The Message Broker, Mosquitto, acts as a queue for capturing and publishing messages sent by the publish software. If you aren't familiar with how a message queue works; its a stack of information that is stored until it can be processed later. The information is pulled off the stack when its processed.

The subscription service listens to the queue and stores items in the queue to a file locally. Those files are formatted for use by the presentation service.

The presentation service contains the business logic for the application. It parses through the file created by the subscription service and presents to the coffee display based on logic contained within itself.

## Deployment

### Coffee Sensor Publish Software

The code can be found in the publish directory. Deploy the code like any other arduino code, by uploading the code through the Arduino IDE.

### MQTT Message Broker

Mosquitto should be deployed on the Raspberry PI 3. The software can be found: https://mosquitto.org

The website explains the installation.

Once installed, mosquitto needs to be setup to run. The broker can be manually run by executing

    mosquitto -d

Mosquitto can be set to run by default by adding the mosquitto -d command to

    /etc/rc.local

### Subscription Service

The subscription service is a python application that can be found in the subscribe folder. Run:

    python mqttSubBasic.py

or create a service definition to deploy at startup.

Sample service definition file (/etc/systemd/system/iotpresent.service)

        [Unit]
        Description=Coffee IoT Subscribe
        After=multi-user.target

        [Service]
        Type=idle
        ExecStart=/usr/bin/python3 /home/pi/Federal-IoT/Franz_Koffeeka/src/subscribe/mqttSubBasic.py

        [Install]
        WantedBy=multi-user.target

## Present Service

Also a python application, the service can be found in the present folder. Run:

    python coffee.py

or create a service definition to deploy.

Sample service definition file (/etc/systemd/system/iotpresent.service)

        [Unit]
        Description=Coffee IoT Present
        Wants=iotsubscribe.service
        After=multi-user.target iotsubscribe.service

        [Service]
        Type=idle
        ExecStart=/usr/bin/python /home/pi/Federal-IoT/Franz_Koffeeka/src/present/coffee.py
        Restart=always

        [Install]
        WantedBy=multi-user.target

## More Information

### Arduino Reading

* Intro https://learn.adafruit.com/ladyadas-learn-arduino-lesson-number-1
* Multi-tasking https://learn.adafruit.com/multi-tasking-the-arduino-part-1
* MQTT (pub/sub):  https://learn.adafruit.com/diy-esp8266-home-security-with-lua-and-mqtt

### Raspberry Pi Reading

* Intro https://www.raspberrypi.org/forums/viewtopic.php?t=4751
* SSH https://tutorials-raspberrypi.com/raspberry-pi-remote-access-by-using-ssh-and-putty/
* MQTT (pub/sub) https://learn.adafruit.com/diy-esp8266-home-security-with-lua-and-mqtt/configuring-mqtt-on-the-raspberry-pi

## All Materials Experimented With

Tutorials: [[http://www.adafruit.com/products/2821#tutorials]]

x Assembled Adafruit Feather HUZZAH ESP8266 WiFi
1x Micro Servo
1x PIR (motion) Sensor
1x USB Cable - A/Micro B
1x Fast Vibration Switch
1x Magnetic Contact Switch (door sensor)
1x Half-sized Breadboard
1x Premium Male/Male Jumper Wires - 40 x 6"
1x Magnetic Contact Switch (door sensor)
1x DHT22 Temperature-humidity Sensor + Extras
Component bag containing:

3x 12mm Tactile Switches
1x Breadboard Trim Potentiometer 10K
1x Diffused 10mm Green LED
1x Diffused 10mm Red LED
5x 10K 5% 1/4W Resistor
5x 560 Ohm 5% 1/4W Resistor
1x Piezo Buzzer
1x Photo Cell Light Sensor
1x Diffused RGB (tri-color) LED
1x Breadboard-friendly SPDT Slide Switch

Tutorials: [[http://www.adafruit.com/products/3032#tutorials]]
Melexis Contact-less Infrared Sensor - MLX90614 5V
Tutorials: [[http://www.adafruit.com/products/1748#tutorials]]
IR Break Beam Sensor - 3mm LEDs
Tutorials: [[http://www.adafruit.com/products/2167#tutorials]]
Photo Transistor Light Sensor
Tutorials: [[http://www.adafruit.com/products/2831#tutorials]]
Contact-less Infrared Thermopile Sensor Breakout - TMP007
Tutorials: [[http://www.adafruit.com/products/2023#tutorials]]
IR Break Beam Sensor - 5mm LEDs
Tutorials: [[http://www.adafruit.com/products/2168#tutorials]]
RGB Color Sensor with IR filter and White LED - TCS34725
Tutorials: [[http://www.adafruit.com/products/1334#tutorials]]

* Rasberry Pi 3 model B
* 32x32 "pixel" display panels