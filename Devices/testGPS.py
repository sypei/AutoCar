#Yoyo 7/19 19:19
import serial
gps = serial.Serial('/dev/ttyS0',baudrate= 9600)

while True:
    line = gps.readline()
    data = line.decode().split(",")
    if data[0] == "$GPRMC":
        if data[2] == "A":
            print ("Latitude: %s" % data[3])
            print ("Longtitude: %s" % data[5])