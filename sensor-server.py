#!/usr/bin/python

import socketserver
from socket import *
import time
import threading
from lib import VL53L0X


class Data():
    distance = -1
    client = None
    socket = None

data = Data()

# Create a VL53L0X object
tof = VL53L0X.VL53L0X()

# Start ranging
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

timing = tof.get_timing()
if (timing < 20000):
    timing = 20000

def trackRange(data):
    while True:
        lastDistance = data.distance
        data.distance = tof.get_distance()
        print("\r>> %d mm, %d cm" % (data.distance, (data.distance/10)), end="")

        if(lastDistance != data.distance and data.client != None):
            print("\r>> %d mm, %d cm: Sending to %s" % (data.distance, (data.distance/10), data.client[0]), end="")
            data.socket.sendto(data.distance.to_bytes(4, 'little'), data.client)
        
        time.sleep(timing/1000000.00)

thread = threading.Thread(target=trackRange, args=(data,))
thread.daemon = True                            # Daemonize thread
thread.start()

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("Client {} connected. Sending sensor data".format(self.client_address[0]))
        socket = self.request[1]

        data.socket = socket
        data.client = self.client_address

        #lastDistance = -1
        #while(True):
        #    if (data.distance > 0 and data.distance != lastDistance):
        #        
        #    lastDistance = data.distance
        #    time.sleep(timing/1000000.00)

print("Server started on port 8881")
server = socketserver.UDPServer(('',8881), MyHandler)
server.max_packet_size = 4
server.serve_forever()

