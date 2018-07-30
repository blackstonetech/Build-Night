import csv
import time
from rgbmatrix import Adafruit_RGBmatrix
from PIL import Image
from PIL import ImageDraw
import os, datetime, time
from optparse import OptionParser

SLEEP_INTERVAL = 1.0
#IDLE_LOOP_MAX = 5
IDLE_LOOP_MAX = 15 
IMAGE_DISPLAY_DURATION = 1.0

IMAGE_BLACK = 'Black.png'
IMAGE_NONE = 'None'

#TODO: replace with args
CSV_FILE_PATH = '/home/pi'
CSV_FILE_NAME = 'IoCoffee.csv'
CSV_FILE_PATH_TEST = '/home/pi/Federal-IoT/Franz_Koffeeka/src/present/coffee'
CSV_FILE_NAME_TEST = 'testdata.csv'

# myfile = "/home/pi/Federal-IoT/Franz_Koffeeka/src/present/coffee/testdata.txt"
imgfilepath = "/home/pi/Federal-IoT/Franz_Koffeeka/src/present/img/"

left_image = [IMAGE_BLACK, IMAGE_BLACK, IMAGE_BLACK]
right_image = [IMAGE_BLACK, IMAGE_NONE, IMAGE_NONE]

# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 2)

# Right now this is iterating the file and processing each row, which if line may be meant to do
# So hasn't hit tail(fin) which probably won't work with tell and seek

#TODO add a switch where it will replay the file and then start tailing, otherwise, just pass until last line and wait on tail

##  Right panel shows coffee pot level:
##     empty (3) - empty, red (2) - low, yellow (1) - half, green (0) - full
##   and strength: 0 - no drip, 1 - left drip, 2 - right drip, 3 - both drips
##   Currently there is only one image for right, so whatever is set in position 0 goes to 1 & 2
##  Left panel shows brewing status. Stays dark with no brewing active right now.
##    Later it could show last brew time maybe...
##  (Not totally sure what the graphic designer meant by the symbols, so this is the interpretation)
## Image selection code could be simplified by renaming files to include numerics and build file names or something.
## Another enhancement is to let drips build up to strength with each image display
##   (or change strength represention which is backlog item and then drips could display animated while brewing)
##   Currently the only use for left is brewing, so it is either black the whole time or
##     flashes white brewing (0), black (1), pink brewing (2) to make a flashing sign affect

def presentStatus(row):

# initialize to black, but then right 2 & 3 need None for logic below
    for img in range(3):
       left_image[img] = IMAGE_BLACK
       right_image[img] = IMAGE_BLACK
    right_image[1] = IMAGE_NONE
    right_image[2] = IMAGE_NONE

    if  row['brewing'] == 't':
        left_image[0] = 'Brewing_Pink.png'
        left_image[1] = 'Black.png'
        left_image[2] = 'Brewing.png'

    if row['level'] == '3':
        if row['strength'] == '0':
            right_image[0] = 'Empty_0.png'
        elif row['strength'] == '1':
            right_image[0] = 'Empty_1.png'
        elif row['strength'] == '2':
            right_image[0] = 'Empty_2.png'
    elif row['level'] == '2':
        if row['strength'] == '0':
            right_image[0] = 'Red_0.png'
        elif row['strength'] == '1':
            right_image[0] = 'Red_1.png'
        elif row['strength'] == '2':
            right_image[0] = 'Red_2.png'
    elif row['level'] == '1':
        if row['strength'] == '0':
            right_image[0] = 'Yellow_0.png'
        elif row['strength'] == '1':
            right_image[0] = 'Yellow_1.png'
        elif row['strength'] == '2':
            right_image[0] = 'Yellow_2.png'
    elif row['level'] == '0':
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