#!/usr/bin/env python

import socket
from time import sleep
from config import UDP_IP, UDP_PORT

MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

while (1):
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sleep(5)
