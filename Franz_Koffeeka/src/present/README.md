# Franz Koffeeka

## Internet of Coffee Project - Monitor the Office Coffee Pot

### present - code for presenting data to the display (runs on Rasberry Pi)

### Python Configuration for video:

https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black/usage

If you're using a Raspberry Pi, install the RPi.GPIO library by executing:
sudo apt-get update
sudo apt-get install build-essential python-dev python-pip
sudo pip install RPi.GPIO

If you're using a BeagleBone Black, install the Adafruit_BBIO library by executing:
 sudo apt-get update
sudo apt-get install build-essential python-dev python-pip
sudo pip install Adafruit_BBIO

Finally, on both the Raspberry Pi and Beaglebone Black install the Python Imaging Library and smbus library by executing:
sudo apt-get install python-imaging python-smbus

Now to download and install the SSD1306 python library code and examples, execute the following commands:
 sudo apt-get install git
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install

### Other video examples
https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/python
