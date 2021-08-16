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
intakeButton = 1
fireButton = 2
extendSolenoid = 3
retractSolenoid = 4
#channels
leftDriveMotorChannel = 1
rightDriveMotorChannel = 2
#leftIntakeMotor = 3
#rightIntakeMotor = 4
#intakeLimitSwitchChannel = 0
pneumaticSolenoidChannel = 5
compressorChannel = 6
#settings
intakeSensorThreshold = 5
multiprocessing.set_start_method("fork")
class robot(wpilib.IterativeRobot):
    #these functions are here so we can easily add more drive motors.
    def setRightMotorSpeed(self,speed):
        self.rightDriveMotor.set(speed)
    def setLeftMotorSpeed(self,speed):
        self.leftDriveMotor.set(speed)
    def runIntake(self,speed,runIntakeQueue):
        self.leftIntake.set(speed)
        self.rightIntake.set(speed)
        while True:
            msg = self.runIntakeQueue.get_nowait()#use code "die" to end the process, and code "spd" to set a different speed; and use a : in between spd and the number
            if msg[0:3] == "die" or limitSwitch.get():
                self.leftIntake.stopMotor()
                self.rightIntake.stopMotor()
                exit()
            elif msg[0:3] == "spd":
                speed = msg[msg.locate(":")+1:]#set the new speed to be what comes after the code; ex. spd:4 will set the speed to 4.
                self.leftIntake.set(int(speed))
                self.rightIntake.set(int(speed))
            msg = None
    def reverseIntake(self,speed,reverseIntakeQueue):#the same as runIntake, just without the killswitch.
        self.leftIntake.set(speed)
        self.rightIntake.set(speed)
        while True:
            msg = runIntakeQueue.get_nowait()#use code "die" to end the process, and code "spd" to set a different speed; and use a : in between spd and the number
            if msg[0:3] == "die":
                self.leftIntake.stopMotor()
                self.rightIntake.stopMotor()
                exit()
            elif msg[0:3] == "spd":
                speed = msg[msg.locate(":")+1:]#set the new speed to be what comes after the code; ex. spd:.4 will set the speed to .4.
                self.leftIntake.set(int(speed))
                self.rightIntake.set(int(speed))
            msg = None
            time.sleep(.1)
    def robotInit(self):
        #get interface objects
        self.leftDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(leftDriveMotorChannel)
        self.rightDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(rightDriveMotorChannel)
        #self.leftIntake = ctre.wpi_talonsrx.WPI_TalonSRX(leftIntakeMotor)
        #self.rightIntake = ctre.wpi_talonsrx.WPI_TalonSRX(rightIntakeMotor)
        #self.limitSwitch = wpilib.digitalinput.DigitalInput(intakeLimitSwitchChannel)
        self.pneumaticSolenoid = wpilib.Solenoid(pneumaticSolenoidChannel)
        self.compressor = wpilib.Compressor()
        self.driverStation = wpilib.DriverStation.getInstance()
        #extra initalization
        self.leftDriveMotor.setInverted(True)
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
            intake = multiprocessing.Process(target=self.runIntake,args=(.2,self.runIntakeQueue,))
            intake.start()
            self.intakeRunning = True
        elif self.driverStation.getStickButton(joystick,fireButton):#reverse the intake to eject power cube
            self.runIntakeQueue.put("die")
            reverseIntake = multiprocessing.Process(target=self.reverseIntake,args=(-.2,self.runIntakeQueue,))
            reverseIntake.start()
            self.reverseIntakeRunning = True
        if self.driverStation.getStickButton(joystick,extendSolenoid):
            self.pneumaticSolenoid.set(True)
        elif self.driverStation.getStickButton(joystick,retractSolenoid):
            self.pneumaticSolenoid.set(False)
        if self.compressor.getPressureSwitchValue():#start/stop compressor
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
