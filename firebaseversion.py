#!/usr/bin/env python3

#DOING ALL NEEDED IMPORTS
from flask import Flask, session
from random import randrange
from os import system, name 
from firebase import firebase
import threading
import time

#DON'T KNOW HOW TO CALL IT BUT WE NEED THESE THINGS
app = Flask(__name__)
app.secret_key = 'secret_key'

#WE NEED IT TO GENERATE NUMBER FOR USER
UserNum = "User " + str(randrange(10)) + ": "

#THANKS TO PYTHON CODE WON'T WORK IF THIS LINE DOESN'T EXIST
result = "SEND MESSAGE\n"

#MAYBE WE'LL NEED IT
i = 0

#HERE'S OUR LOOP SO WE'LL BE ABLE TO SEND MESSAGES OVER AND OVER AGAIN
while True: 
    #IT'S "cls" FOR WINDOWS, HERE WE'LL CLEAR CONSOLE TO EVERYTHING LOOKS OK
    system('clear') 

    #ALL MESSAGES WILL BE HERE UP THE INPUT    
    def print_result():
        print(result)

    print_result()

    #WE'RE CREATING DB FOR OUR MESSAGES
    fb = firebase.FirebaseApplication("https://dbcfv-60641-default-rtdb.europe-west1.firebasedatabase.app/", None)

    #NOW WE'RE ASKING FOR MESSAGE AND ADD USER NUMBER
    message = input("Type your message:   ")
    Smessage = UserNum + message

    #IT IS OUR DATA WITH MESSAGES
    data = {
	    'Message':Smessage
    }

    #HERE WE'RE TRYING TO GET !ALL! MESSAGES
    path = fb.post('dbcfv-60641-default-rtdb/Message', data)
    Npath = str(path)[10:30]
    result = fb.get(f'dbcfv-60641-default-rtdb/Message/', '')
