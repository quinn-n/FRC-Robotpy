#!/usr/bin/env python3.6
import wpilib
import cscore
import ctre
import time

#this robot will need encoders on both sides.
#the motor controllers for the drive motors will need their brake mode set to 'coast'. Well, technically not, but then the entire brake part of this program should be ignored in favour of just changing the accelerator's position.

#controls
steeringAxis = 0
invertSteering = False
centerSteeringAxis = True
steeringDeadZone = 0

accelerationAxis = 1
invertAcceleration = False
centerAccelerationAxis = False
accelerationDeadZone = 0

brakeAxis = 2
invertBrake = False
centerBrakeAxis = False
brakeDeadZone = .05

reverseButton = 0

#config
frontCameraDevID = 0
rearCameraDevID = 1

#self explanitory (hopefully)
frontLeftDriveMotorID = 0
frontRightDriveMotorID = 1
rearLeftDriveMotorID = 2
rearRightDriveMotorID = 3

brakeApplySpeed = 10 #the encoder rate at which the brakes will cut off / turn on (reverse the motors)

class robot(wpilib.IterativeRobot):
    def robotInit(self):
        self.frontLeftDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(frontLeftDriveMotorID)
        self.rearLeftDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(rearLeftDriveMotorID)
        self.frontRightDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(frontRightDriveMotorID)
        self.rearRightDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(rearRightDriveMotorID)

        self.frontLeftDriveMotor.setInverted(False)
        self.rearLeftDriveMotor.setInverted(False)
        self.frontRightDriveMotor.setInverted(False)
        self.rearRightDriveMotor.setInverted(False)

        self.leftDriveEncoder = ctre.sensorcollection.SensorCollection(self.frontLeftDriveMotor)
        self.rightDriveEncoder = ctre.sensorcollection.SensorCollection(self.frontRightDriveMotor)

        self.ds = wpilib.DriverStation.getInstance()

        self.cameraServer = cscore.CameraServer.getInstance()
        self.frontCamera = self.cameraServer.startAutomaticCapture(dev=frontCameraDevID,name="Front Camera")
        self.rearCamera = self.cameraServer.startAutomaticCapture(dev=rearCameraDevID,name="Rear Camera")
        
    def setLeftDriveMotorSpeed(self,speed):
        self.frontLeftDriveMotor.set(speed)
        self.rearLeftDriveMotor.set(speed)

    def setRightDriveMotorSpeed(self,speed):
        self.frontRightDriveMotor.set(speed)
        self.rearRightDriveMotor.set(speed)

    def teleopPeriodic(self):
        forwardSpeed = self.ds.getStickAxis(joystick,accelerationAxis)
        if invertAcceleration:
            forwardSpeed /= -1
        if not centerAccelerationAxis:
            forwardSpeed += 1
            forwardSpeed /= 2
        if self.ds.getStickButton(joystick,reverseButton):
            forwardSpeed /= -1
        if forwardSpeed > accelerationDeadZone or forwardSpeed/-1 > accelerationDeadZone:
            forwardSpeed = 0

        turningSpeed = self.ds.getStickAxis(joystick,steeringAxis)
        if invertSteering:
            turningSpeed /= -1
        if not centerAccelerationAxis:
            turningSpeed += 1
            turningSpeed /= 2
        if turningSpeed > steeringDeadZone or turningSpeed/-1 > steeringDeadZone:
            turningSpeed = 0

        brakeSpeed = self.ds.getStickAxis(joystick,brakeAxis)
        if invertBrake:
            brakeSpeed /= -1
        if not centerBrakeAxis:
            brakeSpeed += 1
            brakeSpeed /= 2

        if brakeSpeed > brakeDeadZone or brakeSpeed/-1 > brakeDeadZone:
            leftDriveSpeed = self.leftDriveEncoder.getPulseWidthVelocity()
            rightDriveSpeed = self.rightDriveEncoder.getPulseWidthVelocity()
            #these if statements control if & in which direction motors should be activated for them to slow down / stop.
            if leftDriveSpeed > brakeApplySpeed:
                self.setLeftDriveMotorSpeed(brakeSpeed)
            elif leftDriveSpeed/-1 > brakeApplySpeed:
                self.setLeftDriveMotorSpeed(brakeSpeed/-1)
            if rightDriveSpeed > brakeApplySpeed:
                self.setRightDriveMotorSpeed(brakeSpeed)
            elif rightDriveSpeed/-1 > brakeApplySpeed:
                self.setRightDriveMotorSpeed(brakeSpeed/-1)

        else:
            #if turningSpeed is positive, the robot turns right.
            self.setLeftDriveMotorSpeed(forwardSpeed+turningSpeed)
            self.setRightDriveMotorSpeed(forwardSpeed-turningSpeed)

    def disabledInit(self):#cuts the drive motors
        self.setLeftDriveMotorSpeed(0)
        self.setRightDriveMotorSpeed(0)

if __name__ == "__main__":
    wpilib.run(robot)
