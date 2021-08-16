#!/usr/bin/env python3.6
import wpilib
import time
import ctre
import multiprocessing
import os

#controls
joystick = 0
joystickXAxis = 0
joystickYAxis = 1
invertX = False
invertY = True
intakeButton = 2
fireButton = 1
extendSolenoid = 3
retractSolenoid = 4
#channels
leftDriveMotorChannel = 1
rightDriveMotorChannel = 2
leftIntakeMotor = 3
rightIntakeMotor = 4
intakeLimitSwitchChannel = 0
pneumaticSolenoidChannel = 0
#settings
intakeSensorThreshold = 5
multiprocessing.set_start_method("fork")
class robot(wpilib.IterativeRobot):
    #these functions are here so we can easily add more drive motors.
    def setRightMotorSpeed(self,speed):
        self.rightDriveMotor.set(speed)
    def setLeftMotorSpeed(self,speed):
        self.leftDriveMotor.set(speed)
    def setIntakeSpeed(self,speed):
        self.leftIntake.set(speed)
        self.rightIntake.set(speed)
    def robotInit(self):
        #get interface objects
        self.leftDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(leftDriveMotorChannel)
        self.rightDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(rightDriveMotorChannel)
        self.leftIntake = ctre.wpi_talonsrx.WPI_TalonSRX(leftIntakeMotor)
        self.rightIntake = ctre.wpi_talonsrx.WPI_TalonSRX(rightIntakeMotor)
        self.rightDriveMotor.setInverted(True)
        self.rightIntake.setInverted(True)
        self.limitSwitch = wpilib.digitalinput.DigitalInput(intakeLimitSwitchChannel)
        self.pneumaticSolenoid = wpilib.Solenoid(pneumaticSolenoidChannel)
        self.compressor = wpilib.Compressor()
        self.driverStation = wpilib.DriverStation.getInstance()
        #extra initalization
        wpilib.CameraServer.launch()
        self.runIntakeQueue = multiprocessing.Queue()
        self.reverseIntakeQueue = multiprocessing.Queue()
        self.runIntakeQueue = multiprocessing.Queue()
        self.reverseIntakeQueue = multiprocessing.Queue()
        self.intakeRunning = False
        self.reverseIntakeRunning = False
    def autonomousInit(self):#literally just drives the robot forward a bit so we get the bonus points
        self.setLeftMotorSpeed(1)
        self.setRightMotorSpeed(1)
        time.sleep(1)
        self.setLeftMotorSpeed(0)
        self.setRightMotorSpeed(0)
    def testInit(self):
        self.compressor.start()
        time.sleep(1)
        self.compressor.stop()
    def teleopPeriodic(self):
        turningSpeed = self.driverStation.getStickAxis(joystick,joystickXAxis)#get the x axis' position
        if invertX:#invert the X axis if we're supposed to
            turningSpeed = turningSpeed/-1
        forwardSpeed = self.driverStation.getStickAxis(joystick,joystickYAxis)#get the y axis' position
        if invertY:#invert the Y axis if we're supposed to
            forwardSpeed = forwardSpeed/-1
#if turningSpeed is positive, the robot turns right. If turningSpeed is negative, the robot turns left.
        self.setRightMotorSpeed(forwardSpeed-turningSpeed)
        self.setLeftMotorSpeed(forwardSpeed+turningSpeed)
        if self.driverStation.getStickButton(joystick,intakeButton):#run the intake
            if not self.limitSwitch:
                self.setIntakeSpeed(.2)
            else:
                self.setIntakeSpeed(0)
        if self.driverStation.getStickButton(joystick,fireButton):#reverse the intake to eject power cube
            self.setIntakeSpeed(-.2)
        if not self.driverStation.getStickButton(joystick,fireButton) and not self.driverStation.getStickButton(joystick,intakeButton):
            self.setIntakeSpeed(0)
        if self.driverStation.getStickButton(joystick,extendSolenoid):
            self.pneumaticSolenoid.set(True)
        elif self.driverStation.getStickButton(joystick,retractSolenoid):
            self.pneumaticSolenoid.set(False)
        if not self.compressor.getPressureSwitchValue():#start/stop compressor
            self.compressor.start()
        else:
            self.compressor.stop()
        if not self.driverStation.getStickButton(joystick,fireButton) and self.intakeRunning:#stop the intake
            self.runIntakeQueue.put("die")
            self.intakeRunning = False
        elif not self.driverStation.getStickButton(joystick,fireButton) and self.reverseIntakeRunning:#reverse the intake
            self.reverseIntakeQueue.put("die")
            self.reverseIntakeRunning = False
        time.sleep(.05)
if __name__ == "__main__":
    wpilib.run(robot)
