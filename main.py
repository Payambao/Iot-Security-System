import pygame
import os
import glob
import picamera
import smtplib
import drivers

import RPi.GPIO as GPIO

from gpiozero import Buzzer
from threading import Thread
from time import sleep

# Importing modules for sending mail
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

#importing the other files created 
import messageScreen
import servo
import activeBuzzer
import passiveBuzzer
import rgb
import videoApp

display = drivers.Lcd()
buzz = Buzzer(14)
def init():
    pygame.init()
    win = pygame.display.set_mode((100,100))
    
def getKey(keyName):
    ans = False
    for eve in pygame.event.get():pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    if keyInput [myKey]:
        ans = True
    pygame.display.update()
    
    return ans

sender = 'imvtaehyung@gmail.com'
password = 'testtest'
receiver = 'imvtaehyung@gmail.com'

DIR = './Database/'
FILE_PREFIX = 'image'
            
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)  # Read output from PIR motion sensor

def send_mail():
    print 'Sending E-Mail'
    # Create the directory if not exists
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    # Find the largest ID of existing images.
    # Start new images after this ID value.
    files = sorted(glob.glob(os.path.join(DIR, FILE_PREFIX + '[0-9][0-9][0-9].jpg')))
    count = 0
    
    if len(files) > 0:
        # Grab the count from the last filename.
        count = int(files[-1][-7:-4])+1

    # Save image to file
    filename = os.path.join(DIR, FILE_PREFIX + '%03d.jpg' % count)
    # Capture the face
    with picamera.PiCamera() as camera:
        pic = camera.capture(filename)
    # Sending mail
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Movement Detected'
    
    body = 'Picture is Attached.'
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()
        
def main():
    if getKey('a'):
        display.lcd_clear()
        messageScreen.systemOff()
        rgb.red()
        sleep(2)
        display.lcd_clear()
        
    if getKey('b'):
        videoApp.handle(msg)
        videoApp.video()
        videoApp.sendNotification(motion)   
        
    if getKey('x'):
        for x in range(6):
            i = GPIO.input(17)
            if i == 0:  # When output from motion sensor is LOW
                print "No intruders", i
                rgb.turnOff()
                sleep(0.3)
                
            elif i == 1:  # When output from motion sensor is HIGH
                print "Intruder detected", i
                rgb.purple()
                sleep(0.3)
                #passiveBuzzer.setup()
                #passiveBuzzer.superMario()
                messageScreen.anomalyDetected()
                #send_mail()
        return
                
    if getKey('LEFT'):
        servo.rightKey()
        rgb.blue()
        
    if getKey('RIGHT'):
        servo.leftKey()
        rgb.white()
        
if __name__ == '__main__':
    init()
    while True:
        main()