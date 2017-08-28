/*
$ gcc ldclient.c eqclient.c -o eqclient
$ ./eqclient <server ip>
*/



#include <stdio.h>
#include <time.h>
#include "ldclient.h"
#include "ldispledconfig.h"


#define MAX_BRIGHTNESS 255 //64

static unsigned char leddata[LDISP_FRAME_SIZE * 2] = {0}; //2 ch stereo


///////////////////////////////////////////////
//
int main(int argc, char *argv[]) {
  
  int i, j;
  unsigned char* pChar;
  int row, column, level;
  int threshold;

  //FIXME: array size should be a define.
  //       Number of frequency bands (16) * number of channels (2)
  static unsigned int levels[16 * 2];
//  static const unsigned char thresholds[LDISP_ROWS];
  
  if(argc < 2)
  {
    printf("usage:\n%s <server ip>\n", argv[0]);
    return -1;
  }

  //Init fake led data
  for(i=0; i<(LDISP_FRAME_SIZE); i++)
  {
    leddata[i] = i % 256;
    if((i % 4) == 0)
    {
      leddata[i] = 0xFF;
    }
  }

  if(LDconnect(argv[1]))
  {
    printf("failed to connect to server\n");
    return 1;
  }

  /*// Initialize threshold levels
  for(i=0; i < LDISP_ROWS; i++)
  {
    thresholds[i] = (256 * i) / LDISP_ROWS;
  }*/

  printf("1\n");
  while(1)
  //for(j=0; j<4; j++)
  {
    //printf("2\n");
    scanf("%x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x\n", 
          &(levels[0]), &(levels[1]), &(levels[2]), &(levels[3]),
          &(levels[4]), &(levels[5]), &(levels[6]), &(levels[7]), 
          &(levels[8]), &(levels[9]), &(levels[10]), &(levels[11]),
          &(levels[12]), &(levels[13]), &(levels[14]), &(levels[15]),
          &(levels[16]), &(levels[17]), &(levels[18]), &(levels[19]),
          &(levels[20]), &(levels[21]), &(levels[22]), &(levels[23]), 
          &(levels[24]), &(levels[25]), &(levels[26]), &(levels[27]),
          &(levels[28]), &(levels[29]), &(levels[30]), &(levels[31]));

    //printf("%d %d %d %d\n",  levels[0], levels[1], levels[15], levels[31]);

    pChar = leddata;
    row = LDISP_ROWS - 1;
    column = 0;

    const int a = 20; // fuzziness constant
    threshold = 255 - a;
    const int thresholdStep = (255-2*a) / 17;

    //level = 0;
    for(i=0; i<(LDISP_NOF_LEDS); i++)
    {      

      *pChar++ = 0xFF; //header bits
      *pChar++ = 0; //blue
     
      if(((column %2) == 1) || (column > 18))
      {
        level = 0;
      }
      else
      {
        //level = levels[2*column] + levels[2*column+1]; // add left and right channels
        level = levels[column] > levels[column+1] ? levels[column] : levels[column + 1]; //max of left and right
        if(level > 255)
        {
          level = 255;
        }
      }

      /* //Simple implementation 
      threshold = (256 * row) / LDISP_ROWS + 1;       
      *pChar++ = level >= threshold ? 0xFF : 0; //green
      */

      /* // Implementation with more fuzz
      float x = level - threshold;
      float y = (x / a + 1) / 2;
      if(y < 0)
      {
         y = 0;
      }
      else if (y > 1.0)
      {
         y = 1.0;
      }
      *pChar++ = y * 0xFF; //green
      */

      // Implementation with fuzz, 5 long bars
      threshold = a + thresholdStep * column;
      if(column > 19)
      {
        level = 0;
      }
      else
      {
        level = levels[(LDISP_ROWS - 1 - row) * 4]; // only left channel, only every 4th freq band

        if(level > 255)
        {
          level = 255;
        }
      }

      float x = level - threshold;
      float y = (x / a + 1) / 2;
      if(y < 0)
      {
        y = 0;
      }
      else if (y > 1.0)
      {
        y = 1.0;
      }
      *pChar++ = y * 0xFF; //green
      

      *pChar++ = 0x1f; //red
  //    printf("row:%d col:%d level:%d thresh:%d\n", row, column, level, threshold);

      if((row % 2) == 1)
      {
        column--;
        if(column < 0)
        {
          row--;
          threshold -= (255-2*a) / 4;
          column = 0;
        }
      }
      else
      {
        column++;
        if(column >= LDISP_COLS)
        {
          row--;
          threshold -= (255-2*a) / 4;
          column = LDISP_COLS - 1;
        }
      }

    }

    if(LDTransmit(leddata, LDISP_FRAME_SIZE))
    {
       printf("Failed to transmit led data to server\n");
      return 3;
    }

    /*if(LDWaitforAck())
    {
      printf("got no ack\n");
    }*/
  }

  LDDisconnect();  

  return 0;
}

