#!/usr/bin/env python3

#doing all needed imports
from random import randrange
from os import system, name 
from firebase import firebase
import threading
import time
from pygame import mixer
import pygame
import subprocess as s
from sys import argv
from datetime import datetime

#we need it to that thing down here
sound = True

#here's that thing. If you don't want notification sound - turn off it!
if len(argv) > 1:
    if argv[1] == "--notification-sound-off":
        sound = False

#initialising our mixer for notification sound
mixer.init()

#we need it to generate number for user
username = ' ' + input("Type in your username: ") + ": "

#it's "cls" for windows, here we'll clear console to everything looks ok
system("clear")

#thanks to Python code won't work if this line doesn't exist
result = "\nSEND MESSAGE\n"

#we're creating db for our messages
fb = firebase.FirebaseApplication("https://dbcfv-60641-default-rtdb.europe-west1.firebasedatabase.app/", None)

#it is our old data so we can compare it with new and messages will be updated
old_data = {} 

#it's a function where we take user's input
def get_input_from_the_user():
    while True:
        #now we're asking for message and add user number
        message = input("Type your message:   ")
        
        if "(yes)" in message:
            message = message.replace("(yes)", "👍")
        elif "(y)" in message:
            message = message.replace("(y)", "👍")
        elif "(no)" in message:
            message = message.replace("(no)", "👎")

        elif message == "/clear":
            fb.delete('dbcfv-60641-default-rtdb/', '')

        else:
            pass

        Smessage = str(datetime.now().time())[:8] + username + message

        #it is our data with messages
        data = {
            'Message':Smessage
        }

        #as you can see we post out message to db
        fb.post('dbcfv-60641-default-rtdb/Message', data)

#thanks to this line we can do 2 things (get input and print messages) at once
thread = threading.Thread(target=get_input_from_the_user)
thread.start()

#here's our notification sound (you need to download needed file)
pygame.mixer.music.load("noti2.wav")

#here's our loop so we'll be able to send messages over and over again
while True: 
    #we're taking messages from db
    messages = fb.get(f'dbcfv-60641-default-rtdb/Message/', '')

    #if messages came:
    if messages:
        if old_data != messages: #if sth new in messages:
            message = messages[list(messages.keys())[-1]]["Message"]
            author = message.split()[1].strip()
            if " " + author + " " != username:
                #create notification banner
                s.call(['notify-send','Perfect Messenger', message])
                if sound: pygame.mixer.music.play(0) #and here's sound if it turned on
            #it's "cls" for windows, here we'll clear console to everything looks ok
            system('clear')
            if "/edit" in message:
                message_id = ""
                message = message.split()
                time_and_username = message[1] + " " + message[2]
                edited_message = ""
                for word in message:
                    if message.index(word) > 2:
                        edited_message += word + " "
                for msg in messages:
                    if messages[msg]["Message"].startswith(time_and_username):
                        message_id = msg
                fb.put(f'dbcfv-60641-default-rtdb/Message/{message_id}/', 'Message', edited_message)
            for message in messages:
                print(messages[message]["Message"])

            old_data = messages
            print(result)
