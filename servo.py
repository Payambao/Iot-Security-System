import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.OUT)
servo1 = GPIO.PWM(24,50) 

# Start PWM running, with value of 0
servo1.start(0)

#servo will rotate 90 degree to the right
def rightKey():
    servo1.ChangeDutyCycle(2+(0/18))
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)

#servo will rotate 90 degree to the left
def leftKey():
    servo1.ChangeDutyCycle(2+(90/18))
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
