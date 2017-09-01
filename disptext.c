/*
$ gcc ldclient.c disptext.c -o disptext
$ ./disptext <server ip> <display text> [offset]
*/



#include <stdio.h>
#include <time.h>
#include <stdlib.h>
//#include "leddata.h"
#include "ldclient.h"
#include "ldispledconfig.h"


#define MAX_BRIGHTNESS 128 //64

static unsigned char leddata[LDISP_FRAME_SIZE] = {0};

static long int myfont[256] = {0};

// Helper function
unsigned char * getledbydispcoords(int xc, int yc)
{
  unsigned char *result = 0;

  if(!((xc >= 0) && (xc < 22) && (yc >= 0) && (yc < 5)))
  {
    return 0;
  }


  result = leddata + yc * 22 * 4; //pointer arithmetic
    
  if(yc % 2)
  {
    //odd row. LEDs go from right to left.
    result += ((21-xc) * 4); //pointer arithmetic
  }
  else
  {
    //even row. LEDs go from left to right.
    result += (xc * 4); //pointer arithmetic
  }

  return result;
}

///////////////////////////////////////////////
//
int main(int argc, char *argv[]) {

  
  int i;
  char * pleddata = 0;
  int startx = 0;
  int x, y, charindex, xc, yc, maxxc, textlength;
  long int charmatrix;
  unsigned char * pszDisplayText;
  
  if(argc < 3)
  {
    printf("usage:\n%s <server ip> <display text>\n", argv[0]);
    return -1;
  }

  //Init led data
  for(i=0; i<(LDISP_FRAME_SIZE); i++)
  {
    //leddata[i] = i % 256;
    leddata[i] = 0;
    if((i % 4) == 0)
    {
      leddata[i] = 0xFF;
    }
  }

  // Initialize font
  for(i=0; i<256; i++)
  {
    myfont[i] = 0;
  }

    //FIXME: change from 3 dots wide characters to 4 or 5 dots


/* 3 dots wide font
  myfont['A'] = 0x094BD26; 
  myfont['B'] = 0x0749D27;
  myfont['C'] = 0x0648526;
  myfont['D'] = 0x074A527;
  myfont['E'] = 0x0709C27;
  myfont['F'] = 0x0109C27;
  myfont['G'] = 0x0E68526;
  myfont['H'] = 0x0529CA5;
  myfont['I'] = 0x0108421;
  myfont['J'] = 0x064A108;
  myfont['!'] = 0x0100421;
  myfont['K'] = 0x0928CA9;
  myfont['L'] = 0x0708421;
  myfont['M'] = 0x118D771;
  myfont['N'] = 0x11CD671;

  myfont['O'] = 0x064A526;
  myfont['P'] = 0x0108CA3;
  myfont['Q'] = 0x0E6A526;
  myfont['R'] = 0x0528CA3;
  myfont['S'] = 0x074182E;
  myfont['T'] = 0x0210847;
  myfont['U'] = 0x064A529;
  myfont['V'] = 0x02294A5;
  myfont['X'] = 0x05288A5;
  myfont['Y'] = 0x02108A5;
  myfont['Z'] = 0x0708887;

  myfont['0'] = 0x07294A7;
  myfont['1'] = 0x0210843;
  myfont['2'] = 0x0709C87;
  myfont['3'] = 0x0721C87;
  myfont['4'] = 0x0421CA5;
  myfont['5'] = 0x0721C27;
  myfont['6'] = 0x0729C27;
  myfont['7'] = 0x0421087;
  myfont['8'] = 0x0729CA7;
  myfont['9'] = 0x0421CA7;
*/

/*  myfont['Å'] = 0x097A4C6;
  myfont['Ä'] = 0x097A4C9;
  myfont['Ö'] = 0x064A4C9;*/

  myfont['A'] = 0x118FE2E; 
  myfont['B'] = 0x0F8BE2F;
  myfont['C'] = 0x1E0843E;
  myfont['D'] = 0x0F8C62F;
  myfont['E'] = 0x1F0BC3F;
  myfont['F'] = 0x010BC3F;
  myfont['G'] = 0x1EC862E;
  myfont['H'] = 0x118FE31;
  myfont['I'] = 0x0108421;
  myfont['J'] = 0x0E8C210;
  myfont['!'] = 0x0100421;
  myfont['K'] = 0x0928CA9;
  myfont['L'] = 0x1F08421;
  myfont['M'] = 0x118D771;
  myfont['N'] = 0x11CD671;

  myfont['O'] = 0x0E8C62E;
  myfont['P'] = 0x010BE2F;
  myfont['Q'] = 0x164C62E;
  myfont['R'] = 0x118BE2F;
  myfont['S'] = 0x0F8383E;
  myfont['T'] = 0x042109F;
  myfont['U'] = 0x0E8C631;
  myfont['V'] = 0x0454631;
  myfont['X'] = 0x1151151;
  myfont['Y'] = 0x0421151;
  myfont['Z'] = 0x1F1111F;
//-----

  myfont['0'] = 0x0F4A52F;
  myfont['1'] = 0x0210843;
  myfont['2'] = 0x0F0BD0F;
  myfont['3'] = 0x0F43D0F;
  myfont['4'] = 0x0843D29;
  myfont['5'] = 0x0F43C2F;
  myfont['6'] = 0x0F4BC2F;
  myfont['7'] = 0x084210F;
  myfont['8'] = 0x0F4BD2F;
  myfont['9'] = 0x0843D2F;

  myfont[':'] = 0x0008020;
  myfont['.'] = 0x0100000;
  myfont['/'] = 0x0011100;

  //myfont[176] = 0x00008A2;  //°
  //myfont[176] = 0x0032526;  //°
  myfont[176] = 0x0001926;  //°

  myfont[133] = 0x097A4C6;  //Å
  myfont[132] = 0x097A4C9;  //Ä
  myfont[150] = 0x064A4C9;  //Ö

  // Set starting x coordinate
  if(argc >= 4)
  {
    startx = atoi(argv[3]);
  }
  
  maxxc = startx;
  charindex = 0;

  pszDisplayText = argv[2];

  // Get display text length
  textlength = 0;
  while(*pszDisplayText)
  {
    textlength++;
    pszDisplayText++;
  }
  pszDisplayText = argv[2];

  // For each character in displaytext...
  for(charindex = 0; charindex < textlength; charindex++)
  {
    //Get 5x5 matrix from font
    printf("%d\n", pszDisplayText[charindex]);

    //Special case: [SPACE]
    //  only advance position
    if(pszDisplayText[charindex] == ' ')
    {
      maxxc += 4;
      startx = maxxc;
      continue;
    }

    charmatrix = myfont[pszDisplayText[charindex]];

    // For each dot in matrix
    for(y = 0; y < 5; y++)
    {
      for(x = 0; x < 5; x++)
      {

        // find x,y LED coordinates
        xc = startx + x;
        yc = y;

        //if coordinates are in bounds 
        if((xc >= 0) && (xc < 22) && (yc >= 0) && (yc < 5))
        {    
          // find corresponding led data pointer
          pleddata = getledbydispcoords(xc, yc);
          if(pleddata)
          {
            // get value from matrix and update led data accordingly
            *pleddata++ = 0xFF; //header
            if(charmatrix & 1)
            {
              *pleddata++ = MAX_BRIGHTNESS; //blue
            }
            else
            {
              *pleddata++ = 0; //blue
            }
            *pleddata++ = 0; // green
            *pleddata++ = 0; // red

          }
        }

        if(charmatrix & 1)
        {
          // update max x coordinate used
          if(xc > maxxc)
          {
            maxxc = xc;
          }
        }

        charmatrix >>= 1;

      }
    }
   
    // update start x coordinate
    if(maxxc >= startx)
    {
      startx = maxxc + 2;
    }

  }//for each text character


  if(LDconnect(argv[1]))
  {
    printf("failed to connect to server\n");
    return 1;
  }

  if(LDTransmit(leddata, LDISP_FRAME_SIZE))
  {
    printf("Failed to transmit led data to server\n");
    return 3;
  }

  if(LDWaitforAck())
  {
    printf("got no ack\n");
  }

  LDDisconnect();  

  return 0;
}

