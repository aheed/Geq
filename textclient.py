#!/usr/bin/python
# -*- coding: latin-1 -*-

import sys
import re
#import os
#import shutil
import commands
import time
from datetime import date, datetime
import urllib

"""Display scrolling text etc
"""

def disptext(server, outputtext, offset):
  disptextcommand = "./disptext " + server + " \"" + outputtext + "\" " + str(offset)
  (dispcmdstatus, dispcmdoutput) = commands.getstatusoutput(disptextcommand)

def scrolltext(server, msgtext):
  maxoffset = 22
  minoffset = -(len(msgtext * 6))

  #print "ÖÄÅ" + str(minoffset)

  curroffset = maxoffset
  while curroffset > minoffset:
    disptext(server, msgtext, curroffset)
    time.sleep(0.1)
    curroffset -= 1


def displayTemperature(serverip):

  temperturestring = "-"

  try:
    ufile = urllib.urlopen("http://www.temperatur.nu/termo/goteborg_ostra/temp.txt")
    #if ufile.info().gettype() == 'text/html':
    #print ufile.info().gettype()
    #print ufile.read()

    #strip trailing <CR> and append degree symbol (°)
    temperturestring = ufile.read()[:-1] + "°" 
  except IOError:
    print 'problem reading url:', url

  disptext(serverip, temperturestring, 0)


def displayNews(serverip):
  print "entering displayNews"

  newsstring = "-"

  try:
    ufile = urllib.urlopen("https://www.svt.se/svttext/web/pages/100.html")
    #ufile = urllib.urlopen("http://www.temperatur.nu/termo/goteborg_ostra/temp.txt")
    #if ufile.info().gettype() == 'text/html':
    #print ufile.info().gettype()
    newsstring = ufile.read()

  except IOError:
    print 'problem reading url:', url

  #matches = re.findall("Y DH\">\s*(.+).*<", newsstring)
  matches = re.findall("<span class=\"Y DH\">\s*(.+)</span", newsstring)


  for match in matches:       
    print 'found', match
    matchwquotes = re.sub("\"", "\\\"", match) 
    print 'found', matchwquotes
    matchwotags = re.sub("<.*?>", "", matchwquotes)
    print 'found', matchwotags
    #scrolltext(serverip, match)
    scrolltext(serverip, matchwotags)


def displayDate(serverip):
  todaysdate = date.today()
  datestring = str(todaysdate.day) + "/" + str(todaysdate.month)
  #print datestring
  disptext(serverip, datestring, 0)


def displayTime(serverip):
  nowtime = datetime.now()
  #print nowtime.timetuple()

  #timestring = str(nowtime.timetuple().tm_hour) + ":" + str(nowtime.timetuple().tm_min)

  timestring = "%02d:%02d" % (nowtime.timetuple().tm_hour, nowtime.timetuple().tm_min)

  #print timestring
  disptext(serverip, timestring, 0)

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: <server ip>";
    sys.exit(1)
  

  serverip = args[0]

  delayconst = 4
  pausetimeconst = 0.5

  while(1):

    displayTime(serverip)
    time.sleep(delayconst)
    disptext(serverip, "", 0)
    time.sleep(pausetimeconst)

    displayDate(serverip)
    time.sleep(delayconst)
    disptext(serverip, "", 0)
    time.sleep(pausetimeconst)

    displayTemperature(serverip)
    time.sleep(delayconst)
    disptext(serverip, "", 0)
    time.sleep(pausetimeconst)

    displayNews(serverip)


if __name__ == "__main__":
  main()
