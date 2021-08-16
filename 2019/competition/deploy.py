#!/usr/bin/env python
import sys
import os
if len(sys.argv) < 2:
    print("Usage: "+sys.argv[0]+" <directory>")
    sys.exit()

ipFileEmpty = False
#read roborio's ip if it's saved
filepath = sys.argv[1]
if os.path.exists(".roborioip"):
    ipFile = open(".roborioip","r")
    ip = ipFile.read()
    ipFile.close()
else:
    ipFileEmpty = True

#if we couldn't read the roborio's ip from .roborioip, query the user for it
if ipFileEmpty:
    ipFileEmpty = True
    ip = input("Please enter the roboRIO's IP: ")
if ipFileEmpty:
    ipFile = open(".roborioip","w")
    ipFile.write(ip)
    ipFile.close()

#upload the directory to the roborio
os.system("scp -r "+filepath+"/* lvuser@"+ip+":~/py/")
