from flask import Flask, session
from random import randrange
from os import system, name 
from firebase import firebase

app = Flask(__name__)
app.config['url'] = 'sqlite:///users.sqlite3'
app.secret_key = 'secret_key'

UserNum = "User " + str(randrange(10)) + ": "

result = "SEND MESSAGE\n"

while True: 
    system('clear') 
    
    print(result)

    fb = firebase.FirebaseApplication("https://dbcfv-60641-default-rtdb.europe-west1.firebasedatabase.app/", None)


    message = input("Type your message:   ")
    Smessage = UserNum + message

    data = {
	    'Message':Smessage
    }

    fb.post('dbcfv-60641-default-rtdb/Message', data)
    result = fb.get('dbcfv-60641-default-rtdb/Message', '')
