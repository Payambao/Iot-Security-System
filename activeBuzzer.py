import RPi.GPIO as GPIO
from time import sleep

BuzzerPin = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BuzzerPin, GPIO.OUT, initial=GPIO.LOW)

def buzz():
    GPIO.output(BuzzerPin, GPIO.HIGH)
    sleep(1)
    GPIO.output(BuzzerPin, GPIO.LOW)    
    
