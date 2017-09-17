#!/usr/bin/python
# -*- coding: latin-1 -*-

import sys
#import re
#import os
#import shutil
#import commands
import time
#from datetime import date, datetime
#import urllib
import ledclient

"""Display a moving object
"""

global maxbright
maxbright = 50 # should be >0, <256

def getcoordsbyLedCoords(xc, yc):
  x = (xc + 1) * 0.007
  y = (yc + 1) * 0.012
  return x, y


def normalizeSaturation(r, g, b):
  normfactor = 3 * maxbright / (r + b + g)
  return r * normfactor, g * normfactor, b * normfactor


def getHueByLedCoords(xc, yc):
#  global maxbright = 100 # should be >0, <256
  r = 50.0 + 100.0 * yc
  g = 50.0
  b = 0 # + 0.2 * xc
  return normalizeSaturation(r, g, b)


def displayball(serverip, ballx, bally):

  leddata = bytearray(5 * 22 *4)

  #Init leddata
  i = 0
  while i < (5 * 22 * 4):
    if (i % 4) == 0:
      leddata[i] = chr(0xFF) #header
#    else:
#      leddata[i] = 0
    i += 1


  # constants
  #a = 40
  a = 25
  ballradius = 0.0005 #meters


  if 1: #######################
      yc = 0
      while yc < 5:
        xc = 0
        while xc < 22:   

            # find x,y LED coordinates
            x, y = getcoordsbyLedCoords(xc, yc)
            #print xc, yc
            #print x, y
            xdist = max(abs(ballx - x) - ballradius, 0)
            ydist = max(abs(bally - y) - ballradius, 0)            

            brightness = maxbright * (1 - 2 * a * a * (xdist * xdist + ydist * ydist))
            brightness = max(brightness, 0)
            #print brightness, int(round(brightness))

            r, g, b = getHueByLedCoords(xc, yc)

            bluebright  = int(round(brightness * b / maxbright))
            redbright   = int(round(brightness * r / maxbright))
            greenbright = int(round(brightness * g / maxbright))

            bluebright  = min(bluebright, maxbright)
            redbright   = min(redbright, maxbright)
            greenbright = min(greenbright, maxbright)

            ledindex = ledclient.getledindexbydispcoords(xc, yc)
            if ledindex != -1:
              #get value from font matrix and update led data accordingly
              leddata[ledindex] = chr(0xFF)  #header
              ledindex += 1
              leddata[ledindex] = bluebright
              ledindex += 1

              leddata[ledindex] = greenbright
              ledindex += 1

              leddata[ledindex] = redbright
              ledindex += 1

          
            xc += 1
        yc += 1


  ledclient.transmit(leddata)
  ledclient.waitforAck()


def main():

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: <server ip>";
    sys.exit(1)
  

  serverip = args[0]

  ledclient.connect(serverip)

  delayconst = 0.03

  i = 0
  xv = 0.00151
  yv = 0.00307
  x = 0
  y = 0
  maxx = 0.16
  maxy = 0.09
  minx = -0.01
  miny = -0.03

#  while i < 1000:
  while 1:
    displayball(serverip, x, y)
    time.sleep(delayconst)
    if x > maxx or x < minx:
      xv *= -1
    if y > maxy or y < miny:
      yv *= -1
    x += xv
    y += yv  
    i += 1

if __name__ == "__main__":
  main()

