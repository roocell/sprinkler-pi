#!/usr/bin/python3

import RPi.GPIO as GPIO
import os, time, sys, datetime
import logging

# create logger
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)




# GPIO
valve = 8 # GPIO14

def setupgpio():
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering

    # connection is on the NO (normally open) port
    # on the relay
    # this is so when the pi is powered off, the doors
    # won't move
    GPIO.setup(valve, GPIO.OUT)
    GPIO.output(valve, GPIO.HIGH)  # default LOW (closed)


if __name__ == '__main__':
    setupgpio()
    while True:
        log.debug("water on")
        #GPIO.output(valve, GPIO.LOW)
        time.sleep(10)
        log.debug("water off")
        #GPIO.output(valve, GPIO.HIGH)
        time.sleep(10)
