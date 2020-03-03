'''
	-->Takes command from Workstation via TCP and sends command to arduino via I2C
'''

import RPi.GPIO as gpio
import smbus
import time
import sys
import socket

bus = smbus.SMBus(1)
address = 0x04


TCP_IP = '0.0.0.0'
TCP_PORT = 5005 # Port number on which to send data
BUFFER_SIZE = 20 # Normally 1024, but I want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print ('Connection address:', addr)


# STOP = 0
# UP = 1
# DOWN = 2
# RIGHT = 3
# LEFT = 4

cmd = 0


def main():

    gpio.setmode(gpio.BCM)
    status = False

    while True:
        cmd = int(str(conn.recv(BUFFER_SIZE).decode("UTF-8")))
    
#        if not cmd: 
 #           break

        bus.write_byte(address, cmd)
        print("Arduino answer to RPI:", bus.read_byte(address))
        time.sleep(0.1)

    conn.close()

if __name__ == '__main__':

    try:
        main()

    except KeyboardInterrupt:
        print('Interrupted')
        gpio.cleanup()

        sys.exit(0)