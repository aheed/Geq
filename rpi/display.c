/* 
Low resolution display made of LED strips

Raspberry Pi
Adafruit Dotstar strip, HW SPI


$ gcc ldserver.c display.c -o display -lwiringPi -lrt -lm -lpthread
$ sudo ./display

*/


#include <stdint.h>
#include <stdio.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <time.h>
#include "ldserver.h"
#include "../ldispledconfig.h"



#define SPI_BITRATE 8000000

//255 is max but battery and rPi have power limitations
#define MAX_BRIGHTNESS 64 //128

#define SLEEP_PER_LOOP 500000 // nanoseconds

#define SPARE_LEDS 1

/*volatile*/ static uint8_t leddata[LDISP_FRAME_SIZE + SPARE_LEDS * LDISP_LED_DATA_SIZE] = {0};





// -------------------------------------------------------------------------

int main( int argc, char* args[] )
{
  int i;
  int      fd;         // File descriptor if using hardware SPI
  struct timespec sleeper, dummy;
  struct timespec resolution;
  int handledframes = 0;


  struct spi_ioc_transfer xfer[3] = {
  { .tx_buf        = 0, // Header (zeros)
    .rx_buf        = 0,
    .len           = 4,
    .delay_usecs   = 0,
    .bits_per_word = 8,
    .cs_change     = 0,
    .speed_hz = SPI_BITRATE},
  { .rx_buf        = 0, // Color payload
    //.len           = 30 * 4,  // FIXME: TEMP !!!!!!!!!!!!!!!!!!!!!!!!!!!
    .len           = (LDISP_NOF_LEDS + SPARE_LEDS) * 4,  
    .delay_usecs   = 0,
    .bits_per_word = 8,
    .cs_change     = 0,
    .speed_hz = SPI_BITRATE},
  { .tx_buf        = 0, // Footer (zeros)
    .rx_buf        = 0,
    //.len = (30 + 15) / 16,   // FIXME: TEMP!!!!!!!!!!!!!!!!!!!!
    .len = ((LDISP_NOF_LEDS + SPARE_LEDS) + 15) / 16,
    .delay_usecs   = 0,
    .bits_per_word = 8,
    .cs_change     = 0,
    .speed_hz = SPI_BITRATE}
  };


  /////////////////////////////////////////
  // initialize LED data.

  // set the extra LED to black  
  unsigned char * pchar = &(leddata[LDISP_FRAME_SIZE]);
  *pchar++ = 0xFF; //header
  *pchar++ = 0;
  *pchar++ = 0;
  *pchar   = 0;


  ///////////////////////////////////////7
  // Init SPI  
  if((fd = open("/dev/spidev0.0", O_RDWR)) < 0) {
    printf("Can't open /dev/spidev0.0 (try 'sudo')\n");
    return 2;
  }
 
  uint8_t mode = SPI_MODE_0 | SPI_NO_CS;
  ioctl(fd, SPI_IOC_WR_MODE, &mode);
  // The actual data rate may be less than requested.
  // Hardware SPI speed is a function of the system core
  // frequency and the smallest power-of-two prescaler
  // that will not exceed the requested rate.
  // e.g. 8 MHz request: 250 MHz / 32 = 7.8125 MHz.
  ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, SPI_BITRATE);

  printf("\n\n");


  //pinMode (4,  OUTPUT) ; //pin 16
  //pinMode (5, INPUT) ;  //pin 18

  // set Pin 18 to generate an interrupt on high-to-low transitions
  // FIXME: remove



  if(LDListen(leddata, LDISP_FRAME_SIZE))
  {
    fprintf (stderr, "Failed to setup server\n");
    return 1;
  }

  while(1)
  {

    //if(handledframes != LDGetReceivedFrames())
    {

        ////////////////////////////////////////
        // Transmit LED data on SPI
        xfer[1].tx_buf   = (unsigned long)leddata;
        (void)ioctl(fd, SPI_IOC_MESSAGE(3), xfer);

       handledframes = LDGetReceivedFrames();
    }
    

   // wait a while
   sleeper.tv_sec  = 0;
   sleeper.tv_nsec = SLEEP_PER_LOOP;
   nanosleep(&sleeper, &dummy);

  }
  

  /*
  // Cleanup
  if(fd) {
   close(fd);
   fd = -1;
  }
  */

  return 0;
}

