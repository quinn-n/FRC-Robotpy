#!/usr/bin/env python3.6
import wpilib
import time
import ctre
import pygame
import multiprocessing
import os
import psutil
pygame.init()

#controls
joystickChannel = 0
joystickXAxis = 0
joystickYAxis = 1
invertX = False
invertY = True
intakeButton = 0
fireButton = 1
#channels
leftDriveMotorChannel = 1
rightDriveMotorChannel = 4
leftIntakeMotor = 2
rightIntakeMotor = 3
intakeLimitSwitchChannel = 0
#settings
intakeSensorThreshold = 5
#this line is for the simulatior. Might have to remove for actual robot.
#speed,rotation = drivetrains.two_motor_drivetrain(leftDriveMotor,rightDriveMotor)
#simulator lines end here

controller = pygame.joystick.Joystick(joystickChannel)
controller.init()
multiprocessing.set_start_method("fork")
runIntakeQueue = multiprocessing.Queue()
reverseIntakeQueue = multiprocessing.Queue()

#get interface objects
rightDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(rightDriveMotorChannel)
leftDriveMotor = ctre.wpi_talonsrx.WPI_TalonSRX(leftDriveMotorChannel)
leftIntake = ctre.wpi_talonsrx.WPI_TalonSRX(leftIntakeMotor)
rightIntake = ctre.wpi_talonsrx.WPI_TalonSRX(rightIntakeMotor)
intakeSensor = wpilib.AnalogInput(intakeLimitSwitchChannel)
limitSwitch = wpilib.digitalinput.DigitalInput(intakeLimitSwitchChannel)

#these functions are here because I thought we were going to have 4 drive motors, but I decided to keep them in case we want to add more in the future
def setRightMotorSpeed(speed):
    rightDriveMotor.set(speed)
def setLeftMotorSpeed(speed):
    leftDriveMotor.set(speed)

def checkParent(process,runIntakeQueue):
    while process.Parent() != None:
        sleep(2)
    runIntakeQueue.put("die")

def runIntake(speed,runIntakeQueue):
    ps = psutil.Process(os.getpid())
    killSwitch = multiprocess.Process(target=checkParent,args=(ps,runIntakeQueue,))
    killSwitch.start()
    leftIntake.set(speed)
    rightIntake.set(speed)
    while True:
        msg = runIntakeQueue.get_nowait()#use code "die" to end the process, and code "spd" to set a different speed; and use a : in between spd and the number
        if msg[0:3] == "die" or limitSwitch.get():
            leftIntake.stopMotor()
            rightIntake.stopMotor()
            exit()
        elif msg[0:3] == "spd":
            speed = msg[msg.locate(":")+1:]#set the new speed to be what comes after the code; ex. spd:4 will set the speed to 4.
            leftIntake.set(int(speed))
            rightIntake.set(int(speed))
        msg = None
def reverseIntake(speed,reverseIntakeQueue):#the same as runIntake, just without the killswitch.
    ps = psutil.Process(os.getpid())
    killSwitch = multiprocess.Process(target=checkParent,args=(ps,runIntakeQueue,))
    killSwitch.start()
    leftIntake.set(speed)
    rightIntake.set(speed)
    while True:
        msg = runIntakeQueue.get_nowait()#use code "die" to end the process, and code "spd" to set a different speed; and use a : in between spd and the number
        if msg[0:3] == "die":
            leftIntake.stopMotor()
            rightIntake.stopMotor()
            exit()
        elif msg[0:3] == "spd":
            speed = msg[msg.locate(":")+1:]#set the new speed to be what comes after the code; ex. spd:4 will set the speed to 4.
            leftIntake.set(int(speed))
            rightIntake.set(int(speed))
        msg = None



class robot(wpilib.IterativeRobot):
    def disabledInit(self):
        print("disabled init running.")
    def robotInit(self):
        print("robot init running.")
        forwardSpeed = 0
        turningSpeed = 0
        pygame.init()
    def autonomousInit(self):
        print("autonomous init is running.")
    def teleopInit(self):
        print("teleop init is running.")
    def operatorControl(self):
        while True:
            event = pygame.event.get()
            for event in pygame.event.get():#pygame.event.get() returns an array
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == joystickXAxis:#if our axis is the x axis, set the turning speed
                        turningSpeed = controller.get_axis(event.axis)
                        if invertX:#invert the X axis if we're supposed to
                            turningSpeed = turningSpeed/-1
                    elif event.axis == joystickYAxis:#if our axis is the y axis, set the forward speed
                        forwardSpeed = controller.get_axis(event.axis)
                        if invertY:#invert the Y axis if we're supposed to
                            forwardSpeed = forwardSpeed/-1
#if turningSpeed is positive, the robot turns right. If turningSpeed is negative, the robot turns left.
                    setRightMotorSpeed(forwardSpeed-turningSpeed)
                    setLeftMotorSpeed(forwardSpeed+turningSpeed)
                elif event.type == pygame.JOYBUTTONDOWN:#turn on different parts of the robot according to button presses.
                    if event.button == intakeButton:#run the intake
                        intake = multiprocessing.Process(target=runIntake,args=(.2,runIntakeQueue,))
                        intake.start()
                    elif event.button == fireButton:#reverse the intake to eject power cube
                        runIntakeQueue.put("die")
                        reverseIntake = multiprocessing.Process(target=reverseIntake,args=(-.2,runIntakeQueue,))
                        reverseIntake.start()
                elif event.type == pygame.JOYBUTTONUP:#turn off different parts of the robot according to button releases.
                    if event.button == intakeButton:#stop the intake
                        runIntakeQueue.put("die")
                    elif event.button == fireButton:
                        reverseIntakeQueue.put("die")
        time.sleep(.005)
if __name__ == "__main__":
    wpilib.run(robot)
