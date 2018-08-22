import time
import SensorLibrary.Adafruit_GPIO.I2C as i2c


# Register and other configuration values:
ADS1115_DEFAULT_ADDRESS        = 0x48
ADS1115_POINTER_CONVERSION     = 0x00
ADS1115_POINTER_CONFIG         = 0x01
ADS1115_POINTER_LOW_THRESHOLD  = 0x02
ADS1115_POINTER_HIGH_THRESHOLD = 0x03
ADS1115_CONFIG_OS_SINGLE       = 0x8000
ADS1115_CONFIG_MUX_OFFSET      = 12
# Maping of gain values to config register values.
ADS1115_CONFIG_GAIN = {
    2/3: 0x0000,
    1:   0x0200,
    2:   0x0400,
    4:   0x0600,
    8:   0x0800,
    16:  0x0A00
}
ADS1115_CONFIG_MODE_CONTINUOUS  = 0x0000
ADS1115_CONFIG_MODE_SINGLE      = 0x0100
# Mapping of data/sample rate to config register values for ADS1015 (faster).
ADS1015_CONFIG_DR = {
    128:   0x0000,
    250:   0x0020,
    490:   0x0040,
    920:   0x0060,
    1600:  0x0080,
    2400:  0x00A0,
    3300:  0x00C0
}
# Mapping of data/sample rate to config register values for ADS1115 (slower).
ADS1115_CONFIG_DR = {
    8:    0x0000,
    16:   0x0020,
    32:   0x0040,
    64:   0x0060,
    128:  0x0080,
    250:  0x00A0,
    475:  0x00C0,
    860:  0x00E0
}
ADS1115_CONFIG_COMP_WINDOW      = 0x0010     #bit[4] = 1 COM_MODE
ADS1115_CONFIG_COMP_ACTIVE_HIGH = 0x0008     #bit[3] = 1 active high
ADS1115_CONFIG_COMP_LATCHING    = 0x0004     #bit[2] = 1 latching comparator
#assert after n converstions
ADS1115_CONFIG_COMP_QUE = {
    1: 0x0000,
    2: 0x0001,
    4: 0x0002
}
ADS1x15_CONFIG_COMP_QUE_DISABLE = 0x0003


class ADS1115:
    """Base functionality for ADS1x15 analog to digital converters."""
    def __init__(self, address = ADS1115_DEFAULT_ADDRESS):
      self._device = i2c.get_i2c_device(address)
    
    def _data_rate_default(self):
      # Default from datasheet page 16, config register DR bit default.
      return 128

    def _data_rate_config(self, data_rate):
      if data_rate not in ADS1115_CONFIG_DR:
          raise ValueError('Data rate must be one of: 8, 16, 32, 64, 128, 250, 475, 860')
      return ADS1115_CONFIG_DR[data_rate]

