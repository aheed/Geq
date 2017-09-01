#!/usr/bin/python
# -*- coding: latin-1 -*-

import sys
#import re
#import os
#import shutil
import commands
import time
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

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: <server ip>";
    sys.exit(1)

  #--------------------------

  temperturestring = "-"

  try:
    ufile = urllib.urlopen("http://www.temperatur.nu/termo/goteborg_ostra/temp.txt")
    #if ufile.info().gettype() == 'text/html':
    print ufile.info().gettype()
    #print ufile.read()

    #strip trailing <CR> and append degree symbol (°)
    temperturestring = ufile.read()[:-1] + "°" 
  except IOError:
    print 'problem reading url:', url
  #--------------------------

  serverip = args[0]
  #outputtext = "32° ABÖ"
  #outputtext = "19:31:54"
  outputtext = temperturestring
  print outputtext

  outputtextoffset = 2

  #disptext(serverip, outputtext, outputtextoffset)
  scrolltext(serverip, outputtext)

  
if __name__ == "__main__":
  main()
