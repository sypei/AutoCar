#!/usr/bin/python
import sys
sys.path.append("/home/pi/Desktop/AutoCar")
import Servo_EXI
import time
import RPi.GPIO as GPIO

#test here!

DCEngineL = Servo_EXI.Servo_EXI(9,0x70)
DCEngineR = Servo_EXI.Servo_EXI(10,0x70)
print("{} : {}  {} : {}".format("left wheel" ,DCEngineL.cur_degree,"right wheel",DCEngineR.cur_degree))
DCEngineL.forwards(200)
DCEngineR.forwards(200)
time.sleep(2)
print("{} : {}  {} : {}".format("left wheel" ,DCEngineL.cur_degree,"right wheel",DCEngineR.cur_degree))
DCEngineL.reverse(200)
DCEngineR.reverse(200)
time.sleep(2)
print("{} : {}  {} : {}".format("left wheel" ,DCEngineL.cur_degree,"right wheel",DCEngineR.cur_degree))
DCEngineL.forwards(100)
DCEngineR.forwards(100)
time.sleep(2)
print("{} : {}  {} : {}".format("left wheel" ,DCEngineL.cur_degree,"right wheel",DCEngineR.cur_degree))
DCEngineL.reverse(100)
DCEngineR.reverse(100)
print("{} : {}  {} : {}".format("left wheel" ,DCEngineL.cur_degree,"right wheel",DCEngineR.cur_degree))
time.sleep(2)

DCEngineL.stop()
DCEngineR.stop()