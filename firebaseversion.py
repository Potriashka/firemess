#!/usr/bin/env python3

#doing all needed imports
from flask import Flask, session
from random import randrange
from os import system, name 
from firebase import firebase
import threading
import time
from pygame import mixer
import pygame
import subprocess as s

from sys import argv

sound = True

if len(argv) > 1:
    if argv[1] == "--notification-sound-off":
        sound = False

mixer.init()

#don't know how to call it but we need these things
app = Flask(__name__)
app.secret_key = 'secret_key'

#we need it to generate number for user
username = input("Type in your username: ") + ": "

system("clear")

#thanks to Python code won't work if this line doesn't exist
result = "\nSEND MESSAGE\n"

#we're creating db for our messages
fb = firebase.FirebaseApplication("https://dbcfv-60641-default-rtdb.europe-west1.firebasedatabase.app/", None)

old_data = {} 

def get_input_from_the_user():
    while True:
        #now we're asking for message and add user number
        message = input("Type your message:   ")
        Smessage = username + message

        #it is our data with messages
        data = {
            'Message':Smessage
        }

        fb.post('dbcfv-60641-default-rtdb/Message', data)

thread = threading.Thread(target=get_input_from_the_user)
thread.start()

pygame.mixer.music.load("noti2.wav")
#here's our loop so we'll be able to send messages over and over again
while True: 
    messages = fb.get(f'dbcfv-60641-default-rtdb/Message/', '')

    if messages:
        if old_data != messages:
            s.call(['notify-send','Perfect Messenger','New message!'])
            if sound: pygame.mixer.music.play(0)
            #it's "cls" for windows, here we'll clear console to everything looks ok
            system('clear')
            for message in messages:
                print(messages[message]["Message"])
    
            old_data = messages
            print(result)
