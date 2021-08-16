#!/usr/bin/env python
#robot-setup.py
#Script to setup roboRIOs with pip and opkg packages.
#Assumes you're already connected to a network with an internet connection.
#Written by Quinn Neufeld, FRC team 773

import os
from time import sleep

#os.system("robotpy-installer download-robotpy")
#os.system("robotpy-installer download-pip wpilib robotpy-navx robotpy-cscore robotpy-rev robotpy-ctre robotpy-wpilib-utilities robotpy-hal-roborio robotpy-hal-base")
#os.system("robotpy-installer download-opkg robotpy-cscore robotpy-ctre robotpy-rev")
#os.system("sudo netctl stop wireless-school && sudo netctl start wireless-773")
#Wait for DNS to figure itself out
sleep(15)
os.system("robotpy-installer install-robotpy")
os.system("robotpy-installer install-opkg robotpy-cscore robotpy-ctre robotpy-rev")
os.system("robotpy-installer install-pip wpilib robotpy-navx robotpy-cscore robotpy-rev robotpy-ctre robotpy-wpilib-utilities robotpy-hal-roborio robotpy-hal-base")
print("Done.")
