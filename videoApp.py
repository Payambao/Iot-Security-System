import telepot
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime
from telepot.loop import MessageLoop
from subprocess import call
import drivers
import rgb

import messageScreen
import activeBuzzer

display = drivers.Lcd()
PIR = 17
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25

GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)

motion = 0
motionNew = 0
 
def handle(msg):
    global telegramText
    global chat_id
  
    chat_id = msg['chat']['id']
    telegramText = msg['text']
  
    print('You have received a new message from ' + str(chat_id))
  
    if telegramText == '/start':
        bot.sendMessage(chat_id, 'Anomaly Detected.')#Put your welcome note here

    while True:
        video()
    


bot = telepot.Bot('5005647654:AAE_JoW_64unWMK8bUbamjFQvLm7MNmlgYY')
bot.message_loop(handle)        

def video():
        
    global chat_id
    global motion 
    global motionNew
    
    if GPIO.input(PIR) == 1:
        print("Anomaly detected")
        motion = 1
        if motionNew != motion:
            motionNew = motion
            sendNotification(motion)
            
            
    elif GPIO.input(PIR) == 0:
        print("No motion detected")
        motion = 0
        if motionNew != motion:
            motionNew = motion


def sendNotification(motion):   

    global chat_id
    
    if motion == 1:
        rgb.lightBlue()
        messageScreen.systemOn()
        sleep(2)
        activeBuzzer.buzz()
        display.lcd_clear()
        rgb.turnOff()
        filename = "./video_" + (time.strftime("%y%b%d_%H%M%S"))
        camera.start_recording(filename + ".h264")
        sleep(5)
        camera.stop_recording()
        command = "MP4Box -add " + filename + '.h264' + " " + filename + '.mp4'
        print(command)
        call([command], shell=True)
        bot.sendVideo(chat_id, video = open(filename + '.mp4', 'rb'))
        bot.sendMessage(chat_id, 'Theres a movement detected.')

        

#while 1:
 #time.sleep(10)    