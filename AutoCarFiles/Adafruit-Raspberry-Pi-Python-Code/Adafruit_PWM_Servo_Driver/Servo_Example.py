#!/usr/bin/python

from NatPiLib import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
servo = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 4096  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print("%d us per period", pulseLength)
  pulseLength /= 4096                     # 12 bits of resolution
  print("%d us per bit", pulseLength)
  pulse *= 1000
  pulse /= pulseLength
  servo.setPWM(channel, 0, pulse)

servo.setPWMFreq(60)                        # Set frequency to 60 Hz
counter = 0
while (True):
  # Change speed of continuous servo on channel O
  servo.setPWM(4, counter, servoMax)
  time.sleep(.05)
  counter = counter + 1
  
  if counter > 599:
      counter = 0


