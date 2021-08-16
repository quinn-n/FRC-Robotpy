#!/usr/bin/python
"""robot.py
For FRC team 773's 2019 season.
Written by Quinn Neufeld.
"""
import wpilib
import ctre
import rev
from cscore import CameraServer

#Motor Config
LEFT_DRIVE_MOTORS = (1, 2)
RIGHT_DRIVE_MOTORS = (3, 4)
LEFT_DRIVE_INV = False
RIGHT_DRIVE_INV = True
SHUTTLE_MOTOR = 5
BEAM_MOTOR = 6
BEAM_INV = False
BEAM_SPEED = .35
SHUTTLE_INV = False
SHUTTLE_SPD = .35
LEFT_INTAKE_MOTOR = 7
RIGHT_INTAKE_MOTOR = 8
LEFT_INTAKE_INV = False
RIGHT_INTAKE_INV = True
INTAKE_SPD = .5

FOR_PARABOLA = lambda x: x ** 2
ROT_PARABOLA = lambda x: x ** 2

#Intake Lift Config
LIFT_RETRACT_BUTTON = 8
LIFT_EXTEND_BUTTON = 7
LEFT_INTAKE_SOLENOID = (2, 3)
RIGHT_INTAKE_SOLENOID = (4, 5)
#Pneumotic config
CHARGE_COMPRESSOR_ON_DISABLE = True
INTAKE_SOLENOID = (0, 1)
COMPRESSOR_CHANNEL = 0
COMPRESSOR_AMPS_ENTRY = "Compressor Current Draw"
COMPRESSOR_ACTIVE_ENTRY = "Compressor Active"
#Control Settings
STICK = 0
FORWARD_AXIS = 1
ROTATE_AXIS = 0
INV_FOR = True
INV_ROT = False
FOR_SENSITIVITY = .75
ROT_SENSITIVITY = .5
FOR_DEADZONE = .01
ROT_DEADZONE = .01
#Intake controls
INTAKE_RELEASE_BTN = 1
INTAKE_TIGHT_BTN = 2
INTAKE_OPEN_BTN = 11
INTAKE_CLOSE_BTN = 12
#Lift controls
LIFT_EXT_BTN = 9
LIFT_RET_BTN = 10
SHUTTLE_MTR_UP_BTN = 6
SHUTTLE_MTR_DOWN_BTN = 4
BEAM_UP_BTN = 5
BEAM_DOWN_BTN = 3
#Camera Settings
CAMERA_NAMES = ["Front Camera"]

