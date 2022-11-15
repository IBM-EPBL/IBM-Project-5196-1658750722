# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from random import randint

def send_mail(usermail,usersubject,usercontent,otp):
    if otp == "yes":
        content = '<strong>YOUR OTP:</strong>'+str(usercontent)
    else:
        content = usercontent

    message = Mail(
        from_email='roshanazar050@gmail.com',
        to_emails=str(usermail),
        subject=str(usersubject),
        html_content=str(content))





    try:
        sg = SendGridAPIClient('')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

#send_mail("roshanazar2002@gmail.com","Otp from news tracker","1234","yes")

def generate_number():
    number=randint(1001,9999)
    return number

#print(generate_number())
