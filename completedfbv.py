#!/usr/bin/env python3

#doing all needed imports
from os import system
from firebase import firebase
import threading
import subprocess as s
from sys import argv
from datetime import datetime
from playsound import playsound

fb = firebase.FirebaseApplication("https://dbcfv-60641-default-rtdb.europe-west1.firebasedatabase.app/", None)

#we're creating registration function that we'll need
def registr():
    password = 1
    password2 = 2
    while password != password2:
        name = input("type in  your name:   ") + '\n'
        email = input("type in your email:   ") + '\n'
        password = input("type your password:   ")
        password2 = input("reenter a password:   ")
    if password == password2:
        f = open("account.txt","w+")
        acc_sets = name + email + password
        f.write(acc_sets)
        f.close()
        data = {
            'Account':acc_sets
            }
        fb.post('Account', data)

#open file to check authorization
f = open("account.txt","r")
#reding the file
contents = f.read()
#we check if the file is empty
if contents == '':
    #if it isn't empty - do the registration
    registr()
else:
    contents #into server

username = ' ' + contents.split("\n", 1)[0] + ": "

#close file
f.close()

print("Hello, " + username)