#!/usr/bin/env python3

#doing all needed imports
from flask import Flask, session
from random import randrange
from os import system, name 
from firebase import firebase
import threading
import time
 
#don't know how to call it but we need these things
app = Flask(__name__)
app.secret_key = 'secret_key'

#we need it to generate number for user
UserNum = "User " + str(randrange(10)) + ": "

#thanks to Python code won't work if this line doesn't exist
result = "SEND MESSAGE\n"

#maybe we'll need it
i = 0

#we're creating db for our messages
fb = firebase.FirebaseApplication("https://dbcfv-60641-default-rtdb.europe-west1.firebasedatabase.app/", None)
 
# messages = []

#here's our loop so we'll be able to send messages over and over again
while True: 
    messages = fb.get(f'dbcfv-60641-default-rtdb/Message/', '')
    for message in messages:
        print(fb.get(f'dbcfv-60641-default-rtdb/Message/' + message + "/Message", ''))
 
 
    #all messages will be here up the input  
    def print_result():
        print(result)
 
    print_result()
 

    #now we're asking for message and add user number
    message = input("Type your message:   ")
    Smessage = UserNum + message

    #it is our data with messages
    data = {
	    'Message':Smessage
    }

    #here we're trying to get all messages
    path = fb.post('dbcfv-60641-default-rtdb/Message', data)
    Npath = str(path)[10:30]
 
    # messages.append(Npath)
 
    #it's "cls" for windows, here we'll clear console to everything looks ok
    system('clear') 
 
 
result = fb.get(f'dbcfv-60641-default-rtdb/Message/{Npath}/Message', '')
