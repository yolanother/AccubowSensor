#!/usr/bin/python

import socketserver
from socket import *
import time
from lib import VL53L0X

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("Client {} connected. Sending sensor data".format(self.client_address[0]))
        socket = self.request[1]

        # Create a VL53L0X object
        tof = VL53L0X.VL53L0X()

        # Start ranging
        tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        timing = tof.get_timing()
        if (timing < 20000):
            timing = 20000
        
        while True:
            distance = tof.get_distance()
            if (distance > 0 and distance < 8190):
                print ("%d mm, %d cm" % (distance, (distance/10)))
                socket.sendto(distance.to_bytes(4, 'little'), self.client_address)
            time.sleep(timing/1000000.00)

print("Server started on port 8881")
server = socketserver.UDPServer(('',8881), MyHandler)
server.max_packet_size = 4
server.serve_forever(  )

