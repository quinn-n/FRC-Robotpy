#!/usr/bin/env python3
import wpilib
import time
from pyfrc.physics import drivetrains
import pygame
pygame.init()

#controls
joystickChannel = 0
joystickXAxis = 0
joystickYAxis = 1
invertX = False
invertY = True
intakeButton = 4
fireButton = 5
#channels
frontLeftMotorChannel = 0
rearLeftMotorChannel = 1
frontRightMotorChannel = 2
rearRightMotorChannel = 3
leftIntakeMotor = 4
rightIntakeMotor = 5
#this line is for the simulatior. Might have to remove for actual robot.
speed,rotation = drivetrains.four_motor_drivetrain(rearLeftMotorChannel,rearRightMotorChannel,frontLeftMotorChannel,frontRightMotorChannel)
#simulator lines end here

controller = pygame.joystick.Joystick(joystickChannel)
controller.init()

#get motor objects
frontRight = wpilib.Talon(frontRightMotorChannel)
frontLeft = wpilib.Talon(frontLeftMotorChannel)
rearRight = wpilib.Talon(rearRightMotorChannel)
rearLeft = wpilib.Talon(rearLeftMotorChannel)
leftIntake = wpilib.Talon(leftIntakeMotor)
rightIntake = wpilib.Talon(rightIntakeMotor)

def setRightMotorsSpeed(speed):
    frontRight.set(speed)
    rearRight.set(speed)
def setLeftMotorsSpeed(speed):
    frontLeft.set(speed)
    frontRight.set(speed)
def setIntakeSpeed(speed):
    leftIntake.set(speed)
    rightIntake.set(speed)

class robot:
    forwardSpeed = 0
    turningSpeed = 0
    pygame.init()
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
                setRightMotorsSpeed(forwardSpeed-turningSpeed)
                setLeftMotorsSpeed(forwardSpeed+turningSpeed)
            elif event.type == pygame.JOYBUTTONDOWN:#turn on different parts of the robot according to button presses.
                if event.button == intakeButton:#run the intake
                    setIntakeSpeed(1)
                elif event.button == fireButton:#reverse the intake to eject power cube
                    setIntakeSpeed(-1)
            elif event.type == pygame.JOYBUTTONUP:#turn off different parts of the robot according to button releases.
                if event.button == intakeButton or fireButton:#stop the intake
                    setIntakeSpeed(0)
if __name__ == "__main__":
    wpilib.run(robot)
