import logging
import os

from flask import Flask
from flask_ask import Ask, request, session, question, statement
import RPi.GPIO as GPIO

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

STATUSON = ['on', 'high', 'enable']
STATUSOFF = ['off', 'low', 'disable']
valve = 8 # GPIO14

def toggle():
    if (GPIO.input(valve) == GPIO.HIGH):
        GPIO.output(valve, GPIO.LOW)
    else:
        GPIO.output(valve, GPIO.HIGH)
    return "OK"


@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('fireplaceIntent', mapping = {'status':'status'})
def Gpio_Intent(status,room):
    if status in STATUSON:
        GPIO.output(valve, GPIO.LOW)
        return statement('turning {} fireplace'.format(status))
    elif status in STATUSOFF:
        GPIO.output(valve, GPIO.HIGH)
        return statement('turning {} fireplace'.format(status))
    else:
        return statement('Sorry not possible.')

# we have to respond to all the 'required' intents
@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('AMAZON.CancelIntent')
def help():
    speech_text = 'cancelled'
    return question(speech_text).reprompt(speech_text).simple_card('cancelled', speech_text)

@ask.intent('AMAZON.StopIntent')
def help():
    speech_text = 'stopped'
    return question(speech_text).reprompt(speech_text).simple_card('stopped', speech_text)

@ask.intent('AMAZON.NavigateHomeIntent')
def help():
    speech_text = 'navigate'
    return question(speech_text).reprompt(speech_text).simple_card('navigate', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False

    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    GPIO.setup(valve,GPIO.OUT)
    GPIO.output(valve, GPIO.HIGH)  # default HIGH (off/closed)

    # to run using ngrok  ( ./ngrok http 5500)
    app.run(debug=True, port=5500)

    # to run using local https and certs
    #app.run(debug=True, port=5500, host='0.0.0.0', ssl_context=('/home/pi/sprinkler-pi/fullchain.pem', '/home/pi/sprinkler-pi/privkey.pem'))
