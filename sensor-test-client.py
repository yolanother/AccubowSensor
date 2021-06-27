import socket
import time
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.sendto(bytes("connect", "utf-8"), ("192.168.1.159", 8881))
while True:
    data = s.recv(4)
    if(len(data) > 0):
        print (">>\r Received: %d" % int.from_bytes(data, byteorder='little'), end='')

s.close()
