#!/usr/bin/env python
"""
robot.py
Written for a flip bot that uses an arduino connected accelerometer to get the orientation of the robot
Written by Quinn Neufeld
"""

import wpilib
from motorcontrol import MotorControl

#Drive motor config
LEFT_DRIVE_MOTORS = [0, 1]
RIGHT_DRIVE_MOTORS = [2, 3]
LEFT_DRIVE_INVERTED = False
RIGHT_DRIVE_INVERTED = False

#Control config
JOY = 0

FOR_AXIS = 0
ROT_AXIS = 1

INV_FOR = False
INV_ROT = False

class Robot(wpilib.IterativeRobot):
    def robotInit(self):
        """Initializes the robot"""
        #Initialize drive motors
        self.left_drive = MotorControl(LEFT_DRIVE_MOTORS)
        self.right_drive = MotorControl(RIGHT_DRIVE_MOTORS)

        self.left_drive.set_inverted(LEFT_DRIVE_INVERTED)
        self.right_drive.set_inverted(RIGHT_DRIVE_INVERTED)
    
    def teleopPeriodic(self):
        """Drive code for the robot.
        Currently uses tank drive."""
        #Get stick axis
        for_spd = self.ds.getStickAxis(JOY, FOR_AXIS)
        rot_spd = self.ds.getStickAxis(JOY, ROT_AXIS)

        #Set inverted axis
        if INV_FOR:
            for_spd *= -1
        if INV_ROT:
            rot_spd *= -1

        #Set motor speeds
        self.left_drive.set(for_spd + rot_spd)
        self.right_drive.set(for_spd - rot_spd)