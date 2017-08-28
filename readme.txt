



To show visual effects of whatever is played on Spotify (standard ffmpeg msut be installed):
ffplay -f pulse -i alsa_output.pci-0000_00_1f.3.hdmi-stereo-extra1.monitor


To find name of device:
LANG=C pactl list | grep -A2 'Source #' | grep 'Name: ' | cut -d" " -f2

You should get output something like this:
alsa_input.pci-0000_00_1f.3.analog-stereo
alsa_output.pci-0000_00_1f.3.hdmi-stereo-extra1.monitor


Interfaces:

  cmd line interface:
    sequence of space separated (8bit?) hex numbers, one per channel/frequency band combo
        Preconfigured params (hard coded in define)
          number of channels
          number of frequency bands

  TCP socket:
   Magic number followed by LED data in DotStar format.
   Sequence of values must be according to LED array geometry.



To do:
  Move ldserver.h/.c from sim dir to common dir
  (Check timing/averaging)
  (Check ffplay output. Looks not so good.)
  Rearrange LED order to snakestyle*
  Scrolling text client
  Make Spectrum client "record" music indefinitely
  Make Spectrum client start "recording" from *.monitor device on startup
  Try the modified ffplay approach again but skip all but the lowest 1000 Hz
    Use max (like the Qt Spectrum app) instead of average for each frequency band?

feature:
  adaptive display level



