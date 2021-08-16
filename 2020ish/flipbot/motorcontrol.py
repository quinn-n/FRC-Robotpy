"""
motorcontrol.py - Provides a class to manage multiple motors with one object
written by Quinn Neufeld
"""

import ctre


class MotorControl:
    """A class to manage multiple motors at once. (eg. 2 motor drive)"""
    def __init__(self, *motor_ids):
        self.controllers = []
        self.setup_controllers(motor_ids)

    def setup_controllers(self, ids):
        """Adds all motor controllers in array ids to self.controllers."""
        for motor_id in ids:
            self.controllers.append(ctre.WPI_TalonSRX(motor_id))
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