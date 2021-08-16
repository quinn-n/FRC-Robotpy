#!/usr/bin/env python3.6
import wpilib
#import ctre
analogChannel = 0
class robot(wpilib.IterativeRobot):
    def robotInit(self):
        self.analogInput = wpilib.AnalogInput(analogChannel)
    def testInit(self):
        print("Starting test...")
        self.currentValue = self.analogInput.getValue()
        self.currentVoltage = self.analogInput.getVoltage()
        print("Value: "+str(self.currentValue)+" Voltage: "+str(self.currentVoltage))
    def testPeriodic(self):
        self.newValue = self.analogInput.getValue()
        self.newVoltage = self.analogInput.getVoltage()
        if self.newValue != self.currentValue or self.newVoltage != self.currentVoltage:
            self.currentValue = self.newValue
            self.currentVoltage = self.newVoltage
            print("Value: "+str(self.currentValue)+" Voltage: "+str(self.currentVoltage))
if __name__ == "__main__":
    wpilib.run(robot)
