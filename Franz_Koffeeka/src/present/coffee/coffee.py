import csv
import time
from rgbmatrix import Adafruit_RGBmatrix
from PIL import Image
from PIL import ImageDraw
import os, datetime, time
from optparse import OptionParser

SLEEP_INTERVAL = 1.0
IDLE_LOOP_MAX = 5
IMAGE_DISPLAY_DURATION = 1.0

#TODO: replace with args
CSV_FILE_PATH = '/home/pi'
CSV_FILE_NAME = 'IoCoffee.csv'
CSV_FILE_PATH_TEST = '/home/pi/Federal-IoT/Franz_Koffeeka/src/present/coffee'
CSV_FILE_NAME_TEST = 'testdata.csv'

# myfile = "/home/pi/Federal-IoT/Franz_Koffeeka/src/present/coffee/testdata.txt"
imgfilepath = "/home/pi/Federal-IoT/Franz_Koffeeka/src/present/Coffee Images/CoffeeExport/"
left_image = []
right_image = []

# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 2)

# Right now this is iterating the file and processing each row, which if line may be meant to do
# So hasn't hit tail(fin) which probably won't work with tell and seek

#TODO add a switch where it will replay the file and then start tailing, otherwise, just pass until last line and wait on tail


##  Right panel shows coffee pot level:
##     empty (0) - empty, red (1) - low, yellow (2) - half, green (3) - full
##   and strength: 0 - no drip, 1 - left drip, 2 - right drip, 3 - both drips
##  Left panel shows brewing status. Stays dark with no brewing active right now.
##    Later it could show last brew time maybe...
##  (Not totally sure what the graphic designer meant by the symbols, so this is the interpretation)
## Image selection code could be simplified by renaming files to include numerics and build file names or something.
## Another enhancement is to let drips build up to strength with each image display

def presentStatus(row):
    left_image.insert(1,'Black.png')
    left_image.insert(2,'Black.png')
    left_image.insert(3,'Black.png')
    right_image.insert(1,'Black.png')
    right_image.insert(2,'None')
    right_image.insert(3,'None')
    print(left_image[0])

    if  row['brewing'] == 't':
        left_image[0] = 'Brewing_Pink.png'
        left_image[1] = 'Black.png'
        left_image[2] = 'Brewing.png'

    if row['level'] == '0':
        if row['strength'] == '0':
            right_image[0] = 'Empty_0.png'
        elif row['strength'] == '1':
            right_image[0] = 'Empty_1.png'
        elif row['strength'] == '2':
            right_image[0] = 'Empty_2.png'
    elif row['level'] == '1':
        if row['strength'] == '0':
            right_image[0] = 'Red_0.png'
        elif row['strength'] == '1':
            right_image[0] = 'Red_1.png'
        elif row['strength'] == '2':
            right_image[0] = 'Red_2.png'
    elif row['level'] == '2':
        if row['strength'] == '0':
            right_image[0] = 'Yellow_0.png'
        elif row['strength'] == '1':
            right_image[0] = 'Yellow_1.png'
        elif row['strength'] == '2':
            right_image[0] = 'Yellow_2.png'
    elif row['level'] == '3':
        if row['strength'] == '0':
            right_image[0] = 'Green_0.png'
        elif row['strength'] == '1':
            right_image[0] = 'Green_1.png'
        elif row['strength'] == '2':
            right_image[0] = 'Green_2.png'
            
## Loop through 3 possible images displaying them.
## When no right images loaded (none), just repeat first image
    for img in range(3):
         left_imagefile = imgfilepath + left_image[img]
         print(left_imagefile)
         image = Image.open(left_imagefile)
         image.load()          # Must do this before SetImage() calls
         matrix.SetImage(image.im.id, 0, 0)
         if right_image[img] != 'None' :
             right_imagefile = imgfilepath + right_image[img]
         else :
             right_imagefile = imgfilepath + right_image[0]
             print(right_imagefile)
             rimage = Image.open(right_imagefile)
             rimage.load()          # Must do this before SetImage() calls
             matrix.SetImage(rimage.im.id, 33, 0)
         time.sleep(IMAGE_DISPLAY_DURATION)


