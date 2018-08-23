#!/usr/bin/python
import sys
sys.path.append("/home/pi/Desktop/AutoCar")
import Motor_HBB
import time
import RPi.GPIO as GPIO

#test here!

DCEngineL = Motor_HBB.Motor_HBB(16,18,7,0x70)
DCEngineR = Motor_HBB.Motor_HBB(11,12,8,0x70)

for i in range(50,100):# to avoid startup problem
    DCEngineL.forwards(i)
    DCEngineR.forwards(i)
    time.sleep(.05)
    
for i in range(50,100):
    DCEngineL.reverse(i)
    DCEngineR.reverse(i)
    time.sleep(.05)

DCEngineL.forwards(0) # to end afterwards
DCEngineR.forwards(0) 