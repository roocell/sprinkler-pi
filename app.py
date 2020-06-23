#!/usr/bin/python3

import RPi.GPIO as GPIO
import os, time, sys, datetime
import logging
import atexit

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask import Response, redirect, url_for
from flask_socketio import SocketIO, emit
from threading import Thread


# create logger
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

# create flask and socket
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# GPIO
valve = 8 # GPIO14

def setupgpio():
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering

    # connection is on the NO (normally open) port
    # on the relay
    # this is so when the pi is powered off, the doors
    # won't move
    GPIO.setup(valve, GPIO.OUT)
    GPIO.output(valve, GPIO.HIGH)  # default HIGH (off/closed)

@app.route('/')
def index():
    return render_template('index.html');

@app.route('/trigger')
def trigger():
    if (GPIO.input(valve) == GPIO.HIGH):
        GPIO.output(valve, GPIO.LOW)
    else:
        GPIO.output(valve, GPIO.HIGH)
    return "OK"

def getStatus():
    if (GPIO.input(valve) == GPIO.HIGH):
        return { "status" : "off"}
    else:
        return { "status" : "on"}

@app.route('/status')
def status():
    return getStatus()

@socketio.on('connect', namespace='/status')
def connect():
    log.debug("flask client connected")
    # always emit at connect so client can update
    socketio.emit('status', getStatus(), namespace='/status', broadcast=True)
    return "OK"

@socketio.on('disconnect', namespace='/status')
def test_disconnect():
    log.debug('flask client disconnected')

def loop(socketio):
    setupgpio()
    while True:
        # TODO: scheduled watering
        #log.debug("water on")
        #GPIO.output(valve, GPIO.LOW)
        #time.sleep(10)
        #log.debug("water off")
        #GPIO.output(valve, GPIO.HIGH)
        time.sleep(10)

def cleanup():
    log.debug("cleaning up")
    GPIO.cleanup()                      # Release all GPIO

if __name__ == '__main__':
    atexit.register(cleanup)
    t = Thread(target=loop, args=(socketio,))
    t.start()
    log.debug("starting HTTP")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False)