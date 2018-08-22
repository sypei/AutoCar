import time
from SensorLibrary.MPU6050 import MPU6050

imu = MPU6050()

while True:
    imu.set_accel_range(2)
    print(imu.get_accel_data())
    time.sleep(0.5)