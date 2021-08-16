#!/usr/bin/env python3.6
import wpilib
import time
import ctre
import os
import cscore

#controls
joystick = 0
joystickXAxis = 2
joystickYAxis = 1
invertX = False
invertY = True
joystickPOV = 0
intakePOV = 0
firePOV = 180
extendScissorLift = 3
retractScissorLift = 5
turningSensitivity = 1.01
forwardSensitivity = 1
XDeadZone = .02
YDeadZone = 0
#channels
frontLeftDriveMotorChannel = 3
rearLeftDriveMotorChannel = 4
frontRightDriveMotorChannel = 2
rearRightDriveMotorChannel = 1
leftIntakeMotor = 5
rightIntakeMotor = 6
#rangeSensorChannel = 1
extendScissorLiftChannel = 3
retractScissorLiftChannel = 2
#settings
intakeSpeed = .4
cameraNames = []
#cameraNames.append("Right Camera")
class robot(wpilib.IterativeRobot):
    #these functions are here so we can easily add more drive motors.
    def setRightMotorSpeed(self,speed):
        self.frontRightDriveMotor.set(speed)
        self.rearRightDriveMotor.set(speed)
    def setLeftMotorSpeed(self,speed):
        self.frontLeftDriveMotor.set(speed)
        self.rearLeftDriveMotor.set(speed)
    def setIntakeSpeed(self,speed):
        self.leftIntake.set(speed)
        self.rightIntake.set(speed)
    def extendLift(self,delay=0):
        self.extendScissorLift.set(True)
        self.retractScissorLift.set(False)
        if delay != 0:
            time.sleep(delay)
            self.extendScissorLift.set(False)
    def retractLift(self,delay=0):
        self.extendScissorLift.set(False)
        self.retractScissorLift.set(True)
        if delay != 0:
            time.sleep(delay)
            self.retractScissorLift.set(False)
    def stopLift(self):
        self.extendScissorLift.set(False)
        self.retractScissorLift.set(False)
    def robotInit(self):
        #motors
        self.frontLeftDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(frontLeftDriveMotorChannel)
        self.frontRightDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(frontRightDriveMotorChannel)
        self.rearLeftDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(rearLeftDriveMotorChannel)
        self.rearRightDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(rearRightDriveMotorChannel)
        self.leftIntake = ctre.wpi_talonsrx.WPI_TalonSRX(leftIntakeMotor)
        self.rightIntake = ctre.wpi_talonsrx.WPI_TalonSRX(rightIntakeMotor)
        self.frontRightDriveMotor.setInverted(True)
        self.rearRightDriveMotor.setInverted(True)
        self.frontLeftDriveMotor.setInverted(False)
        self.rearLeftDriveMotor.setInverted(False)
#        self.rightIntake.setInverted(True)
        #solenoids
        self.extendScissorLift = wpilib.Solenoid(extendScissorLiftChannel)
        self.retractScissorLift = wpilib.Solenoid(retractScissorLiftChannel)
        self.compressor = wpilib.Compressor()
        #cameras
        self.cameraServer = cscore.CameraServer.getInstance()
        self.cameraServer.enableLogging()
        self.cameras = []
        for i in range(len(cameraNames)):
            self.cameras.append(self.cameraServer.startAutomaticCapture(dev=i,name=cameraNames[i]))
        #misc
        self.driverStation = wpilib.DriverStation.getInstance()
#        self.rangeSensor = wpilib.DigitalInput(rangeSensorChannel)
        print("Ititialized")
    def autonomousInit(self):
        #get game data
        self.message = ""
        while(len(self.message) < 3):
            self.message = self.driverStation.getGameSpecificMessage()
        self.setRightMotorSpeed(.5)
        self.setLeftMotorSpeed(.5)
        time.sleep(3)
        self.setLeftMotorSpeed(0)
        self.setRightMotorSpeed(0)
        #switch is self.message[0], 'L' or 'R'. scale is self.message[1]
#        self.alliance = self.driverStation.getAlliance()
        #if we start on the left, we can put the cube in the switch
