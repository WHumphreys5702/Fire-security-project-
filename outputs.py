from twilio.rest import Client
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys





def write(message,line):
    lines = open("configurations.txt","r").readlines()
    lines[line] = message + "\n"
    out = open("configurations.txt","w")
    out.writelines(lines)
    out.close()
    
def read(line):
    f = open("configurations.txt", "r")
    ok = f.readlines()
    specific = ok[line]
    ok = specific.strip()
    f.close()
    return ok


# reads and stores variables in text file by the position of the lines
cellphone = read(0)
address = read(1)
email = read(2)

# used for the twilio API
client = Client('AC44713aa5abfa414473e1f21ae77a7e5c', 'ed37412bf05a613181ec4c8728cdda90')
message= "Alert! We have detected a fire at {}. Check your email at {} for a picture".format(address, email) 

def text():
    client.messages.create( body = message, from_='+17432093292', to= cellphone)
    


def call():
    client.calls.create( twiml= message, to= cellphone, from_= '+17432093292')

# we couldnt get the email function to work in time



