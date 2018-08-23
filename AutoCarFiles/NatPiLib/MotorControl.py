#!/usr/bin/env
from NatPiLib import PWM
import time
import RPi.GPIO as GPIO

class Motor(PWM):

    @classmethod
    def motor_init():
        # Set GPIO pins_left wheel
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        
        # Set GPIO pins_right wheel
        channel_selection_R = 8
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)

    def motor_left(left_PWM,forward):#forward when "forward" set on
        motor_init()
        channel_selection_L = 7
        if forward==1:
            GPIO.output(16, True)
            GPIO.output(18, False)
        else:
            GPIO.output(16, False)
            GPIO.output(18, True)
        motorMinL = 0  # Min pulse length out of 4096
        motorMaxL = left_PWM  # Max pulse length out of 4096
        for i in range(motorMinL,motorMaxL):
          self.setPWM(channel_selection_L, 0, i) # chan, duty cycle is max-min/4096
        
    def motor_right(right_PWM,forward):#forward when "forward" set on
        motor_init()
        channel_selection_R = 8
        if forward==1:
            GPIO.output(11, True)
            GPIO.output(12, False)
        else:
            GPIO.output(11, False)
            GPIO.output(12, True)
        motorMinR = 0  # Min pulse length out of 4096
        motorMaxR = right_PWM  # Max pulse length out of 4096
        for i in range(motorMinR,motorMaxR):
          self.setPWM(channel_selection_R, 0, i) # chan, duty cycle is max-min/4096
