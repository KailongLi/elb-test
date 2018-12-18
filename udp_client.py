#!/usr/bin/python

import socket
import time
import random
import string
import sys

data_len = 15
port = 8090
ip = "192.168.10.15"

if len(sys.argv) == 1:
    print sys.argv[0], "length ip port"
    sys.exit(-1)
if len(sys.argv) >= 2:
    data_len = int(sys.argv[1])
if len(sys.argv) >= 3:
    ip = sys.argv[2]
if len(sys.argv) >= 4:
    port = int(sys.argv[3])

address = (ip, port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(1)

while True:
    msg = [random.choice(string.digits + string.ascii_letters) for i in range(data_len)]
    data = ''.join(msg)
    if not msg:
        break
    try:
        s.sendto(data, address)
        print "client send: ", data
        rdata, addr = s.recvfrom(2048)
        if not data:
            print "client has exist"
            break
        print "received:", rdata, "from", addr
    except socket.timeout as e:
        print e
    time.sleep(1)

s.close()