#    def _conversion_value(self, low, high):
#      # Convert to 16-bit signed value.
#      value = ((high & 0xFF) << 8) | (low & 0xFF)
#      # Check for sign bit and turn into a negative value if set.
#      if value & 0x8000 != 0:
#        value -= 1 << 16
#      return value

      
    def _read(self, mux, gain, data_rate, mode):
        """Perform an ADC read with the provided mux, gain, data_rate, and mode
        values.  Returns the signed integer result of the read.
        """
        config = ADS1115_CONFIG_OS_SINGLE  # Go out of power-down mode for conversion.
        # Specify mux value.
        config |= (mux & 0x07) << ADS1115_CONFIG_MUX_OFFSET   #offset = 12([2:0] to [14:12] )
        # Validate the passed in gain and then set it in the config.
        #bit[7:5] control the data rate setting
        if gain not in ADS1115_CONFIG_GAIN:
            raise ValueError('Gain must be one of: 2/3, 1, 2, 4, 8, 16')
        config |= ADS1115_CONFIG_GAIN[gain]
        # Set the mode (continuous or single shot).
        config |= mode
        # Get the default data rate if none is specified (default differs between
        # ADS1015 and ADS1115).
        if data_rate is None:
            data_rate = self._data_rate_default()
       
        config |= self._data_rate_config(data_rate)
        config |= ADS1x15_CONFIG_COMP_QUE_DISABLE  # Disble comparator mode.
        # Send the config value to start the ADC conversion.
        # Explicitly break the 16-bit value down to a big endian pair of bytes.
        self._device.writeList(ADS1115_POINTER_CONFIG, [(config >> 8) & 0xFF, config & 0xFF])
        # Wait for the ADC sample to finish based on the sample rate plus a
        # small offset to be sure (0.1 millisecond).
        time.sleep(1.0/data_rate+0.0001)
        # Retrieve the result.
        result = self._device.readS16BE(ADS1115_POINTER_CONVERSION)
        return result

    def _read_comparator(self, mux, gain, data_rate, mode, high_threshold,
                         low_threshold, active_low, traditional, latching,
                         num_readings):
        """Perform an ADC read with the provided mux, gain, data_rate, and mode
        values and with the comparator enabled as specified.  Returns the signed
        integer result of the read.
        """
        assert num_readings == 1 or num_readings == 2 or num_readings == 4, 'Num readings must be 1, 2, or 4!'
        # Set high and low threshold register values.
        self._device.writeList(ADS1115_POINTER_HIGH_THRESHOLD, [(high_threshold >> 8) & 0xFF, high_threshold & 0xFF])
        self._device.writeList(ADS1115_POINTER_LOW_THRESHOLD, [(low_threshold >> 8) & 0xFF, low_threshold & 0xFF])
        # Now build up the appropriate config register value.
        config = ADS1115_CONFIG_OS_SINGLE  # Go out of power-down mode for conversion.
        # Specify mux value.
        config |= (mux & 0x07) << ADS1115_CONFIG_MUX_OFFSET
        # Validate the passed in gain and then set it in the config.
        if gain not in ADS1115_CONFIG_GAIN:
            raise ValueError('Gain must be one of: 2/3, 1, 2, 4, 8, 16')
        config |= ADS1115_CONFIG_GAIN[gain]
        # Set the mode (continuous or single shot).
        config |= mode
        # Get the default data rate if none is specified (default differs between
        # ADS1015 and ADS1115).
        if data_rate is None:
            data_rate = self._data_rate_default()
        # Set the data rate (this is controlled by the subclass as it differs
        # between ADS1015 and ADS1115).
        config |= self._data_rate_config(data_rate)
        # Enable window mode if required.
        if not traditional:
            config |= ADS1115_CONFIG_COMP_WINDOW
        # Enable active high mode if required.
        if not active_low:
            config |= ADS1115_CONFIG_COMP_ACTIVE_HIGH
        # Enable latching mode if required.
        if latching:
            config |= ADS1115_CONFIG_COMP_LATCHING
        # Set number of comparator hits before alerting.
        config |= ADS1115_CONFIG_COMP_QUE[num_readings]
        # Send the config value to start the ADC conversion.
        # Explicitly break the 16-bit value down to a big endian pair of bytes.
        self._device.writeList(ADS1115_POINTER_CONFIG, [(config >> 8) & 0xFF, config & 0xFF])
        # Wait for the ADC sample to finish based on the sample rate plus a
        # small offset to be sure (0.1 millisecond).
        time.sleep(1.0/data_rate+0.0001)
        # Retrieve the result.
        result = readS16BE(ADS1115_POINTER_CONVERSION)
        return result

    def read_adc(self, channel, gain=1, data_rate=None):
        """Read a single ADC channel and return the ADC value as a signed integer
        result.  Channel must be a value within 0-3.
        """
        assert 0 <= channel <= 3, 'Channel must be a value within 0-3!'
        # Perform a single shot read and set the mux value to the channel plus
        # the highest bit (bit 3) set.
        return self._read(channel + 0x04, gain, data_rate, ADS1115_CONFIG_MODE_SINGLE)

    def read_adc_difference(self, differential, gain=1, data_rate=None):
        """Read the difference between two ADC channels and return the ADC value
        as a signed integer result.  Differential must be one of:
          - 0 = Channel 0 minus channel 1
          - 1 = Channel 0 minus channel 3
          - 2 = Channel 1 minus channel 3
          - 3 = Channel 2 minus channel 3
        """
        assert 0 <= differential <= 3, 'Differential must be a value within 0-3!'
        # Perform a single shot read using the provided differential value
        # as the mux value (which will enable differential mode).
        return self._read(differential, gain, data_rate, ADS1115_CONFIG_MODE_SINGLE)

    def start_adc(self, channel, gain=1, data_rate=None):
        """Start continuous ADC conversions on the specified channel (0-3). Will
        return an initial conversion result, then call the get_last_result()
        function to read the most recent conversion result. Call stop_adc() to
        stop conversions.
        """
        assert 0 <= channel <= 3, 'Channel must be a value within 0-3!'
        # Start continuous reads and set the mux value to the channel plus
        # the highest bit (bit 3) set.
        return self._read(channel + 0x04, gain, data_rate, ADS1115_CONFIG_MODE_CONTINUOUS)

    def start_adc_difference(self, differential, gain=1, data_rate=None):
        """Start continuous ADC conversions between two ADC channels. Differential
        must be one of:
          - 0 = Channel 0 minus channel 1
          - 1 = Channel 0 minus channel 3
          - 2 = Channel 1 minus channel 3
          - 3 = Channel 2 minus channel 3
        Will return an initial conversion result, then call the get_last_result()
        function continuously to read the most recent conversion result.  Call
        stop_adc() to stop conversions.
        """
        assert 0 <= differential <= 3, 'Differential must be a value within 0-3!'
        # Perform a single shot read using the provided differential value
        # as the mux value (which will enable differential mode).
        return self._read(differential, gain, data_rate, ADS1115_CONFIG_MODE_CONTINUOUS)

    def start_adc_comparator(self, channel, high_threshold, low_threshold,
                             gain=1, data_rate=None, active_low=True,
                             traditional=True, latching=False, num_readings=1):
        """Start continuous ADC conversions on the specified channel (0-3) with
        the comparator enabled.  When enabled the comparator to will check if
        the ADC value is within the high_threshold & low_threshold value (both
        should be signed 16-bit integers) and trigger the ALERT pin.  The
        behavior can be controlled by the following parameters:
          - active_low: Boolean that indicates if ALERT is pulled low or high
                        when active/triggered.  Default is true, active low.
          - traditional: Boolean that indicates if the comparator is in traditional
                         mode where it fires when the value is within the threshold,
                         or in window mode where it fires when the value is _outside_
                         the threshold range.  Default is true, traditional mode.
          - latching: Boolean that indicates if the alert should be held until
                      get_last_result() is called to read the value and clear
                      the alert.  Default is false, non-latching.
          - num_readings: The number of readings that match the comparator before
                          triggering the alert.  Can be 1, 2, or 4.  Default is 1.
        Will return an initial conversion result, then call the get_last_result()
        function continuously to read the most recent conversion result.  Call
        stop_adc() to stop conversions.
        """
        assert 0 <= channel <= 3, 'Channel must be a value within 0-3!'
        # Start continuous reads with comparator and set the mux value to the
        # channel plus the highest bit (bit 3) set.
        return self._read_comparator(channel + 0x04, gain, data_rate,
                                     ADS1115_CONFIG_MODE_CONTINUOUS,
                                     high_threshold, low_threshold, active_low,
                                     traditional, latching, num_readings)

    def start_adc_difference_comparator(self, differential, high_threshold, low_threshold,
                                        gain=1, data_rate=None, active_low=True,
                                        traditional=True, latching=False, num_readings=1):
        """Start continuous ADC conversions between two channels with
        the comparator enabled.  See start_adc_difference for valid differential
        parameter values and their meaning.  When enabled the comparator to will
        check if the ADC value is within the high_threshold & low_threshold value
        (both should be signed 16-bit integers) and trigger the ALERT pin.  The
        behavior can be controlled by the following parameters:
          - active_low: Boolean that indicates if ALERT is pulled low or high
                        when active/triggered.  Default is true, active low.
          - traditional: Boolean that indicates if the comparator is in traditional
                         mode where it fires when the value is within the threshold,
                         or in window mode where it fires when the value is _outside_
                         the threshold range.  Default is true, traditional mode.
          - latching: Boolean that indicates if the alert should be held until
                      get_last_result() is called to read the value and clear
                      the alert.  Default is false, non-latching.
          - num_readings: The number of readings that match the comparator before
                          triggering the alert.  Can be 1, 2, or 4.  Default is 1.
        Will return an initial conversion result, then call the get_last_result()
        function continuously to read the most recent conversion result.  Call
        stop_adc() to stop conversions.
        """
        assert 0 <= differential <= 3, 'Differential must be a value within 0-3!'
        # Start continuous reads with comparator and set the mux value to the
        # channel plus the highest bit (bit 3) set.
        return self._read_comparator(differential, gain, data_rate,
                                     ADS1115_CONFIG_MODE_CONTINUOUS,
                                     high_threshold, low_threshold, active_low,
                                     traditional, latching, num_readings)

    def stop_adc(self):
        """Stop all continuous ADC conversions (either normal or difference mode).
        """
        # Set the config register to its default value of 0x8583 to stop
        # continuous conversions.
        config = 0x8583
        self._device.writeList(ADS1x15_POINTER_CONFIG, [(config >> 8) & 0xFF, config & 0xFF])

    def get_last_result(self):
        """Read the last conversion result when in continuous conversion mode.
        Will return a signed integer value.
        """
        # Retrieve the conversion register value, convert to a signed int, and
        # return it.
        #big endian(Kinree)
        result = self._device.readS16BE(ADS1115_POINTER_CONVERSION)
        return result


