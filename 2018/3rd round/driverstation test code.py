#!/usr/bin/env python3.6
import socket
ip = "192.168.1.100"
port = 1337
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((ip,port))
while True:
    msg = s.recv(4096)
    print(msg.decode("utf-8"))
