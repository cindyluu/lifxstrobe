#!/usr/bin/env python

import socket
from config import UDP_IP, UDP_PORT

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind(("<broadcast>", UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    print "received message:", data
