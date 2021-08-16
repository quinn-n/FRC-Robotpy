#!/usr/bin/env python3.6
import pygame
import wpilib
from pyfrc.physics import drivetrains

#controls
joystickID = 0
xAxis = 0
yAxis = 1
invertX = False
invertY = True

#channel IDs
frontLeftMotorChannel = 0
frontRightMotorChannel = 1
rearLeftMotorChannel = 2
rearRightMotorChannel = 3

class robot(wpilib.IterativeRobot):
    def robotInit(self):
        self.frontLeftMotor = wpilib.Talon(frontLeftMotorChannel)
        self.frontRightMotor = wpilib.Talon(frontRightMotorChannel)
        self.rearLeftMotor = wpilib.Talon(rearLeftMotorChannel)
        self.rearRightMotor = wpilib.Talon(rearRightMotorChannel)
        def left(speed):#group our motor controls into two functions
            self.frontLeftMotor.set(speed)
            self.rearLeftMotor.set(speed)
        def right(speed):
            self.frontRightMotor.set(speed)
            self.rearRightMotor.set(speed)
        pygame.init()#start pygame & get joystick object
        self.controller = pygame.joystick.Joystick(joystickID)
        self.controller.init()
    def operatorControl(self):
        while True:
            for event in self.pygame.event.get():#read a new joystick event
                if event.type == self.pygame.JOYAXISMOTION:#if it's an axis motion, update the motor speed
                    if event.axis == xAxis:
                        xPos = self.controller.get_axis(event.axis)
                        if invertX:
                            xPos = xPos/-1
                    elif event.axis == yAxis:
                        yPos = self.controller.get_axis(event.axis)
                        if invertY:
                            yPos = yPos/-1
                    leftDriveSpeed = yPos+xPos
                    rightDriveSpeed = yPos-xPos
                    wpilib.tankDrive(leftDriveSpeed,rightDriveSpeed)
                elif event.type == self.pygame.JOYBUTTONDOWN:
                    #activate robot functions
                    time.sleep(0)
                elif event.type == self.pygame.JOYBUTTONUP:
                    #deactivate robot functions
                    time.sleep(0) #the compiler isn't happy if there's nothing where there sould be something.
                time.sleep(.05) #don't eat all the cpu cycles pls
    #
class PhysicsEngine(object):
    def __init__(self,physics_controller):
        self.physics_controller = physics_controller
        self.position = 0
        self.frontLeftMotor = wpilib.Talon(frontLeftMotorChannel)
        self.frontRightMotor = wpilib.Talon(frontRightMotorChannel)
        self.rearLeftMotor = wpilib.Talon(rearLeftMotorChannel)
        self.rearRightMotor = wpilib.Talon(rearRightMotorChannel)

    def update_sim(self,hal_data,now,tm_diff):
        fl_motor = hal_data["pwm"][0]["value"]
        fr_motor = hal_data["pwm"][1]["value"]
        rl_motor = hal_data["pwm"][2]["value"]
        rr_motor = hal_data["pwm"][3]["value"]
        speed,rotation = drivetrains.four_motor_drivetrain(self.rearLeftMotor,self.rearRightMotor,self.frontLeftMotor,self.frontRightMotor)
        self.physics_controller.drive(speed,rotation,tm_diff)
        self.position += hal_data["pwm"][4]["value"]*tm_diff*3
if __name__ == "__main__":
    wpilib.run(robot)
