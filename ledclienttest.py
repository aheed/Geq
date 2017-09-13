#!/usr/bin/python
# -*- coding: utf-8 -*-


import ledclient




def main():

  HOST = '127.0.0.1'    # The remote host

  leddata = ""

  i = 0
  while i < (5 * 22 * 4):
  
    if (i % 4) == 0:
      leddata += chr(0xFF) #header
      #print i
    else:
      leddata += chr(255 - i / 2) 
    i += 1

#  ledclient.sendleddata(HOST, leddata)


  ledclient.connect(HOST)
  #ledclient.transmit(leddata)
  someleddata = ledclient.texttoleddata(":\"é°", 2)
  ledclient.transmit(someleddata)
  ledclient.waitforAck()



if __name__ == "__main__":
  main()

