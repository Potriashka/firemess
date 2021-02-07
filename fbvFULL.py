#!/usr/bin/env python3

#doing all needed imports
from os import system
from firebase import firebase
import threading
import subprocess as s
from sys import argv
from datetime import datetime
from playsound import playsound
import os

#we're creating db for our messages
fb = firebase.FirebaseApplication("https://dbcfv-60641-default-rtdb.europe-west1.firebasedatabase.app/", None)

contents = None
#we're creating registration function that we'll need
def registr():
    global contents
    password = 1
    password2 = 2
    key = None
    #we need user to write his password rightly
    while password != password2:
        #ask user about their data
        name = input("type in  your name:   ") + '\n'
        email = input("type in your email:   ") + '\n'
        password = input("type your password:   ")
        password2 = input("reenter a password:   ")
        key = int(input("Key (number): "))
    #if both password are alright:
    if password == password2:
        temp = ""
        for char in password:
            temp += chr(int(ord(char))+key)
        password = temp
        f = open("account.txt","w")
        #we need it to send data to db
        acc_sets = name + email + password
        f.write(acc_sets + "\n" + str(key))
        f.close()
        contents = acc_sets
        data = {
            'Account':acc_sets
            }
        fb.post('Account', data)



#open file to check authorization
try:
    f = open("account.txt","r")
    #reding the file
    contents = f.read()
    f.close()
except: registr()

#we write user name (it won't work for the first time)
username = ' ' + contents.split("\n", 1)[0] + ": "

#close file




#we need it to that thing down here
sound = True

#here's that thing. If you don't want notification sound - turn off it!
if len(argv) > 1:
    if argv[1] == "--notification-sound-off":
        sound = False

#it's "cls" for windows, here we'll clear console to everything looks ok
system("clear")

#thanks to Python code won't work if this line doesn't exist
result = "\nSEND MESSAGE\n"


#it is our old data so we can compare it with new and messages will be updated
old_data = {} 

#it's a function where we take user's input
def get_input_from_the_user():
    while True:
        #now we're asking for message and add user number
        message = input()
        
        if "(yes)" in message:
            message = message.replace("(yes)", "👍")
        if "(y)" in message:
            message = message.replace("(y)", "👍")
        if "(no)" in message:
            message = message.replace("(no)", "👎")
        if "(cryingwithlaughter)" in message:
            message = message.replace("(cryingwithlaughter)", "😂")

        if message == "/logout":
            os.remove("account.txt")
            quit()

        elif message == "/clear":
            system("clear")
            fb.delete('Message', '')

        elif message.startswith("/reply"):
            original = ""
            message_id = ""
            msg = message.split()
            if len(msg) > 3:
                time_and_username = msg[1] + " " + msg[2]
                edited_message = ""
                for word in msg:
                    if msg.index(word) > 2:
                        edited_message += word + " "
                for m in messages:
                    if messages[m]["Message"].startswith(time_and_username):
                        message_id = m
                        original = messages[m]["Message"]
                current_time = str(datetime.now().time())[:8]
                fb.put(f'Message/{message_id}/', 'Message', original + "↓\n" + current_time + username + edited_message + "↑")
            message_id = ""
            original = ""
            message = ""
            edited_message = ""


        elif message.startswith("/edit"):
            message_id = ""
            msg = message.split()
            if len(msg) > 3:
                time_and_username = msg[1] + " " + msg[2]
                if username.strip().startswith(msg[2].strip()):
                    edited_message = ""
                    for word in msg:
                        if msg.index(word) > 2:
                            edited_message += word + " "
                    for msg in messages:
                        if messages[msg]["Message"].startswith(time_and_username):
                            message_id = msg
                    fb.put(f'Message/{message_id}/', 'Message', str(datetime.now().time())[:8] + username + "EDITED " + edited_message)
                else: print("You can only edit your own messages.", username, message[2])

        else:
            Smessage = str(datetime.now().time())[:8] + username + message

            #it is our data with messages
            data = {
                'Message':Smessage
            }

            #as you can see we post out message to db
            fb.post('Message', data)

#thanks to this line we can do 2 things (get input and print messages) at once
thread = threading.Thread(target=get_input_from_the_user)
thread.start()

#here's our loop so we'll be able to send messages over and over again
while True: 
    #we're taking messages from db
    messages = fb.get(f'/Message/', '')

    #if messages came:
    if messages:
        if old_data != messages: #if sth new in messages:
            try:
                message = messages[list(messages.keys())[-1]]["Message"]
                print(message)
                author = message.split()[1].strip()
                if " " + author + " " != username:
                    #create notification banner
                    s.call(['notify-send','Perfect Messenger', message])
                    if sound: playsound("noti2.wav") #and here's sound if it turned on
                #it's "cls" for windows, here we'll clear console to everything looks ok
                system('clear')
                for message in messages:
                    print(messages[message]["Message"])

                old_data = messages
                print(result)
            except Exception as e:
                print(e)
