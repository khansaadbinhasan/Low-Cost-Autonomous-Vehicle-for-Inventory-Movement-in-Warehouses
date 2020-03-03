'''
    --> Sets up I2C connection with Pi as master and arduino as slave
    --> This was taken from https://dzone.com/articles/arduino-and-raspberry-pi-working-together-part-2-now-with-i2
'''

import RPi.GPIO as gpio
import smbus
import time
import sys

bus = smbus.SMBus(1)

address = 0x04

def main():

    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)

    status = False

    while 1:

        gpio.output(17, status)
        status = not status
        bus.write_byte(address, 1 )
        print "Arduino answer to RPI:", bus.read_byte(address)
        time.sleep(1)

if __name__ == '__main__':

    try:
        main()

    except KeyboardInterrupt:
        print 'Interrupted'
        gpio.cleanup()
        sys.exit(0)
