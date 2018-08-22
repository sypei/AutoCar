#!/usr/bin/python
from NatPiLib import PWM
import time
import RPi.GPIO as GPIO

# ===========================================================================
# Example Code
# Yoyo edited July. 20th
# ===========================================================================
class Motor_HBB:
    
    # Note if you'd like more debug output you can instead run:
    #pwm = PWM(0x40, debug=True)
    def __init__(self,forwardsPin, reversePin, channel, address, pwm_freq = 50):
        # Set GPIO pins_Direction
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(forwardsPin, GPIO.OUT)
        GPIO.setup(reversePin, GPIO.OUT)
        # Store all arguments
        self.address = address
        self.forwardsPin = forwardsPin
        self.reversePin = reversePin
        self.channel = channel
        self.motor = PWM.PWM(address)
        self.motor.setPWMFreq(pwm_freq)
        self.MAX_PWM_VAL = 4096
        self.MIN_PWM_VAL = 0

    def forwards(self,percent_max): # percent_max is a value 0~100
        speed_pwm = int(percent_max / 100 * self.MAX_PWM_VAL)# Values are 0 to MAX_PWM_VAL
        GPIO.output(self.forwardsPin, True)
        GPIO.output(self.reversePin, False)
        self.motor.setPWM(self.channel, 0, speed_pwm)
        
    def reverse(self,percent_max): # percent_max is a value 0~100
        speed_pwm = int(percent_max / 100 * self.MAX_PWM_VAL) # Values are 0 to MAX_PWM_VAL
        GPIO.output(self.forwardsPin, False)
        GPIO.output(self.reversePin, True)
        self.motor.setPWM(self.channel, 0, speed_pwm)
        
