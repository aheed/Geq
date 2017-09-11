#!/usr/bin/python
# -*- coding: latin-1 -*-


import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #global socket variable


def connect(server):
  PORT = 10013

  s.connect((server, PORT))


def transmit(leddata):
  s.sendall(leddata)


def waitforAck():
  data = s.recv(1024)
  s.close()

  recstring = "got " + repr(data) + " (len:" + str(len(data)) + ")"
  print recstring



################################################################
## Old code and test stuff below

def sendleddata(server, leddata):
 
  PORT = 10013

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((server, PORT))

  s.sendall(leddata)

  data = s.recv(1024)
  s.close()

  recstring = "got " + repr(data) + " (len:" + str(len(data)) + ")"
  print recstring



def main():

  HOST = '127.0.0.1'    # The remote host

  leddata = ""

  i = 0
  while i < (5 * 22 * 4):
  
    if (i % 4) == 0:
      leddata += chr(0xFF) #header
      #print i
    else:
      leddata += chr(i / 2) 
    i += 1

  sendleddata(HOST, leddata)


if __name__ == "__main__":
  main()
