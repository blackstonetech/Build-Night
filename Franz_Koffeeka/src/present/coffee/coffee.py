import csv
import time
from rgbmatrix import Adafruit_RGBmatrix
import Image
import ImageDraw

myfile = "/home/pi/coffee/testdata.txt"
# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 2)

# Flash screen red, green, blue (packed color values)


# Show RGB test pattern (separate R, G, B color values)
#for b in range(16):
#        for g in range(8):
#                for r in range(8):
#                        matrix.SetPixel(
#                          (b / 4) * 8 + g,
#                          (b & 3) * 8 + r,
#                          (r * 0b001001001) / 2,
#                          (g * 0b001001001) / 2,
#                           b * 0b00010001)

#matrix.SetPixel(32, 0, 90, 110, 15);

#time.sleep(10.0)
#matrix.Clear()

image = Image.open("Empty_1.png")
image.load()          # Must do this before SetImage() calls
#matrix.Fill(0x6F85FF) # Fill screen to sky color
#for n in range(32, -image.size[0], -1): # Scroll R to L
matrix.SetImage(image.im.id, 0, 0)
time.sleep(10.0)


#Opening and reading from t he file in python

#with open('testdata.txt', 'rb') as csvfile:
#   spamreader = csv.reader(csvfile, delimiter='|')
#   for row in spamreader:
#      epoch = row[1]   

#print epoch



#Logic to handle the epoch time
epochtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370))
#print epochtime




