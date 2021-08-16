#!/usr/bin/env python3
import wpilib
import time
import ctre
import os
import cscore

#controls
joystick = 0
joystickXAxis = 0
joystickTurnAxis = 2
joystickYAxis = 1
invertTurn = False
invertY = True
invertX = False
turningSensitivity = 1
forwardSensitivity = 1
sideSensitivity = 1
turnDeadZone = .05
YDeadZone = .05
XDeadZone = .05
#robot config
#offset is for when your robot moves forward/back when you're trying to move sideways, and it will apply forward / backward acceleration based on your horizontal speed.
#a positive offset will cause your robot to apply forward correction.
offset = .1
#channels
frontLeftDriveMotorChannel = 3
rearLeftDriveMotorChannel = 4
frontRightDriveMotorChannel = 2
rearRightDriveMotorChannel = 1
#cameras
cameraNames = []
#cameraNames.append("Front Camera")
#cameraNames.append("Camera 2")
class robot(wpilib.IterativeRobot):
    #these functions are here to make teleop easier.
    def setRightMotorSpeed(self,speed):
        self.frontRightDriveMotor.set(speed)
        self.rearRightDriveMotor.set(speed)
    def setLeftMotorSpeed(self,speed):
        self.frontLeftDriveMotor.set(speed)
        self.rearLeftDriveMotor.set(speed)
    def robotInit(self):
        #motors
        self.frontLeftDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(frontLeftDriveMotorChannel)
        self.frontRightDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(frontRightDriveMotorChannel)
        self.rearLeftDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(rearLeftDriveMotorChannel)
        self.rearRightDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(rearRightDriveMotorChannel)
        self.frontRightDriveMotor.setInverted(False)
        self.rearRightDriveMotor.setInverted(False)
        self.frontLeftDriveMotor.setInverted(True)
        self.rearLeftDriveMotor.setInverted(True)
        #misc
        self.driverStation = wpilib.DriverStation.getInstance()
        wpilib.CameraServer.launch()
        #Cameras
        self.cameraServer = cscore.CameraServer.getInstance()
        #self.cameraServer.enableLogging()
        self.cameras = []
        for i in range(len(cameraNames)):
            self.cameras.append(self.cameraServer.startAutomaticCapture(dev=i,name=cameraNames[i]))
        #self.cameras[1].setResolution(width=160,height=120)
    def autonomousInit(self):
        self.setRightMotorSpeed(.5)
        self.setLeftMotorSpeed(.5)
        time.sleep(3)
        self.setLeftMotorSpeed(0)
        self.setRightMotorSpeed(0)
        time.sleep(1)
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
        turningSpeed = self.driverStation.getStickAxis(joystick,joystickTurnAxis)#get the x axis' position
        if turningSpeed < turnDeadZone/-1 or turningSpeed > turnDeadZone:
            if turningSpeed > turnDeadZone:
                turningSpeed -= turnDeadZone
            elif turningSpeed < turnDeadZone:
                turningSpeed += turnDeadZone
        else:
            turningSpeed = 0
        if invertTurn and turningSpeed != 0:#invert the X axis if we're supposed to
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
        sideSpeed = self.driverStation.getStickAxis(joystick,joystickXAxis)
        if sideSpeed < XDeadZone/-1 or sideSpeed > XDeadZone:
            if sideSpeed > XDeadZone:
                sideSpeed -= XDeadZone
            elif sideSpeed < XDeadZone:
                sideSpeed += XDeadZone
        else:
            sideSpeed = 0
        if invertX:
            sideSpeed /= -1
        #offset for robots that are slightly off weight so they can still drive sideways even if under normal conditions they would end up driving forward and sideways.
        #multpliers for offset
        offsetSpeed = offset * sideSpeed
        forwardSpeed += offsetSpeed
        #multipliers for sensitivity
        turningSpeed*=turningSensitivity
        forwardSpeed*=forwardSensitivity
        sideSpeed*=sideSensitivity
#if turningSpeed is positive, the robot turns right. If turningSpeed is negative, the robot turns left.
        self.frontLeftDriveMotor.set(forwardSpeed+turningSpeed+sideSpeed)
        self.rearLeftDriveMotor.set(forwardSpeed+turningSpeed-sideSpeed)
        self.frontRightDriveMotor.set(forwardSpeed-turningSpeed-sideSpeed)
        self.rearRightDriveMotor.set(forwardSpeed-turningSpeed+sideSpeed)
if __name__ == "__main__":
    wpilib.run(robot)
