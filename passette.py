#import the GPIO and time package
import RPi.GPIO as GPIO
import time
import os
#from mopidy import core

GPIO.setmode(GPIO.BOARD)

#yellow/back button
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#red/pause button
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#green/play button
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#white/next button
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#encoder | A - red | C - black | B - yellow
#pinA
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#pinB
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

count = 0
counter = 10
pinALast = GPIO.input(29)
pinBLast = GPIO.input(31)
pinCLast = pinALast ^ pinBLast
encoderMin = 0
encoderMax = 100
inc = 1

last_state = pinALast * 4 + pinBLast * 2 + pinCLast * 1

#system on start
os.system("mpc volume 10")

os.system("mpc add spotify:track:6jXPZid0KLorvgIDP6TiSo")
os.system("mpc add spotify:track:5GjPQ0eI7AgmOnADn1EO6Q")
os.system("mpc add spotify:track:6r20M5DWYdIoCDmDViBxuz")
os.system("mpc add spotify:track:17S4XrLvF5jlGvGCJHgF51")


while True:
    #back/yellow button 
    if GPIO.input(37) == GPIO.HIGH:
        os.system("mpc prev")
        print("'back' was pushed!")
        time.sleep(.3)
        
    #pause/red button
    if GPIO.input(36) == GPIO.HIGH:
        os.system("mpc pause")
        print("'pause' was pushed!")
        time.sleep(.3)
        
    #play/green button
    if GPIO.input(33) == GPIO.HIGH:
        os.system("mpc toggle")
        print("'play' was pushed!")
        time.sleep(.3)
        
    #next/white button
    if GPIO.input(32) == GPIO.HIGH:
        os.system("mpc next")
        print("'next' was pushed!")
        time.sleep(.3)
        
    #encoder
    pinA = GPIO.input(29)
    pinB = GPIO.input(31)
        
    pinC = pinA ^ pinB
        
    new_state = pinA * 4 + pinB * 2 + pinC * 1
        
    delta = (new_state - last_state) % 4
    
#    delta | pinA | pinB | pinC | new_state
#    ======================================
#      0   |   0  |   0  |   0  |    0
#      1   |   1  |   0  |   1  |    5
#      2   |   1  |   1  |   0  |    6
#      3   |   0  |   1  |   1  |    3

#    https://bobrathbone.com/raspberrypi/documents/Raspberry%20Rotary%20Encoders.pdf
    
    if (new_state != last_state):
        count += 1
        
        if (count % 4 == 1):

            if (delta == 3):
                counter += inc
                if (counter > encoderMax):
                    counter = 100
             
            else:
                counter -= inc
                if (counter < encoderMin):
                    counter = 0
                        
            volume = "mpc volume " + str(int(counter))
            os.system(volume)      
            
            last_state = new_state
        