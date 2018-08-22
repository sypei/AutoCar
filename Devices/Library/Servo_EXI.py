#!/usr/bin/python
from NatPiLib import PWM
import time
import RPi.GPIO as GPIO
# ===========================================================================
# Example Code
# Yoyo edited July. 20th
# ===========================================================================
class Servo_EXI:
    #pwm = PWM(0x40, debug=True)
    def __init__(self, channel, address, pwm_freq = 50):# the default address is 0x40
        self.address = address
        self.channel = channel
        self.servo = PWM.PWM(address)
        self.servo.setPWMFreq(pwm_freq)
        self.MAX_PWM_VAL = 4096
        self.MIN_PWM_VAL = 0
        self.MAX_PWM_Servo = 550 # mechanical restriction of servo EXI
        self.MIN_PWM_Servo = 10
        self.cur_pwm = int(0.5*(self.MAX_PWM_Servo+self.MIN_PWM_Servo))# Necessary for discontinuous rotation, unnecessary for continous rotation
        self.cur_degree = int((self.cur_pwm - 10)/540*180) 
        #self.servo.setPWM(self.channel, 0, self.cur_pwm)

    def forwards(self,step):# step should be around 10~30
        if (self.cur_pwm+step)>= self.MAX_PWM_Servo:
            target_pwm = self.MAX_PWM_Servo
        else:
            target_pwm = self.cur_pwm + step
        for i in range(self.cur_pwm,target_pwm,20):
          self.servo.setPWM(self.channel, 0, i) # chan, duty cycle is max-min/4096
          time.sleep(.01)
        self.cur_pwm = target_pwm
        self.cur_degree = int((self.cur_pwm - 10)/540*180) 
        
    def reverse(self,step):# step should be around 10~30
        if (self.cur_pwm-step)<= self.MIN_PWM_Servo:
            target_pwm = self.MIN_PWM_Servo
        else:
            target_pwm = self.cur_pwm - step
        for i in range(0,self.cur_pwm - target_pwm,20):
          self.servo.setPWM(self.channel, 0, self.cur_pwm - i) # chan, duty cycle is max-min/4096
          time.sleep(.01)
        self.cur_pwm = target_pwm
        self.cur_degree = int((self.cur_pwm - 10)/540*180)
        
    def stop(self):
        self.servo.setPWM(self.channel, 0, self.cur_pwm)
        
""" the default address
servo = PWM.PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 0  # Min pulse length out of 4096
servoMax = 550  # Max pulse length out of 4096
channel_selection = 9
# Set GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.OUT)

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print("us per period",pulseLength)
  pulseLength /= 4096                     # 12 bits of resolution
  print("us per bit", pulseLength)
  pulse *= 1000
  pulse /= pulseLength # No. of bits for pulse input
  servo.setPWM(channel, 0, pulse)

servo.setPWMFreq(60)                        # Set frequency to 60 Hz

# Change speed of continuous servo on channel O

GPIO.output(22,1)
time.sleep(1)
GPIO.output(22,0)
time.sleep(2)
GPIO.cleanup()


# Change speed of continuous servo on channel O
for i in range(servoMin,servoMax,10):
  servo.setPWM(channel_selection, 0, i) # chan, duty cycle is max-min/4096
  time.sleep(.01)
  print("forwards: ", i)
for i in range(0,servoMax - servoMin,10):
  servo.setPWM(channel_selection, 0, servoMax - i) # chan, duty cycle is max-min/4096
  time.sleep(.01)
  print("reverse: ", servoMax - i)
  
servo.setPWM(channel_selection, 0, 0)

"""





 