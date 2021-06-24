#!/bin/bash

tar -c . | ssh pi@192.168.1.159 'rm -rf AccubowSensor; mkdir AccubowSensor; tar -kxf - -C AccubowSensor; chmod +x AccubowSensor/sensor-server.sh' 

while [ -n "$1" ]; do
    if [ "$1" == "make-bin" ]; then
        ssh pi@192.168.1.159 'cd AccubowSensor/VL53L0X_rasp_python; make; cp cd AccubowSensor/VL53L0X_rasp_python/bin/* lib/'
    fi

    if [ "$1" == "run" ]; then
        ssh pi@192.168.1.159 'AccubowSensor/sensor-server.sh'
    fi
    shift
done