import time
from SensorLibrary.ADXL345 import ADXL345

accel = ADXL345()

while True:
    x, y, z = accel.read()
    print('X={0}, Y={1}, Z={2}'.format(x, y, z))
    time.sleep(0.5)