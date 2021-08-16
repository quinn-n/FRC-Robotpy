#!/usr/bin/python
"""robot.py
For FRC team 773's 2019 season.
Written by Quinn Neufeld.
"""
#import socket
import wpilib
import ctre
#from cscore import CameraServer

#Motor Config
LEFT_DRIVE_MOTORS = (1, 2)
RIGHT_DRIVE_MOTORS = (3, 4)
LEFT_DRIVE_INV = False
RIGHT_DRIVE_INV = False
LIFT_MOTOR = [5]
LIFT_INV = False
LIFT_SPD = .5
INTAKE_MOTOR = [6]
INTAKE_INV = False
INTAKE_SPD = .3
#Intake Config
LEFT_INTAKE_PNEUMOTIC = (2, 3)
RIGHT_INTAKE_PNEUMOTIC = (4, 5)
#Pneumotic config
CHARGE_COMPRESSOR_ON_DISABLE = True
BEAM_PNEUMOTIC = (0, 1)
COMPRESSOR_CHANNEL = 0
#Control Settings
STICK = 0
FORWARD_AXIS = 1
ROTATE_AXIS = 2
INV_FOR = False
INV_ROT = False
#Intake controls
INTAKE_RELEASE_BTN = 1
INTAKE_TIGHT_BTN = 2
#Lift controls
LIFT_EXT_BTN = 5
LIFT_RET_BTN = 3
LIFT_MTR_EXT_BTN = 6
LIFT_MTR_RET_BTN = 4
#Camera Settings
CAMERA_NAMES = ("Front Camera")

class MotorControl():
    """A class to manage multiple motors at once. (eg. 2 motor drive)"""
    def __init__(self, motor_ids):
        self.controllers = []
        self.setup_controllers(motor_ids)

    def setup_controllers(self, ids):
        """Adds all motor controllers in array ids to self.controllers."""
        for motor_id in ids:
            self.controllers.append(ctre.WPI_VictorSPX(motor_id))
            self.controllers[-1].id = motor_id

    def set_inverted(self, val):
        """Sets the inverted value for the control group."""
        for controller in self.controllers:
            controller.setInverted(val)

    def set(self, speed):
        """Sets the speed for the control group."""
        for controller in self.controllers:
            controller.set(speed)

    def set_brake(self, val):
        """Sets the brake value for each motor controller.
        0 = EEPROM setting
        1 = Coast
        2 = Brake"""
        for controller in self.controllers:
            controller.NeutralMode = val

    def emg_stop(self):
        """Function for emergency stop.
        Sets the brake value to 2 and sets the motor speed to 0."""
        self.set_brake(2)
        self.set(0)

class SolenoidControl():
    """Class for controlling a solenoid that runs off of 2 channels."""
    def __init__(self, extend_id, retract_id):
        self.extend_solenoid = wpilib.Solenoid(extend_id)
        self.retract_solenoid = wpilib.Solenoid(retract_id)

    def extend(self):
        """Extends the solenoid."""
        self.retract_solenoid.set(False)
        self.extend_solenoid.set(True)

    def retract(self):
        """Retracts the solenoid."""
        self.extend_solenoid.set(False)
        self.retract_solenoid.set(True)

    def stop(self):
        """Stops the solenoid from moving.
        Stops the solenoid by depressurizing both sides."""
        self.extend_solenoid.set(False)
        self.retract_solenoid.set(False)

    def pressure_stop(self):
        """Stops the solenoid from moving.
        Stops the solenoid by pressurizing both sides."""
        self.extend_solenoid.set(True)
        self.retract_solenoid.set(True)

class Robot(wpilib.TimedRobot):
    """The robot class that will control our robot."""
    def robotInit(self):
        """Robot initialization code."""
        #setup motors
        self.left_drive = MotorControl(LEFT_DRIVE_MOTORS)
        self.right_drive = MotorControl(RIGHT_DRIVE_MOTORS)
        self.left_drive.set_inverted(LEFT_DRIVE_INV)
        self.right_drive.set_inverted(RIGHT_DRIVE_INV)
        self.lift_motor = MotorControl(LIFT_MOTOR)
        self.lift_motor.set_inverted(LIFT_INV)
        self.intake = MotorControl((INTAKE_MOTOR))
        self.intake.set_inverted(INTAKE_INV)
        #Setup solenoids
        self.beam_solenoid = SolenoidControl(BEAM_PNEUMOTIC[0], BEAM_PNEUMOTIC[1])
        self.left_lift_solenoid = SolenoidControl(LEFT_INTAKE_PNEUMOTIC[0], LEFT_INTAKE_PNEUMOTIC[1])
        self.right_lift_solenoid = SolenoidControl(RIGHT_INTAKE_PNEUMOTIC[0], RIGHT_INTAKE_PNEUMOTIC[1])
        self.compressor = wpilib.Compressor(COMPRESSOR_CHANNEL)
        self.ds = wpilib.DriverStation.getInstance()
#        self.cs = CameraServer.getInstance()
#        self.start_cameras()

    def disabledPeriodic(self):
        """Keeps things like the compressor running while the robot is disabled."""
        if self.compressor.getPressureSwitchValue() and CHARGE_COMPRESSOR_ON_DISABLE:
            self.compressor.start()
        else:
            self.compressor.stop()

    """
    def start_cameras(self):
        self.cameras = []
        for i in range(len(CAMERA_NAMES)):
            name = CAMERA_NAMES[i]
            self.cameras.append(cs.startAutomaticCapture(dev=i, name=name))
    """

    def teleopPeriodic(self):
        """Code that the robot runs when it's in teleop mode."""
        #Get the joystick axis positions.
        forward_speed = self.ds.getStickAxis(STICK, FORWARD_AXIS)
        rotate_speed = self.ds.getStickAxis(STICK, ROTATE_AXIS)
        #Invert axis if necessary.
        if INV_FOR:
            forward_speed *= -1
        if INV_ROT:
            rotate_speed *= -1

        #set drive motor speeds (turns right when rotate_speed is positive).
        self.left_drive.set(forward_speed + rotate_speed)
        self.right_drive.set(forward_speed - rotate_speed)

        #intake
        if self.ds.getStickButton(STICK, INTAKE_TIGHT_BTN):
            self.intake.set(INTAKE_SPD)
        elif self.ds.getStickButton(STICK, INTAKE_RELEASE_BTN):
            self.intake.set(-INTAKE_SPD)
        else:
            self.intake.set(0)

        #lift motor
        if self.ds.getStickButton(STICK, LIFT_MTR_EXT_BTN):
            self.lift_motor.set(LIFT_SPD)
        elif self.ds.getStickButton(STICK, LIFT_MTR_RET_BTN):
            self.lift_motor.set(-LIFT_SPD)
        else:
            self.lift_motor.set(0)

        #lift pneumotic
        if self.ds.getStickButton(STICK, LIFT_EXT_BTN):
            self.beam_solenoid.extend()
        elif self.ds.getStickButton(STICK, LIFT_RET_BTN):
            self.beam_solenoid.retract()
        else:
            self.beam_solenoid.stop()

if __name__ == "__main__":
    wpilib.run(Robot)
