#!/usr/bin/env python3.6
import pygame
import socket
import time
pygame.init()

#controls
joystickChannel = 0
joystickXAxis = 0
joystickYAxis = 1
invertX = False
invertY = True
intakeButton = 4
fireButton = 5
#config
ip = "0.0.0.0"
port = 1337
timeBetweenCommands = .005

#get connection from roboRIO
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((ip,port))
s.listen(1)
conn,addr = s.accept()
print("Got connection from "+addr[0])
controller = pygame.joystick.Joystick(joystickChannel)
controller.init()

while True:
    for event in pygame.event.get():
        eventType = str(event.type)
        eventType = eventType.encode("utf-8")
        try:#send event type
            conn.send(eventType)
        except:
            print("Could not send event type!")
        if event.type == pygame.JOYAXISMOTION:
            eventAxis = str(event.axis)
            time.sleep(timeBetweenCommands)
            try:#send event axis
                conn.send(eventAxis.encode("utf-8"))
            except:
                print("Could not send event axis!")
            if event.axis == joystickXAxis:
                turningSpeed = controller.get_axis(event.axis)
                if invertX:
                    turningSpeed = turningSpeed/-1
                turningSpeed = str(turningSpeed)
                time.sleep(timeBetweenCommands)
                try:#send turning speed
                    conn.send(turningSpeed.encode("utf-8"))
                except:
                    print("Could not send turning speed!")
            elif event.axis == joystickYAxis:
                forwardSpeed = controller.get_axis(event.axis)
                if invertY:
                    forwardSpeed = forwardSpeed/-1
                forwardSpeed = str(forwardSpeed)
                time.sleep(timeBetweenCommands)#allow time for the test to keep up
                try:#send forward speed
                    conn.send(forwardSpeed.encode("utf-8"))
                except:
                    print("Could not send forward speed!")
        elif event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
            eventButton = str(event.button)
            try:#send button
                conn.send(eventButton.encode("utf-8"))
            except:
                print("Could not send button press!")