def main():
## Not handling file name and quiet yet
    parser = OptionParser("usage: coffee.py [--file=filename [--quiet] [--test]")
    parser.add_option("-f", "--file", dest="csvfilename",
                  help="input csv file", metavar="FILE")
    parser.add_option("-q", "--quiet",
                  action="store_false", dest="quietmode", default=True,
                  help="don't print status messages to stdout")
    parser.add_option("-t", "--test",
                  action="store_true", dest="testmode", default=False,
                  help="run through existing file and present")

    (options, args) = parser.parse_args()

    if options.testmode:
        print("test mode active")
        csvFile = os.path.join(CSV_FILE_PATH_TEST, CSV_FILE_NAME_TEST)
    else:
        csvFile = os.path.join(CSV_FILE_PATH, CSV_FILE_NAME)

    fieldnames = ['epoch_time', 'last_brew_time', 'quality', 'brewing', 'strength', 'level']

    with open(csvFile, 'r') as fin:
#        reader = csv.DictReader(fin, delimiter='|', fieldnames=fieldnames, restval='n')
        reader = csv.reader(fin, delimiter='|')
#        for line in reader:
        for linex in fin:
#        for line in csv.reader(linex, delimiter='|'):
            linex = linex.rstrip('\r\n')
            line = linex.split('|')
            row = dict(zip(fieldnames, line))
            print("read line==>" + str(line) + "<== #" + str(reader.line_num) )
            print("read row==>" + str(row) + "<== #" + str(reader.line_num) )
            if options.testmode:
                print("test line==>" + str(line) + "<== #" + str(reader.line_num) )
                presentStatus(row)
            else:
                print("skipping line==>" + str(line) + "<==")

#       "Listen for new lines added to file."
        print("in tail loop")
        hold_line_num = reader.line_num
        loop_count = 0
        while True:
            if options.quietmode:
              if loop_count > IDLE_LOOP_MAX :
                print("Idle too long - exiting!")
                break
           
            where = fin.tell()
            linex = fin.readline()
            if not linex:
                print("in wait loop on line #" + str(reader.line_num))
                time.sleep(SLEEP_INTERVAL)
                loop_count += 1
                continue

#            fin.seek(where)
#            line = next(reader)
#            linex = fin.readline()
            linex = linex.rstrip('\r\n')
            line = linex.split('|')
            row = dict(zip(fieldnames, line))

            print("next line==>" + str(line) + "<== #" + str(reader.line_num) )
            print("next row==>" + str(row) + "<== #" + str(reader.line_num) )
##            if reader.line_num == hold_line_num :
##                time.sleep(SLEEP_INTERVAL)
##                loop_count += 1
##            else:
            presentStatus(row)
            hold_line_num = reader.line_num
            loop_count = 0
                

if __name__ == '__main__':
    main()

##### Holding on to some other attempts at code before clean-up. Delete for production ####

##def main():
##    print("here")
##    p = OptionParser("usage: tail.py file")
##    (options, args) = p.parse_args()
###    if len(args) < 1:
###        p.error("must specify a file to watch")
##
##    csvFile = os.path.join(CSV_FILE_PATH, CSV_FILE_NAME)
##
##    fieldnames = ['epoch_time', 'last_brew_time', 'quality', 'brewing', 'strength', 'level']
##
####    with open(csvFile, 'rb') as csvfile:
####         reader = csv.DictReader(csvfile,delimiter='|', fieldnames=fieldnames, restval='n')
####         for row in reader:
####             print(row)
#####         epochtime = time.strftime('%Y-%m-%d %H:%M:%S', float(row['epoch_time']))
####             print(row['epoch_time'], row['last_brew_time'], row['quality'],row['brewing'],row['strength'],row['level'])
#####         print(epoch_time, row['last_brew_time'], row['quality'],row['brewing'],row['strength'],row['level'])
##### note may work to get it off a string var: for row in csv.reader(['one,two,three']):
###    with open(args[0], 'r') as fin:
##    print("here")
##    with open(csvFile, 'r') as fin:
##        reader = csv.DictReader(fin, delimiter='|', fieldnames=fieldnames, restval='n')
###        for line in readlines_then_tail(fin):
###        for line in readlines_then_tail(reader):
### "New code scheme - read through file here"
##        for line in reader:
##            print("read line==>" + str(line) + "<==")
####            print(line.strip())
### this doesn't work?            if line:
##            if 1 == 1:
##                print("skip line==>" + str(line) + "<==")
##                presentStatus(line)
###                yield line
##            else:
### do this once working                tail(fin)
##                presentStatus(line)
###Logic to handle the epoch time
##    epochtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370))
##    print(epochtime)
##

