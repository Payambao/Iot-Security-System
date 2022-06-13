import RPi.GPIO as GPIO

#imported the libraries found in Github
import I2C_LCD_driver
import drivers

from time import *
from time import sleep

display = drivers.Lcd()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def systemOff():
    display.lcd_display_string("Status: INACTIVE", 1)

def systemOn():
    display.lcd_display_string("Status: ACTIVE", 1)
    
def anomalyDetected():
    display.lcd_display_string("WARNING:", 1)
    display.lcd_display_string("Anomaly Detected", 2)
    display.lcd_clear()