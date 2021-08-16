#!/usr/bin/env python3
import wpilib
import time
from pyfrc.physics import drivetrains
import pygame
import multiprocessing
import os
import psutil
import socket
pygame.init()
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
errorFile = open("./error.txt","a")

#controls
joystickXAxis = 0
joystickYAxis = 1
intakeButton = 4
fireButton = 5
#channels
leftDriveMotorChannel = 0
rightDriveMotorChannel = 1
leftIntakeMotor = 2
rightIntakeMotor = 3
intakeSensorChannel = 4
#settings
intakeSensorThreshold = 5
driverStationIP = "192.168.1.100"
driverStationPort = 1337

#initalization
team = wpilib.DriverStation.Alliance
#connect to driver station
try:
    s.connect((driverStationIP,driverStationPort))
except:
    errorFile.write("Could not connect to driver station.")
    exit()
#multiprocessing init
multiprocessing.set_start_method("fork")
queue = multiprocessing.Queue()

#get interface objects
rightDriveMotor = wpilib.Talon(rightDriveMotorChannel)
leftDriveMotor = wpilib.Talon(leftDriveMotorChannel)
leftIntake = wpilib.Talon(leftIntakeMotor)
rightIntake = wpilib.Talon(rightIntakeMotor)
intakeSensor = wpilib.AnalogInput(intakeSensorChannel)

#these functions are here because I thought we were going to have 4 drive motors, but I decided to keep them in case we want to add more in the future
def setRightMotorSpeed(speed):
    rightDriveMotor.set(speed)
def setLeftMotorSpeed(speed):
    leftDriveMotor.set(speed)

def checkParent(process,queue):
    while process.Parent() != None:
        sleep(2)
    queue.put("die")
def runIntake(speed,queue):
    ps = psutil.Process(os.getpid())
    killSwitch = multiprocess.Process(target=checkParent,args=(ps,queue))
    killSwitch.start()
    leftIntake.set(speed)
    rightIntake.set(speed)
    while True:
        msg = queue.get_nowait()#use code "die" to end the process, and code "spd" to set a different speed; and use a : in between spd and the number
        if msg[0:3] == "die" or intakeSensor.getVoltage() >= intakeSensorThreshold:
            leftIntake.stopMotor()
            rightIntake.stopMotor()
            exit()
        elif msg[0:3] == "spd":
            speed = msg[msg.locate(":")+1:]#set the new speed to be what comes after the code; ex. spd:4 will set the speed to 4.
            leftIntake.set(int(speed))
            rightIntake.set(int(speed))
        msg = None

class robot(wpilib.IterativeRobot):
    def robotInit(self):
        forwardSpeed = 0
        turningSpeed = 0
        pygame.init()
    def operatorControl(self):
        while True:
            try:
                eventType = s.recv()
            except:
                errorFile.write("could not recieve event type!\n")
            eventType = int(eventType.decode("utf-8"))
            if eventType == pygame.JOYAXISMOTION:
                try:
                    eventAxis = s.recv(4096)
                    eventAxis = int(eventAxis.decode("utf-8"))
                except:
                    errorFile.write("could not recieve event axis!\n")
                if eventAxis == joystickXAxis:#if our axis is the x axis, set the turning speed
                    try:
                        turningSpeed = s.recv(4096)
                    except:
                        errorFile.write("could not recieve turning speed!\n")
                    turningSpeed = float(turningSpeed.decode("utf-8"))
                elif eventAxis == joystickYAxis:#if our axis is the y axis, set the forward speed
                    try:
                        forwardSpeed = s.recv(4096)
                    except:
                        errorFile.write("could not recieve forward speed!\n")
                    forwardSpeed = float(forwardSpeed.decode("utf-8"))
#if turningSpeed is positive, the robot turns right. If turningSpeed is negative, the robot turns left.
                setRightMotorSpeed(forwardSpeed-turningSpeed)
                setLeftMotorSpeed(forwardSpeed+turningSpeed)
            elif eventType == pygame.JOYBUTTONDOWN:#turn on different parts of the robot according to button presses.
                try:
                    eventButton = s.recv(4096)
                except:
                    errorFile.write("Could not recieve button press!")
                eventButton = int(eventButton.decode("utf-8"))
                if eventButton == intakeButton:#run the intake
                    intake = multiprocessing.Process(target=runIntake,args=(.2,queue,))
                    intake.start()
                elif eventBtton == fireButton:#reverse the intake to eject power cube
                    queue.put("spd:-.2")
                elif eventType == pygame.JOYBUTTONUP:#turn off different parts of the robot according to button releases.
                    try:
                        eventButton = s.recv(4096)
                    except:
                        errorFile.write("Could not recieve button press!")
                    eventButton = int(eventButton.decode("utf-8"))
                    if eventButton == intakeButton or eventButton == fireButton:#stop the intake
                        queue.put("die")
if __name__ == "__main__":
    wpilib.run(robot)