## Keeping as it is another perspective with animation     
##if  row['brewing'] == 't':
##    left_image[0] = 'Brewing_Pink.png'
##    left_image[1] = 'Black.png'
##    left_image[2] = 'Brewing.png'
##if row['level'] == '0':
##    if row['strength'] == '0':
##    right_image[0] = 'Empty_0.png'
##    right_image[1] = 'Empty_1.png'
##    right_image[2] = 'Empty_2.png'
##elif row['level'] == '1':
##    right_image[0] = 'Red_0.png'
##    right_image[1] = 'Red_1.png'
##    right_image[2] = 'Red_2.png'
##elif row['level'] == '2':
##    right_image[0] = 'Yellow_0.png'
##    right_image[1] = 'Yellow_1.png'
##    right_image[2] = 'Yellow_2.png'
##elif row['level'] == '3':
##    right_image[0] = 'Green_0.png'
##    right_image[1] = 'Green_1.png'
##    right_image[2] = 'Green_2.png'
##else :
##    left_image[0] = 'Brewing_Pink.png'
##    left_image[1] = 'Black.png'
##    left_image[2] = 'Brewing.png'
##        


##     image = Image.open("Empty_1.png")
## image.load()          # Must do this before SetImage() calls
#matrix.Fill(0x6F85FF) # Fill screen to sky color
#for n in range(32, -image.size[0], -1): # Scroll R to L
## matrix.SetImage(image.im.id, 0, 0)
## time.sleep(2.0)

#Opening and reading from the file in python
#with open('testdata.txt', 'rb') as csvfile:
## with open(myfile, 'rb') as csvfile:
##   spamreader = csv.reader(csvfile, delimiter='|')
##   for row in spamreader:
##      print row
##      epoch = row[1]   
##
##print epoch

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

##    with open(csvFile, 'rb') as csvfile:
##         reader = csv.DictReader(csvfile,delimiter='|', fieldnames=fieldnames, restval='n')
##         for row in reader:
##             print(row)
###         epochtime = time.strftime('%Y-%m-%d %H:%M:%S', float(row['epoch_time']))
##             print(row['epoch_time'], row['last_brew_time'], row['quality'],row['brewing'],row['strength'],row['level'])
###         print(epoch_time, row['last_brew_time'], row['quality'],row['brewing'],row['strength'],row['level'])
### note may work to get it off a string var: for row in csv.reader(['one,two,three']):
#    with open(args[0], 'r') as fin:
##    print("here")
##    epoch_timeIndex = fieldnames.index("epoch_time")
##    last_brew_timeIndex = fieldnames.index("last_brew_time")
##    qualityIndex = fieldnames.index("quality")
##    brewingIndex = fieldnames.index("brewing")
##    strengthIndex = fieldnames.index("strength")
##    levelIndex = fieldnames.index("level")

##            try:
##                line = next(reader)
##            except StopIteration:
##                print("stopiteration")

### def readlines_then_tail(fin):
##def readlines_then_tail(line):
##    "Iterate through lines and then tail for further lines."
##    while True:
###        line = fin.readline()
###        line = next(fin)
##        print("next line==>" + str(line) + "<==")
##        if line:
##            yield line
##        else:
##            
##            tail(fin)
##
##def tail(fin):
##    "Listen for new lines added to file."
##    print("in tail")
##    while True:
##        where = fin.tell()
###        line = fin.readline()
##        print("in loop, where :" + str(where))
##        line = next(fin)
##        print("tail next line==>" + str(line) + "<==")
##        if not line:
##            time.sleep(SLEEP_INTERVAL)
##            fin.seek(where)
##        else:
##            yield line
##

