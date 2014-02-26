import time
from PIL import Image
import numpy
from numpy import *
import misc_functions
import sys

import scipy.io.mmio
from scipy.io.mmio import *

def drawPrintHelp():
    """
        prints help
    """
    print " ----------- "
    print "DRAW.PY MODULE HELP"
    print " ----------- "
    print "this module contains tools to visualize data in "
    print "Matrix Market format matrix "
    print " ----------- "
    print "Usage:"
    print "> python draw.py FILE [OPTIONS]"
    print "\n"
    print "FILE - Meta Matrix file with matrix to visualize"
    print ""
    print "OPTIONS:"
    print "-help, --help  - print this message"
    print "-bright n  - set brightness=n; 5 by default"
    print "-scale n   - set scale-rate=n; 50 by default"
    print "-file FILENAME - save image into file with FILENAME name"
    print " -------- "

CONST_SCALE_RATE = 50
CONST_BRIGHTNESS = 5

def drawVisitsMatrix(file_name):
    
    history_matrix = mmread(file_name).tocsr()

    height = history_matrix.shape[0] / CONST_SCALE_RATE
    width  = history_matrix.shape[1] / CONST_SCALE_RATE
    picture_size = (width, height)

    picture = Image.new('RGB', picture_size)

    # setting non-zero pixels
    for i in range(height):
        #misc_functions.step()
        #print "i = ", i
        for j in range(width):
            #print "j = ", j
            pixel = history_matrix[i * CONST_SCALE_RATE : (i + 1) * CONST_SCALE_RATE, j * CONST_SCALE_RATE : (j + 1) * CONST_SCALE_RATE].toarray()
            #print "pixel = ", pixel
            col = int((255 * numpy.sum(numpy.sum(pixel))) / CONST_BRIGHTNESS)
            if col > 255:
                col = 255
            #print "col = ", col
            picture.putpixel((j,i), (col, col, col))

    picture.save(CONST_OUTPUT)

if ("-help" in sys.argv) or ("--help" in sys.argv) or (len(sys.argv) < 3):
    drawPrintHelp()
else:
    
    mm_filename = sys.argv[1]
    CONST_OUTPUT = mm_filename + ".bmp"
    
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "-scale":
            CONST_SCALE_RATE = int( sys.argv[i+1] )
        if sys.argv[i] == "-bright":
            CONST_BRIGHT = int( sys.argv[i+1] )
        
        if sys.argv[i] == "-file":
            CONST_OUTPUT = int( sys.argv[i+1] )

    
    print "Draw parameters:"
    print "scale-rate = ", CONST_SCALE_RATE
    print "brightness = ", CONST_BRIGHTNESS
    print "output file = ", CONST_OUTPUT
    print "data file = ", mm_filename
    print "----"
    
    print "Start processing.."
    drawVisitsMatrix(mm_filename)
    print "picture saved - [ mm_filename ]"
    
