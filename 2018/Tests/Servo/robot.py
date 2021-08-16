#!/usr/bin/env python3.6
import wpilib
servoPWM = 0
joystick = 0
joystickAxis = 1
class robot(wpilib.IterativeRobot):
    def robotInit(self):
        self.servo = wpilib.Servo(servoPWM)
        self.driverStation = wpilib.DriverStation.getInstance()
    def testPeriodic(self):
        self.servoTarget = self.driverStation.getStickAxis(joystick,joystickAxis)
        self.servo.set(self.servoTarget)

if __name__ == "__main__":
    wpilib.run(robot)
