import SensorLibrary.Adafruit_GPIO.I2C as i2c
import sys
sys.path.append("/home/pi/Desktop/I2C Devices")
# Global Variables
GRAVITY_MS2 = 9.80665
LSM6DS33_ADDR = 0x6b
LSM6DS33_WHOAMI_ID = 0b01101001

# Pre-defined values
ODR_XL_PWR_DN = 0x0
ODR_XL_13_HZ = 0x1
ODR_XL_26_HZ = 0x2
ODR_XL_52_HZ = 0x3
ODR_XL_104_HZ = 0x4
ODR_XL_208_HZ = 0x5
ODR_XL_416_HZ = 0x6
ODR_XL_833_HZ = 0x7
ODR_XL_1660_HZ = 0x8
ODR_XL_3330_HZ = 0x9
ODR_XL_6660_HZ = 0xA

FS_XL_2G = 0b00
FS_XL_4G = 0b10
FS_XL_8G = 0b11
FS_XL_16G = 0b01

BW_XL_400_HZ = 0b00
BW_XL_200_HZ = 0b01
BW_XL_100_HZ = 0b10
BW_XL_50_HZ = 0b11

# Scale Modifiers
ACCEL_SCALE_MODIFIER_2G     = 16384.0
ACCEL_SCALE_MODIFIER_4G     = 8192.0
ACCEL_SCALE_MODIFIER_8G     = 4096.0
ACCEL_SCALE_MODIFIER_16G    = 2048.0

# LSM6DS33 Registers
WHO_AM_I = 0x0F

CTRL1_XL = 0x10 
CTRL2_G = 0x11 
CTRL3_C = 0x12 
CTRL4_C = 0x13 
CTRL5_C = 0x14 
CTRL6_C = 0x15
CTRL7_G = 0x16 
CTRL8_XL = 0x17
CTRL9_XL = 0x18
CTRL10_C = 0x19

OUT_TEMP_L = 0X20
OUT_TEMP_H = 0X21

OUTX_L_G = 0x22
OUTX_H_G = 0x23
OUTY_L_G = 0x24
OUTY_H_G = 0X25
OUTZ_L_G = 0X26
OUTZ_H_G = 0X27

OUTX_L_XL = 0x28
OUTX_H_XL = 0x29
OUTY_L_XL = 0x2A
OUTY_H_XL = 0X2B
OUTZ_L_XL = 0X2C
OUTZ_H_XL = 0X2D

