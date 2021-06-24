import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.sendto(bytes("connect", "utf-8"), ("192.168.1.159", 8881))
while True:
    data = s.recv(32)
    if(len(data) > 0):
        print ("Received: %d" % int(data))

s.close()