class MotorControl():
    """A class to manage multiple motors at once. (eg. 2 motor drive)"""
    def __init__(self, motor_ids):
        self.controllers = []
        self.setup_controllers(motor_ids)

    def setup_controllers(self, ids):
        """Adds all motor controllers in array ids to self.controllers."""
        for motor_id in ids:
            self.controllers.append(rev.CANSparkMax(motor_id, rev.MotorType.kBrushless))

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
        self.shuttle_motor = ctre.wpi_talonsrx.WPI_TalonSRX(SHUTTLE_MOTOR)
        self.shuttle_motor.setInverted(SHUTTLE_INV)
        self.beam_motor = ctre.wpi_talonsrx.WPI_TalonSRX(BEAM_MOTOR)
        self.beam_motor.setInverted(BEAM_INV)
        self.left_intake = ctre.wpi_talonsrx.WPI_TalonSRX(LEFT_INTAKE_MOTOR)
        self.left_intake.setInverted(LEFT_INTAKE_INV)
        self.right_intake = ctre.wpi_talonsrx.WPI_TalonSRX(RIGHT_INTAKE_MOTOR)
        self.right_intake.setInverted(RIGHT_INTAKE_INV)
        #Setup solenoids
        self.left_lift_solenoid = SolenoidControl(LEFT_INTAKE_SOLENOID[0], LEFT_INTAKE_SOLENOID[1])
        self.right_lift_solenoid = SolenoidControl(RIGHT_INTAKE_SOLENOID[0], RIGHT_INTAKE_SOLENOID[1])
        self.left_intake_solenoid = SolenoidControl(INTAKE_SOLENOID[0], INTAKE_SOLENOID[1])
        self.compressor = wpilib.Compressor(COMPRESSOR_CHANNEL)
        #Extra initialization
        self.ds = wpilib.DriverStation.getInstance()
        self.cs = CameraServer.getInstance()
        self.start_cameras()
        #Setup vars
        self.retracted_lift = False
    
    def autonomousInit(self):
        """Calls self.teleopInit().
        Insurance for sandstorm."""
        print("Ran autonomous init.")
        self.teleopInit()
    
    def autonomousPeriodic(self):
        """Calls self.teleopPeriodic().
        Insurance for sandstorm."""
        self.teleopPeriodic()
    
    def robotPeriodic(self):
        """Always running on the robot.
        Manages the compressor and it's dashboard."""
        pressure_switch = self.compressor.getPressureSwitchValue()
        self.compressor.setClosedLoopControl(pressure_switch)

    def disabledPeriodic(self):
        """Keeps things like the compressor running while the robot is disabled."""
        if self.compressor.getPressureSwitchValue() and CHARGE_COMPRESSOR_ON_DISABLE:
            self.compressor.start()
        else:
            self.compressor.stop()
    
    def start_cameras(self):
        self.cameras = []
        for i in range(len(CAMERA_NAMES)):
            name = CAMERA_NAMES[i]
            self.cameras.append(self.cs.startAutomaticCapture(dev=i, name=name))

    def teleopPeriodic(self):
        """Code that the robot runs when it's in teleop mode."""
        #Get the joystick axis positions.
        forward_speed = self.ds.getStickAxis(STICK, FORWARD_AXIS)
        rotate_speed = self.ds.getStickAxis(STICK, ROTATE_AXIS)
        forward_speed = round(forward_speed, 1)
        rotate_speed = round(rotate_speed, 1)
        #Invert axis if necessary.
        if INV_FOR:
            forward_speed *= -1
        if INV_ROT:
            rotate_speed *= -1
        
        #Apply sensitivity settings
        forward_speed *= FOR_SENSITIVITY
        rotate_speed *= ROT_SENSITIVITY

        #set drive motor speeds (turns right when rotate_speed is positive).
        self.left_drive.set(forward_speed + rotate_speed)
        self.right_drive.set(forward_speed - rotate_speed)

        #Intake motor control
        if self.ds.getStickButton(STICK, INTAKE_TIGHT_BTN):
            self.set_intake(INTAKE_SPD)
        elif self.ds.getStickButton(STICK, INTAKE_RELEASE_BTN):
            self.set_intake(-INTAKE_SPD)
        else:
            self.set_intake(0)
        
        #Intake open/close control
        if self.ds.getStickButton(STICK, INTAKE_OPEN_BTN):
            self.left_intake_solenoid.retract()
        elif self.ds.getStickButton(STICK, INTAKE_CLOSE_BTN):
            self.left_intake_solenoid.extend()

        #Shuttle motor
        if self.ds.getStickButton(STICK, SHUTTLE_MTR_UP_BTN):
            self.shuttle_motor.set(SHUTTLE_SPD)
        elif self.ds.getStickButton(STICK, SHUTTLE_MTR_DOWN_BTN):
            self.shuttle_motor.set(-SHUTTLE_SPD)
        else:
            self.shuttle_motor.set(0)

        #Beam motor
        if self.ds.getStickButton(STICK, BEAM_UP_BTN):
            self.beam_motor.set(BEAM_SPEED)
        elif self.ds.getStickButton(STICK, BEAM_DOWN_BTN):
            self.beam_motor.set(-BEAM_SPEED)
        else:
            self.beam_motor.set(0)

        #Retract and extend the intake 
        if self.ds.getStickButton(STICK, LIFT_RETRACT_BUTTON):
            self.retracted_lift = True
        elif self.ds.getStickButton(STICK, LIFT_EXTEND_BUTTON):
            self.retracted_lift = False
        if self.retracted_lift:
            self.left_lift_solenoid.retract()
            self.right_lift_solenoid.retract()
        else:
            self.left_lift_solenoid.extend()
            self.right_lift_solenoid.extend()
    
    def set_intake(self, spd):
        """Sets the speed of the intakes."""
        self.left_intake.set(spd)
        self.right_intake.set(spd)

if __name__ == "__main__":
    wpilib.run(Robot)
