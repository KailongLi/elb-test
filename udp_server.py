from socket import socket, AF_INET, SOCK_DGRAM
import sys
import time
import random
import string

def time_server(address, dlen):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(address)
    while True:
        msg, addr = sock.recvfrom(8192)
        print('Got message from', addr, 'len', len(msg), msg)
        msg = [random.choice(string.digits + string.ascii_letters) for i in range(dlen)]
        data = ''.join(msg)
        resp = time.ctime()
        sock.sendto(data.encode('ascii'), addr)

if __name__ == '__main__':
    data_len = 10
    port = 8888
    if len(sys.argv) == 1:
        print sys.argv[0], "length port"
        sys.exit(-1)
    if len(sys.argv) >= 2:
        data_len = int(sys.argv[1])
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    time_server(('', port), data_len)
