"""
accel.py
Gets input over spi from an accelerometer
written by Quinn Neufeld
"""

import wpilib

class Accelerometer:
    """A class written to get input from an accelerometer"""
    def __init__(self, port):
        #kOnboard https://robotpy.readthedocs.io/projects/wpilib/en/stable/wpilib/SerialPort.html
        self.ard = wpilib.SerialPort(9600, )
    
    def get(self):
        """Returns the accelerometer's x, y and z acceleration"""
