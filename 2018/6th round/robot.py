#!/usr/bin/env python3.6
import wpilib
import time
import ctre
import multiprocessing
import os
import psutil

#controls
joystick = 0
joystickXAxis = 0
joystickYAxis = 1
invertX = False
invertY = True
intakeButton = 0
fireButton = 1
#channels
leftDriveMotorChannel = 1
rightDriveMotorChannel = 2
#leftIntakeMotor = 3
#rightIntakeMotor = 4
#intakeLimitSwitchChannel = 0
#settings
intakeSensorThreshold = 5

multiprocessing.set_start_method("fork")
runIntakeQueue = multiprocessing.Queue()
reverseIntakeQueue = multiprocessing.Queue()


class robot(wpilib.IterativeRobot):
    #these functions are here so we can easily add more drive motors.
    def setRightMotorSpeed(self,speed):
         self.rightDriveMotor.set(speed)
    def setLeftMotorSpeed(self,speed):
        self.leftDriveMotor.set(speed)
    
    def checkParent(process,runIntakeQueue):
        while process.Parent() != None:
            sleep(2)
        runIntakeQueue.put("die")
    
    def runIntake(self,speed,runIntakeQueue):
        ps = psutil.Process(os.getpid())
        killSwitch = multiprocess.Process(target=checkParent,args=(ps,runIntakeQueue,))
        killSwitch.start()
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
    def reverseIntake(speed,reverseIntakeQueue):#the same as runIntake, just without the killswitch.
        ps = psutil.Process(os.getpid())
        killSwitch = multiprocess.Process(target=checkParent,args=(ps,reverseIntakeQueue,))
        killSwitch.start()
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
        self.driverStation = wpilib.DriverStation.getInstance()
        #extra initalization
        self.runIntakeQueue = multiprocessing.Queue()
        self.reverseIntakeQueue = multiprocessing.Queue()
    def autonomousInit(self):#literally just drives the robot forward a bit so we get the bonus points
        self.setLeftMotorSpeed(1)
        self.setRightMotorSpeed(1)
        time.sleep(1)
        self.setLeftMotorSpeed(0)
        self.setRightMotorSpeed(0)
    def operatorControl(self):
        while True:
            turningSpeed = self.driverStation.getStickAxis(joystick,joystickXAxis)#get the x axis' position
            if invertX:#invert the X axis if we're supposed to
                turningSpeed = turningSpeed/-1
            forwardSpeed = self.driverStation.getStickAxis(joystick,joystickYAxis)#get the y axis' position
            if invertY:#invert the Y axis if we're supposed to
                forwardSpeed = forwardSpeed/-1
#if turningSpeed is positive, the robot turns right. If turningSpeed is negative, the robot turns left.
            setRightMotorSpeed(forwardSpeed-turningSpeed)
            setLeftMotorSpeed(forwardSpeed+turningSpeed)
            if self.driverStation.getStickButton(joystick,intakeButton):#run the intake
                intake = multiprocessing.Process(target=runIntake,args=(.2,runIntakeQueue,))
                intake.start()
            elif self.driverStation.getStickButton(joystick,fireButton):#reverse the intake to eject power cube
                runIntakeQueue.put("die")
                reverseIntake = multiprocessing.Process(target=reverseIntake,args=(-.2,runIntakeQueue,))
                reverseIntake.start()
            if not self.driverStation.getStickButton(joystick,fireButton):#stop the intake
                runIntakeQueue.put("die")
            elif not self.driverStation.getStickButton(joystick,fireButton):
                reverseIntakeQueue.put("die")
        time.sleep(.005)
if __name__ == "__main__":
    wpilib.run(robot)
