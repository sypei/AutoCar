# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LIS3MDL
# This code is designed to work with the LIS3MDL_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import sys
sys.path.append("/home/pi/Desktop/I2C Devices")
import time
import SensorLibrary.Adafruit_GPIO.I2C as i2c


# I2C Address of the device
LIS3MDL_MAG_ADDRESS				= 0x1e

# LIS3MDL Magnetometer register
LIS3MDL_CTRL_REG1_M             = 0x20
LIS3MDL_CTRL_REG2_M				= 0x21
LIS3MDL_CTRL_REG3_M				= 0x22
LIS3MDL_CTRL_REG4_M				= 0x23
LIS3MDL_OUT_X_L_M				= 0x28
LIS3MDL_OUT_X_H_M				= 0x29
LIS3MDL_OUT_Y_L_M				= 0x2A
LIS3MDL_OUT_Y_H_M				= 0x2B
LIS3MDL_OUT_Z_L_M				= 0x2C
LIS3MDL_OUT_Z_H_M				= 0x2D

# Mag X/Y Axes Operating Mode
LIS3MDL_MAG_OM_LOW              = 0x00 # Low-power Mode,  ODR [Hz]: 1000, FAST_ODR: 1
LIS3MDL_MAG_OM_MEDIUM           = 0x20 # Medium-Performance Mode,  ODR [Hz]: 560, FAST_ODR: 1
LIS3MDL_MAG_OM_HIGH             = 0x40 # High-Performance Mode,  ODR [Hz]: 300, FAST_ODR: 1
LIS3MDL_MAG_OM_ULTRA_HIGH       = 0x60 # Ultra-High-Performance Mode,  ODR [Hz]: 155, FAST_ODR: 1

# Mag Datarate configuration
LIS3MDL_MAG_DR_0_625            = 0x00 # ODR = 0.625 Hz
LIS3MDL_MAG_DR_1_25				= 0x04 # ODR = 1.25 Hz
LIS3MDL_MAG_DR_2_5				= 0x08 # ODR = 2.5 Hz
LIS3MDL_MAG_DR_5				= 0x0C # ODR = 5 Hz
LIS3MDL_MAG_DR_10				= 0x10 # ODR = 10 Hz
LIS3MDL_MAG_DR_20				= 0x14 # ODR = 20 Hz
LIS3MDL_MAG_DR_40				= 0x18 # ODR = 40 Hz
LIS3MDL_MAG_DR_80				= 0x1C # ODR = 80 Hz

# Magnetic Field Full-scale selection
LIS3MDL_MAG_GAIN_4G             = 0x00 # Full scale = +/-4 Gauss, LSB first
LIS3MDL_MAG_GAIN_8G             = 0x20 # Full scale = +/-8 Gauss
LIS3MDL_MAG_GAIN_12G			= 0x40 # Full scale = +/-12 Gauss
LIS3MDL_MAG_GAIN_16G			= 0x60 # Full scale = +/-16 Gauss

# Mag Measurement Mode
LIS3MDL_MAG_MD_CONTINUOUS       = 0x00 # Continuous-Conversion Mode
LIS3MDL_MAG_MD_SINGLE           = 0x01 # Single-Conversion Mode
LIS3MDL_MAG_MD_POWER_DOWN       = 0x03 # Power-Down Mode

# Mag Z Axis Operating Mode
LIS3MDL_MAG_OMZ_LOW             = 0x00 # Low-power Mode
LIS3MDL_MAG_OMZ_MEDIUM          = 0x04 # Medium-Performance Mode
LIS3MDL_MAG_OMZ_HIGH            = 0x08 # High-Performance Mode
LIS3MDL_MAG_OMZ_ULTRA_HIGH      = 0x0C # Ultra-High-Performance Mode

class LIS3MDL():
    def __init__(self,address = LIS3MDL_MAG_ADDRESS):
        self._device =i2c.get_i2c_device(address)
        
    def mag_opmode_xy(self):
        """Select the X and Y Axes Operative Mode of the Magnetometer from the given provided values"""
        MAG_OP_MODE_XY = LIS3MDL_MAG_OM_ULTRA_HIGH
        self._device.write8(LIS3MDL_CTRL_REG1_M, MAG_OP_MODE_XY)

    def mag_datarate(self):
        """Select the data rate of the Magnetometer from the given provided values"""
        MAG_DATARATE = (LIS3MDL_MAG_DR_0_625)
        self._device.write8(LIS3MDL_CTRL_REG1_M, MAG_DATARATE)
	
    def mag_scale_selection(self):

        MAG_SCALE = (LIS3MDL_MAG_GAIN_4G)
        self._device.write8(LIS3MDL_CTRL_REG2_M, MAG_SCALE)
    
    def mag_opmode(self):
        """Select the fOperating Mode of the Magnetometer from the given provided values"""
        MAG_OP_MODE = (LIS3MDL_MAG_MD_CONTINUOUS)
        self._device.write8(LIS3MDL_CTRL_REG3_M, MAG_OP_MODE)

    def mag_opmode_z(self):
        """Select the Z Axis Operative Mode of the Magnetometer from the given provided values"""
        MAG_OP_MODE_Z = LIS3MDL_MAG_OMZ_ULTRA_HIGH
        self._device.write8(LIS3MDL_CTRL_REG4_M, MAG_OP_MODE_Z)
        
    def readmag(self):

        xMAG = self._device.readS16(LIS3MDL_OUT_X_L_M)
        yMAG = self._device.readS16(LIS3MDL_OUT_Y_L_M)
        zMAG = self._device.readS16(LIS3MDL_OUT_Z_L_M)
        return {'x' : xMAG, 'y' : yMAG, 'z' : zMAG}


