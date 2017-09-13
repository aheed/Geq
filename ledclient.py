#!/usr/bin/python
# -*- coding: utf-8 -*-


import socket


#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #global socket variable


############################
MAX_BRIGHTNESS = 64

#############################################################
myfont = {}

myfont['A'] = 0x094BD26
myfont['B'] = 0x0749D27
myfont['C'] = 0x0648526
myfont['D'] = 0x0F8C62F
myfont['E'] = 0x1F0BC3F
myfont['F'] = 0x010BC3F
myfont['G'] = 0x1EC862E
myfont['H'] = 0x118FE31
myfont['I'] = 0x0108421
myfont['J'] = 0x0E8C210
myfont['!'] = 0x0100421
myfont['K'] = 0x0928CA9
myfont['L'] = 0x1F08421
myfont['M'] = 0x118D771
myfont['N'] = 0x11CD671

myfont['O'] = 0x0E8C62E
myfont['P'] = 0x010BE2F
myfont['Q'] = 0x164C62E
myfont['R'] = 0x118BE2F
myfont['S'] = 0x0F8383E
myfont['T'] = 0x042109F
myfont['U'] = 0x0E8C631
myfont['V'] = 0x0454631
myfont['W'] = 0x11DD631
myfont['X'] = 0x1151151
myfont['Y'] = 0x0421151
myfont['Z'] = 0x1F1111F

myfont['a'] = myfont['A']
myfont['b'] = myfont['B']
myfont['c'] = myfont['C']
myfont['d'] = myfont['D']
myfont['e'] = myfont['E']
myfont['f'] = myfont['F']
myfont['g'] = myfont['G']
myfont['h'] = myfont['H']
myfont['i'] = myfont['I']
myfont['j'] = myfont['J']
myfont['k'] = myfont['K']
myfont['l'] = myfont['L']
myfont['m'] = myfont['M']
myfont['n'] = myfont['N']
myfont['o'] = myfont['O']
myfont['p'] = myfont['P']
myfont['q'] = myfont['Q']
myfont['r'] = myfont['R']
myfont['s'] = myfont['S']
myfont['t'] = myfont['T']
myfont['u'] = myfont['U']
myfont['v'] = myfont['V']
myfont['w'] = myfont['W']
myfont['x'] = myfont['X']
myfont['y'] = myfont['Y']
myfont['z'] = myfont['Z']

myfont['0'] = 0x0F4A52F
myfont['1'] = 0x0210842
myfont['2'] = 0x0F0BD0F
myfont['3'] = 0x0F43D0F
myfont['4'] = 0x0843D29
myfont['5'] = 0x0F43C2F
myfont['6'] = 0x0F4BC2F
myfont['7'] = 0x084210F
myfont['8'] = 0x0F4BD2F
myfont['9'] = 0x0843D2F

myfont[':'] = 0x0008020
myfont['.'] = 0x0100000
myfont['/'] = 0x0008880
myfont['-'] = 0x0001C00
myfont['+'] = 0x0011c40

myfont['"'] = 0x000000A
myfont['('] = 0x0208422
myfont[')'] = 0x0110841

#myfont[176] = 0x0001926  #°
myfont[u'°'] = 0x0001926  #°

#myfont[133] = 0x097A4C6  #Å
myfont[unicode('Å', "utf-8")] = 0x097A4C6  #Å

#myfont[132] = 0x097A4C9  #Ä
myfont[u'Ä'] = 0x097A4C9  #Ä

#myfont[150] = 0x064A4C9  #Ö
myfont[u'Ö'] = 0x064A4C9  #Ö

#myfont[165] = myfont[133]  #å
myfont[u'å'] = myfont[u'Å']  #å


#myfont[164] = myfont[132]  #ä
myfont[u'ä'] = myfont[u'Ä']  #ä

#myfont[182] = myfont[150]  #ö
myfont[u'ö'] = myfont[u'Ö']  #ö

#myfont[169] = myfont['E']  #é
myfont[u'é'] = myfont['E']  #é


#print myfont


###########################################################
## Helper function
def getledindexbydispcoords(xc, yc):

  if not((xc >= 0) and (xc < 22) and (yc >= 0) and (yc < 5)):
    return -1


  result = yc * 22 * 4
    
  if yc % 2:
    #odd row. LEDs go from right to left.
    result += ((21-xc) * 4)
  else:
    #even row. LEDs go from left to right.
    result += (xc * 4)

  return result


##########################################################
def texttoleddata(msgtext, offset):
 
  leddata = bytearray(5 * 22 *4)
  startx = offset
  maxxc = startx
  charindex = 0
  charmatrix = 0

  #Init leddata
  i = 0
  while i < (5 * 22 * 4):
    if (i % 4) == 0:
      leddata[i] = chr(0xFF) #header
#    else:
#      leddata[i] = 0
    i += 1

  for msgchar in unicode(msgtext, "utf-8"):
    #print msgchar


    if msgchar == ' ':
      #Special case: [SPACE]
      #  only advance position
      maxxc += 4
      startx = maxxc
    else:
      #Normal case: anything but [SPACE]
      
      if msgchar in myfont: ## Avoid KeyError
        charmatrix = myfont[msgchar]
      else:
        print "not in font:" + msgchar
     
      y = 0
      while y < 5:
        x = 0
        while x < 5:   
          # find x,y LED coordinates
          xc = startx + x;
          yc = y;

          #if coordinates are in bounds 
          if (xc >= 0) and (xc < 22) and (yc >= 0) and (yc < 5):
            ledindex = getledindexbydispcoords(xc, yc)
            if ledindex != -1:
              #get value from font matrix and update led data accordingly
              leddata[ledindex] = chr(0xFF)  #header
              ledindex += 1
              if (charmatrix & 1) != 0: 
                leddata[ledindex] = MAX_BRIGHTNESS  #blue
              else:
                leddata[ledindex] = 0  #blue
              ledindex += 1

              leddata[ledindex] = 0  #green
              ledindex += 1

              leddata[ledindex] = 0  #red
              ledindex += 1

          if (charmatrix & 1) != 0:
            # update max x coordinate used
            if xc > maxxc:
              maxxc = xc

          charmatrix >>= 1;
          
          x += 1
        y += 1


    #update start x coordinate
    if maxxc >= startx:
      startx = maxxc + 2

    charindex += 1 #next msgchar...
   

  return leddata


################################################################
def connect(server):
  PORT = 10013

  global s
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #global socket variable
  s.connect((server, PORT))

def transmit(leddata):
  global s
  s.sendall(leddata)

def waitforAck():
  global s
  data = s.recv(1024)
  s.close()

  recstring = "got " + repr(data) + " (len:" + str(len(data)) + ")"
  #print recstring



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

  testmsgtext = "AAA"
  testoffset = 0
  testleddata = texttoleddata(testmsgtext, testoffset)

  sendleddata(HOST, testleddata)


if __name__ == "__main__":
  main()

