import SensorLibrary.Adafruit_GPIO.I2C as i2c

# Global Variables
GRAVITY_MS2 = 9.80665
MPU6050_ADDR = 0x68

# Pre-defined ranges
ACCEL_RANGE_2G  = 0x00
ACCEL_RANGE_4G  = 0x08
ACCEL_RANGE_8G  = 0x10
ACCEL_RANGE_16G = 0x18

GYRO_RANGE_250DEG   = 0x00
GYRO_RANGE_500DEG   = 0x08
GYRO_RANGE_1000DEG  = 0x10
GYRO_RANGE_2000DEG  = 0x18

# Scale Modifiers
ACCEL_SCALE_MODIFIER_2G     = 16384.0
ACCEL_SCALE_MODIFIER_4G     = 8192.0
ACCEL_SCALE_MODIFIER_8G     = 4096.0
ACCEL_SCALE_MODIFIER_16G    = 2048.0

GYRO_SCALE_MODIFIER_250DEG  = 131.0
GYRO_SCALE_MODIFIER_500DEG  = 65.5
GYRO_SCALE_MODIFIER_1000DEG = 32.8
GYRO_SCALE_MODIFIER_2000DEG = 16.4

# MPU-6050 Registers
PWR_MGMT_1 = 0x6B
PWR_MGMT_2 = 0x6C

SELF_TEST_X = 0x0D
SELF_TEST_Y = 0x0E
SELF_TEST_Z = 0x0F
SELF_TEST_A = 0x10

ACCEL_XOUT0 = 0x3B
ACCEL_XOUT1 = 0x3C
ACCEL_YOUT0 = 0x3D
ACCEL_YOUT1 = 0x3E
ACCEL_ZOUT0 = 0x3F
ACCEL_ZOUT1 = 0x40

TEMP_OUT0 = 0x41
TEMP_OUT1 = 0x42

GYRO_XOUT0 = 0x43
GYRO_XOUT1 = 0x44
GYRO_YOUT0 = 0x45
GYRO_YOUT1 = 0x46
GYRO_ZOUT0 = 0x47
GYRO_ZOUT1 = 0x48

ACCEL_CONFIG = 0x1C
GYRO_CONFIG = 0x1B

WHO_AM_I = 0x75