class LSM6DS33:
    def __init__(self, address = LSM6DS33_ADDR):
        self._device = i2c.get_i2c_device(address)
        # Check that the MPU-6050 is connected, then enable it.
        # Default output data rate: 104 Hz (normal mode)
        if self._device.readU8(WHO_AM_I) == LSM6DS33_WHOAMI_ID:
            self._device.write8(CTRL1_XL, 0B10000000)
            self._device.write8(CTRL2_G,  0B00000100)
            self._device.write8(CTRL3_C,  0B00000100)
            
        else:
            raise RuntimeError('Failed to find the expected device ID register value, check your wiring.')

    def set_accel_output_data_rate(self, rate):
        """Sets the outut data rate (Hz) of the accelerometer. Choose from: 
            0, 13, 26, 52, 104, 208, 416, 833, 1660, 3330, 6660
        """
        # Convert int to defined ODR
        if rate == 0:
            rate = ODR_XL_PWR_DN
        elif rate == 13:
            rate = ODR_XL_13_HZ
        elif rate == 26:
            rate = ODR_XL_26_HZ
        elif rate == 52:
            rate = ODR_XL_52_HZ
        elif rate == 104:
            rate = ODR_XL_104_HZ
        elif rate == 208:
            rate = ODR_XL_208_HZ
        elif rate == 416:
            rate = ODR_XL_416_HZ
        elif rate == 833:
            rate = ODR_XL_833_HZ
        elif rate == 1660:
            rate = ODR_XL_1660_HZ
        elif rate == 3330:
            rate = ODR_XL_3330_HZ
        elif rate == 6660:
            rate = ODR_XL_6660_HZ
        else:
            print('Output data rate not defined: using 104 Hz')
            rate = ODR_XL_104_HZ
        
        # Read original register value
        rg_val = self.read_accel_output_data_rate(True)
        
        # First change it to 0 to make sure we write the correct value later
        self._device.write8(CTRL1_XL, 0x0F & rg_val)

        # Write the new range to the ACCEL_CONFIG register
        self._device.write8(CTRL1_XL, rate << 4 | rg_val)
        
    def read_accel_output_data_rate(self, raw = False):
        """Reads the output data rate the accelerometer is set to.
        If raw is True, it will return the raw value from the ACCEL_CONFIG
        register
        If raw is False, it will return an integer: -1, 0, 13, 26, 52, 104, 208, 
        416, 833, 1660, 3330, 6660. When it returns -1 something went wrong.
        """
        # Get the raw value
        raw_data = (self._device.readU8(CTRL1_XL)) >> 4 & 0x0F

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == ODR_XL_PWR_DN:
                return 0
            elif raw_data == ODR_XL_13_HZ:
                return 13
            elif raw_data == ODR_XL_26_HZ:
                return 26
            elif raw_data == ODR_XL_52_HZ:
                return 52
            elif raw_data == ODR_XL_104_HZ:
                return 104
            elif raw_data == ODR_XL_208_HZ:
                return 208
            elif raw_data == ODR_XL_416_HZ:
                return 416
            elif raw_data == ODR_XL_833_HZ:
                return 833
            elif raw_data == ODR_XL_1660_HZ:
                return 1660
            elif raw_data == ODR_XL_3330_HZ:
                return 3330
            elif raw_data == ODR_XL_6660_HZ:
                return 6660
            else:
                return -1

    def set_accel_range(self, accel_range):
        """Sets the range of the accelerometer. Choose from: 
            2, 4, 8, 16
        """
        # Convert int to defined ODR
        if accel_range == 2:
            accel_range = FS_XL_2G
        elif accel_range == 4:
            accel_range = FS_XL_4G
        elif accel_range == 8:
            accel_range = FS_XL_8G
        elif accel_range == 16:
            accel_range = FS_XL_16G
        else:
            print('Range not defined: using +/- 2G')
            accel_range = FS_XL_2G
        
        # Read original register value
        rg_val = self.read_accel_range(True)
        
        # First change it to 0 to make sure we write the correct value later
        self._device.write8(CTRL1_XL, 0xF3 & rg_val)

        # Write the new range to the ACCEL_CONFIG register
        self._device.write8(CTRL1_XL, accel_range << 2 | rg_val)
        
    def read_accel_range(self, raw = False):
        """Reads the range the accelerometer is set to.
        If raw is True, it will return the raw value from the ACCEL_CONFIG
        register
        If raw is False, it will return an integer: -1, 2, 4, 8 or 16. When it
        returns -1 something went wrong.
        """
        # Get the raw value
        raw_data = (self._device.readU8(CTRL1_XL) >> 2) & 0x03

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == FS_XL_2G:
                return 2
            elif raw_data == FS_XL_4G:
                return 4
            elif raw_data == FS_XL_8G:
                return 8
            elif raw_data == FS_XL_16G:
                return 16
            else:
                return -1
        
    def set_accel_bandwith(self, bandwidth):
        """Sets the anti-aliasing filter bandwidth (Hz) of the accelerometer. Choose from: 
            50, 100, 200, 400
        """
        # Convert int to defined ODR
        if bandwidth == 50:
            bandwidth = BW_XL_50_HZ
        elif bandwidth == 100:
            bandwidth = BW_XL_100_HZ
        elif bandwidth == 200:
            bandwidth = BW_XL_200_HZ
        elif bandwidth == 400:
            bandwidth = BW_XL_400_HZ
        else:
            print('Bandwidth not defined: using 400 Hz')
            bandwidth = BW_XL_400_HZ
        
        # Read original register value
        rg_val = self.read_accel_output_data_rate(True)
        
        # First change it to 0 to make sure we write the correct value later
        self._device.write8(CTRL1_XL, 0xFC & rg_val)

        # Write the new range to the ACCEL_CONFIG register
        self._device.write8(CTRL1_XL, bandwidth | rg_val)
        
    def read_accel_bandwidth(self, raw = False):
        """Reads the anti-aliasing filter bandwidth the accelerometer is set to.
        If raw is True, it will return the raw value from the ACCEL_CONFIG
        register
        If raw is False, it will return an integer: -1, 50, 100, 200, 400. When it
        returns -1 something went wrong.
        """
        # Get the raw value
        raw_data = self._device.readU8(CTRL1_XL)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == BW_XL_50_HZ:
                return 50
            elif raw_data == BW_XL_100_HZ:
                return 100
            elif raw_data == BW_XL_200_HZ:
                return 200
            elif raw_data == BW_XL_400_HZ:
                return 400
            else:
                return -1
            
    def get_temp(self):
        """Reads the temperature from the onboard temperature sensor of the MPU-6050.
        Returns the temperature in degrees Celcius.
        """
        # Get the raw data
        raw_temp = self._device.readS16(OUT_TEMP_L)

        # Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        #actual_temp = (raw_temp / 340) + 36.53

        # Return the temperature
        return raw_temp
    
    def get_accel_data(self, g = False):
        """Gets and returns the X, Y and Z values from the accelerometer.
        If g is True, it will return the data in g
        If g is False, it will return the data in m/s^2
        Returns a dictionary with the measurement results.
        """
        # Read the data from the MPU-6050
        x = self._device.readS16BE(OUTX_L_XL)
        y = self._device.readS16BE(OUTY_L_XL)
        z = self._device.readS16BE(OUTZ_L_XL)

        accel_scale_modifier = None
        accel_range = self.read_accel_range(True)

        if accel_range == FS_XL_2G:
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_2G
        elif accel_range == FS_XL_4G:
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_4G
        elif accel_range == FS_XL_8G:
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_8G
        elif accel_range == FS_XL_16G:
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_16G
        else:
            print("Unknown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_2G

        x = x / accel_scale_modifier
        y = y / accel_scale_modifier
        z = z / accel_scale_modifier

        if g is True:
            return {'x': x, 'y': y, 'z': z}
        elif g is False:
            x = x * GRAVITY_MS2
            y = y * GRAVITY_MS2
            z = z * GRAVITY_MS2
            return {'x': x, 'y': y, 'z': z}
    
"""
b.write_byte_data(LSM, CTRL_1, 0b1100111) # enable accelerometer, 100 hz sampling
b.write_byte_data(LSM, CTRL_2, 0b0000000) #set +- 2g full scale page 36 datasheet
b.write_byte_data(LSM, CTRL_5, 0b01100100) #high resolution mode, thermometer off, 6.25hz ODR
b.write_byte_data(LSM, CTRL_6, 0b00100000) # set +- 4 gauss full scale
b.write_byte_data(LSM, CTRL_7, 0x00) #get magnetometer out of low power mode

b.write_byte_data(LGD, LGD_CTRL_1, 0x0F) #turn on gyro and set to normal mode
b.write_byte_data(LGD, LGD_CTRL_4, 0b00110000) #set 2000 dps full scale

DT = 1
PI = 3.14159265358979323846
RAD_TO_DEG = 57.29578
AA = 0.98
gyrox_angle = 0.0
gyroy_angle = 0.0
gyroz_angle = 0.0
CFangx = 0.0
CFangy = 0.0

while True:
    now = time.clock()
    magx = twos_comp_combine(b.read_byte_data(LSM, MAG_X_MSB), b.read_byte_data(LSM, MAG_X_LSB))
    magy = twos_comp_combine(b.read_byte_data(LSM, MAG_Y_MSB), b.read_byte_data(LSM, MAG_Y_LSB))
    magz = twos_comp_combine(b.read_byte_data(LSM, MAG_Z_MSB), b.read_byte_data(LSM, MAG_Z_LSB))

    #print "Magnetic field (x, y, z):", magx, magy, magz

    accx = twos_comp_combine(b.read_byte_data(LSM, ACC_X_MSB), b.read_byte_data(LSM, ACC_X_LSB))
    accy = twos_comp_combine(b.read_byte_data(LSM, ACC_Y_MSB), b.read_byte_data(LSM, ACC_Y_LSB))
    accz = twos_comp_combine(b.read_byte_data(LSM, ACC_Z_MSB), b.read_byte_data(LSM, ACC_Z_LSB))
    accx = accx * 0.061 * 0.001
    accy = accy * 0.061 * 0.001
    accz = accz * 0.061 * 0.001 - 0.1


    print ("Acceleration (x, y, z):", accx, accy, accz)

    gyrox = twos_comp_combine(b.read_byte_data(LGD, LGD_GYRO_X_MSB), b.read_byte_data(LGD, LGD_GYRO_X_LSB))
    gyroy = twos_comp_combine(b.read_byte_data(LGD, LGD_GYRO_Y_MSB), b.read_byte_data(LGD, LGD_GYRO_Y_LSB))
    gyroz = twos_comp_combine(b.read_byte_data(LGD, LGD_GYRO_Z_MSB), b.read_byte_data(LGD, LGD_GYRO_Z_LSB))
    
    #print "Gyroscope (x, y, z):", gyrox, gyroy, gyroz
    rate_gyrox = gyrox * 0.07
    rate_gyroy = gyroy * 0.07
    rate_gyroz = gyroz * 0.07
    
    gyrox_angle+=rate_gyrox*DT
    gyroy_angle+=rate_gyroy*DT
    gyroz_angle+=rate_gyroz*DT;
    
    #accx_angle = (math.atan2(accy,math.sqrt(accx*accx+accz*accz))+PI)*RAD_TO_DEG
    accx_angle = (math.atan2(accy,accz))*RAD_TO_DEG
    #accx_angle = (math.atan2(accy,accz)+PI)*RAD_TO_DEG
    #accy_angle = (math.atan2(accx,math.sqrt(accy*accy+accz*accz))+PI)*RAD_TO_DEG
    accy_angle = (math.atan2(-accx,accz))*RAD_TO_DEG
    #accy_angle = (math.atan2(accz,accx)+PI)*RAD_TO_DEG
    
    CFangx = AA*(CFangx+rate_gyrox*DT) +(1 - AA) * accx_angle;
    CFangy = AA*(CFangy+rate_gyroy*DT) +(1 - AA) * accy_angle;

    print ("Angle = ", CFangx, CFangy) # accx_angle,accy_angle #
    while (time.clock() <= now + DT):
        pass"""