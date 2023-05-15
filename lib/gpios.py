from mimetypes import init
import RPi.GPIO as GPIO

PIN_PUMP7 = 19
PIN_PUMP8 = 26
PIN_EV7 = 16
PIN_EV8 = 20
PIN_TIRETTE = 17
PIN_BAU = 21
PIN_SICK = 23


GPIO_Initialized = False
def init_pin(id, output = False, pud_up = True, output_up = True):
    global GPIO_Initialized
    if not GPIO_Initialized:
        GPIO.setmode(GPIO.BCM)
        GPIO_Initialized = True
    if (output):
        GPIO.setup(id, GPIO.OUT)
        if (output_up):
            GPIO.output(id, GPIO.HIGH)
        else:
            GPIO.output(id, GPIO.LOW)
    else:
        if (pud_up):
            GPIO.setup(id, GPIO.IN, GPIO.PUD_UP)
        else:
            GPIO.setup(id, GPIO.IN, GPIO.PUD_DOWN)
def get_pin(id):
    return GPIO.input(id)
def set_pin(id):
    GPIO.output(id, GPIO.HIGH)
def clear_pin(id):
    GPIO.output(id, GPIO.LOW)