class MPU6050:
    def __init__(self, address = MPU6050_ADDR):
        self._device = i2c.get_i2c_device(address)
        # Check that the MPU-6050 is connected, then enable it.
        if self._device.readU8(WHO_AM_I) == address:
            self._device.write8(PWR_MGMT_1, 0x00)
        else:
            raise RuntimeError('Failed to find the expected device ID register value, check your wiring.')

    def get_temp(self):
        """Reads the temperature from the onboard temperature sensor of the MPU-6050.
        Returns the temperature in degrees Celcius.
        """
        # Get the raw data
        raw_temp = self._device.readS16BE(TEMP_OUT0)

        # Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        actual_temp = (raw_temp / 340) + 36.53

        # Return the temperature
        return actual_temp

    def set_accel_range(self, accel_range):
        """Sets the range of the accelerometer to range.
        accel_range -- the range to set the accelerometer to. Using a
        pre-defined range is advised.
            2: +/- 2G,
            4: +/- 4G,
            8: +/- 8G,
            16: +/- 16G
        """
        # Convert int to defined range value
        if accel_range == 2:
            accel_range = ACCEL_RANGE_2G
        elif accel_range == 4:
            accel_range = ACCEL_RANGE_4G
        elif accel_range == 8:
            accel_range = ACCEL_RANGE_4G
        elif accel_range == 16:
            accel_range = ACCEL_RANGE_4G
        else:
            print('Range not defined: using +/- 2G')
            accel_range = ACCEL_RANGE_2G
        
        # First change it to 0x00 to make sure we write the correct value later
        self._device.write8(ACCEL_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self._device.write8(ACCEL_CONFIG, accel_range)

    def read_accel_range(self, raw = False):
        """Reads the range the accelerometer is set to.
        If raw is True, it will return the raw value from the ACCEL_CONFIG
        register
        If raw is False, it will return an integer: -1, 2, 4, 8 or 16. When it
        returns -1 something went wrong.
        """
        # Get the raw value
        raw_data = self._device.readU8(ACCEL_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == ACCEL_RANGE_2G:
                return 2
            elif raw_data == ACCEL_RANGE_4G:
                return 4
            elif raw_data == ACCEL_RANGE_8G:
                return 8
            elif raw_data == ACCEL_RANGE_16G:
                return 16
            else:
                return -1

    def get_accel_data(self, g = False):
        """Gets and returns the X, Y and Z values from the accelerometer.
        If g is True, it will return the data in g
        If g is False, it will return the data in m/s^2
        Returns a dictionary with the measurement results.
        """
        # Read the data from the MPU-6050
        x = self._device.readS16BE(ACCEL_XOUT0)
        y = self._device.readS16BE(ACCEL_YOUT0)
        z = self._device.readS16BE(ACCEL_ZOUT0)

        accel_scale_modifier = None
        accel_range = self.read_accel_range(True)

        if accel_range == ACCEL_RANGE_2G:
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_2G
        elif accel_range == ACCEL_RANGE_4G:
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_4G
        elif accel_range == ACCEL_RANGE_8G:
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_8G
        elif accel_range == ACCEL_RANGE_16G:
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

    def set_gyro_range(self, gyro_range):
        """Sets the range of the gyroscope to range.
        gyro_range -- the range to set the gyroscope to. Using a pre-defined
        range is advised.
            GYRO_RANGE_250DEG   = +/- 250DEG/s
            GYRO_RANGE_500DEG   = +/- 500DEG/s
            GYRO_RANGE_1000DEG  = +/- 1000DEG/s
            GYRO_RANGE_2000DEG  = +/- 2000DEG/s
        """
        # Convert int to defined range value
        if gyro_range == 250:
            gyro_range = GYRO_RANGE_250DEG
        elif gyro_range == 500:
            gyro_range = GYRO_RANGE_500DEG
        elif gyro_range == 1000:
            gyro_range = GYRO_RANGE_1000DEG
        elif gyro_range == 2000:
            gyro_range = GYRO_RANGE_2000DEG
        else:
            print('Range not defined: using +/- 250DEG/s')
            gyro_range = GYRO_RANGE_250DEG
        
        # First change it to 0x00 to make sure we write the correct value later
        self._device.write8(GYRO_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self._device.write8(GYRO_CONFIG, gyro_range)

    def read_gyro_range(self, raw = False):
        """Reads the range the gyroscope is set to.
        If raw is True, it will return the raw value from the GYRO_CONFIG
        register.
        If raw is False, it will return 250, 500, 1000, 2000 or -1. If the
        returned value is equal to -1 something went wrong.
        """
        # Get the raw value
        raw_data = self._device.readU8(GYRO_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == GYRO_RANGE_250DEG:
                return 250
            elif raw_data == GYRO_RANGE_500DEG:
                return 500
            elif raw_data == GYRO_RANGE_1000DEG:
                return 1000
            elif raw_data == GYRO_RANGE_2000DEG:
                return 2000
            else:
                return -1

    def get_gyro_data(self):
        """Gets and returns the X, Y and Z values from the gyroscope.
        Returns the read values in a dictionary.
        """
        # Read the raw data from the MPU-6050
        x = self._device.readS16BE(GYRO_XOUT0)
        y = self._device.readS16BE(GYRO_YOUT0)
        z = self._device.readS16BE(GYRO_ZOUT0)

        gyro_scale_modifier = None
        gyro_range = self.read_gyro_range(True)

        if gyro_range == GYRO_RANGE_250DEG:
            gyro_scale_modifier = GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == GYRO_RANGE_500DEG:
            gyro_scale_modifier = GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == GYRO_RANGE_1000DEG:
            gyro_scale_modifier = GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == GYRO_RANGE_2000DEG:
            gyro_scale_modifier = GYRO_SCALE_MODIFIER_2000DEG
        else:
            print("Unknown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            gyro_scale_modifier = GYRO_SCALE_MODIFIER_250DEG

        x = x / gyro_scale_modifier
        y = y / gyro_scale_modifier
        z = z / gyro_scale_modifier

        return {'x': x, 'y': y, 'z': z}

    def get_all_data(self):
        """Reads and returns all the available data."""
        temp = self.get_temp()
        accel = self.get_accel_data()
        gyro = self.get_gyro_data()

        return [accel, gyro, temp]