#        if self.alliance.numerator == 1:
#            self.side = self.driverStation.getGameSpecificMessage()
#            if self.side != None and self.side != "":
#                if self.side[0] == "R":#right switch
#                    #go forwards slightly
#                    self.setLeftMotorSpeed(.5)
#                    self.setRightMotorSpeed(.5)
#                    time.sleep(.3)
#                    #go to other side of switch
#                    self.setRightMotorSpeed(0)
#                    time.sleep(.9)
#                    self.setRightMotorSpeed(.5)
#                    time.sleep(3.4)
#                    self.setRightMotorSpeed(.45)
#                    self.setLeftMotorSpeed(0)
#                    time.sleep(.9)
#                    self.setLeftMotorSpeed(.5)
#                    time.sleep(1.75)
#                    #face the intake
#                    self.setLeftMotorSpeed(0)
#                    time.sleep(.75)
#                    self.setRightMotorSpeed(0)
#                    #reverse the intake
#                    self.setIntakeSpeed(intakeSpeed/-1)
#                    time.sleep(2)
#                    self.setIntakeSpeed(0)
#                elif self.side[0] == "L":#left switch
#                    #drive to switch
#                    self.setLeftMotorSpeed(.5)
#                    self.setRightMotorSpeed(.5)
#                    time.sleep(2)
#                    self.setRightMotorSpeed(0)
#                    time.sleep(.9)
#                    self.setLeftMotorSpeed(0)
#                    #eject cube
#                    self.setIntakeSpeed(intakeSpeed/-1)
#                    time.sleep(2)
#                    self.setIntakeSpeed(0)
#            else:
#                #if something is wrong with the FMS, we can just cross the line.
#                self.setLeftMotorSpeed(.5)
#                self.setRightMotorSpeed(.5)
#                time.sleep(2)
#                self.setLeftMotorSpeed(0)
#                self.setRightMotorSpeed(0)
        #if we start on the right side, just cross the line
#        elif self.alliance.numerator == 3:
#            self.setLeftMotorSpeed(.5)
#            self.setRightMotorSpeed(.5)
#            time.sleep(2)
#            self.setLeftMotorSpeed(0)
#            self.setRightMotorSpeed(0)
        #set the motor speeds to 0, just in case it doesn't happen.
        self.setLeftMotorSpeed(0)
        self.setRightMotorSpeed(0)
    def testInit(self):
        self.setLeftMotorSpeed(.5)
        self.setRightMotorSpeed(.5)
        time.sleep(.25)
    def testPeriodic(self):
        self.setLeftMotorSpeed(1)
        self.setRightMotorSpeed(1)
    def teleopPeriodic(self):
        print("Entering teleop...")
        turningSpeed = self.driverStation.getStickAxis(joystick,joystickXAxis)#get the x axis' position
        if turningSpeed < XDeadZone/-1 or turningSpeed > XDeadZone:
            if turningSpeed > XDeadZone:
                turningSpeed -= XDeadZone
            elif turningSpeed < XDeadZone:
                turningSpeed += XDeadZone
        else:
            turningSpeed = 0
        if invertX and turningSpeed != 0:#invert the X axis if we're supposed to
            turningSpeed = turningSpeed/-1
        forwardSpeed = self.driverStation.getStickAxis(joystick,joystickYAxis)#get the y axis' position
        if forwardSpeed < YDeadZone/-1 or forwardSpeed > YDeadZone:
            if forwardSpeed > YDeadZone:
                forwardSpeed -= YDeadZone
            elif forwardSpeed < YDeadZone:
                forwardSpeed += YDeadZone
        else:
            forwardSpeed = 0
        if invertY and forwardSpeed != 0:#invert the Y axis if we're supposed to
            forwardSpeed = forwardSpeed/-1
        #multipliers for sensitivity
        turningSpeed*=turningSensitivity
        forwardSpeed*=forwardSensitivity
#if turningSpeed is positive, the robot turns right. If turningSpeed is negative, the robot turns left.
        self.setRightMotorSpeed(forwardSpeed-turningSpeed)
        self.setLeftMotorSpeed(forwardSpeed+turningSpeed)
        if self.driverStation.getStickPOV(joystick,joystickPOV) == intakePOV:#run the intake
            self.setIntakeSpeed(intakeSpeed)
        if self.driverStation.getStickPOV(joystick,joystickPOV) == firePOV:#reverse the intake to eject power cube
            self.setIntakeSpeed(intakeSpeed/-1)
        if not self.driverStation.getStickPOV(joystick,joystickPOV) == firePOV and not self.driverStation.getStickPOV(joystick,joystickPOV) == intakePOV:#stop intake
            self.setIntakeSpeed(0)
        if self.driverStation.getStickButton(joystick,extendScissorLift):#hold to extend
            self.extendLift()
        elif self.driverStation.getStickButton(joystick,retractScissorLift):#hold to retract
            self.retractLift()
        if not self.driverStation.getStickButton(joystick,extendScissorLift) and not self.driverStation.getStickButton(joystick,retractScissorLift):
            self.stopLift()
        if not self.compressor.getPressureSwitchValue():#start/stop compressor
            self.compressor.start()
        else:
            self.compressor.stop()
if __name__ == "__main__":
    wpilib.run(robot)
