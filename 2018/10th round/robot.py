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
quickExtendSolenoid = 5
quickRetractSolenoid = 6
#channels
leftDriveMotorChannel = 4
rightDriveMotorChannel = 1
leftIntakeMotor = 2
rightIntakeMotor = 3
rangeSensorChannel = 1
extendPneumaticSolenoidChannel = 0
retractPneumaticSolenoidChannel = 1
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
        self.rangeSensor = wpilib.DigitalInput(rangeSensorChannel)
        self.extendPneumaticSolenoid = wpilib.Solenoid(extendPneumaticSolenoidChannel)
        self.retractPneumaticSolenoid = wpilib.Solenoid(retractPneumaticSolenoidChannel)
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
    def autonomousInit(self):
        #switch is self.message[0], 'L' or 'R'. scale is self.message[1]
        self.side = self.driverStation.getGameSpecificMessage()
        if self.side != None and self.side != "":
            if self.side[0] == "R":#right switch
                #insert instructions here
                #just test code
                self.setLeftMotorSpeed(.5)
                self.setRightMotorSpeed(.5)
            elif self.side[0] == "L":#left switch
                #insert instructions here
                self.setLeftMotorSpeed(-.5)
                self.setRightMotorSpeed(-.5)
            time.sleep(.75)
            self.setLeftMotorSpeed(0)
            self.setRightMotorSpeed(0)
    def testInit(self):
        self.setLeftMotorSpeed(1)
        self.setRightMotorSpeed(1)
        time.sleep(1)
        self.setLeftMotorSpeed(0)
        self.setRightMotorSpeed(0)
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
            if self.rangeSensor.get():
                self.setIntakeSpeed(.2)
            else:
                self.setIntakeSpeed(0)
        if self.driverStation.getStickButton(joystick,fireButton):#reverse the intake to eject power cube
            self.setIntakeSpeed(-.2)
        if not self.driverStation.getStickButton(joystick,fireButton) and not self.driverStation.getStickButton(joystick,intakeButton):#stop intake
            self.setIntakeSpeed(0)
        if self.driverStation.getStickButton(joystick,extendSolenoid):#extend solenoid
            self.extendPneumaticSolenoid.set(True)
            self.retractPneumaticSolenoid.set(False)
        elif self.driverStation.getStickButton(joystick,retractSolenoid):#retract solenoid
            self.extendPneumaticSolenoid.set(False)
            self.retractPneumaticSolenoid.set(True)
        if self.driverStation.getStickButton(joystick,quickExtendSolenoid) and self.hasRun == False:#extend solenoid a little bit
            self.extendPneumaticSolenoid.set(True)
            time.sleep(.025)
            self.extendPneumaticSolenoid.set(False)
            self.hasRun = True
        elif self.driverStation.getStickButton(joystick,quickRetractSolenoid) and self.hasRun == False:#retract solenoid a little bit
            self.retractPneumaticSolenoid.set(True)
            time.sleep(.025)
            self.retractPneumaticSolenoid.set(False)
            self.hasRun = True
        if not self.driverStation.getStickButton(joystick,quickExtendSolenoid) and not self.driverStation.getStickButton(joystick,quickRetractSolenoid):#reset self.hasRun so it can run again.
            self.hasRun = False
        if not self.compressor.getPressureSwitchValue():#start/stop compressor
            self.compressor.start()
        else:
            self.compressor.stop()
        #time.sleep(.05)
if __name__ == "__main__":
    wpilib.run(robot)
