import threading
import phonenumbers

from rest_framework.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from twilio.rest import Client
from decouple import config

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
        
    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']]
        )
        if data.get('content_type') == 'html':
            email.content_subtype = 'html'
        EmailThread(email).start()

def send_email(email, code):
    html_content = render_to_string(
        'email/authentication/activate_account.html',
        {"code": code}
    )
    Email.send_email({
        "subject": "Registration",
        "to_email": email,
        "body": html_content,
        "content_type": "html"
    })
    
def send_phone_notification(phone_number, code):
    account_sid = config('ACCOUNT_SID')
    auth_token = config('AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"Hello everyone! Your verification code is {code}\n",
        from_="+123213123", # twilio number
        to=f"{phone_number}"
    )
    

def phone_checker(p_number):
    if not(p_number and isinstance(p_number, str) and p_number.isdigit()):
        raise ValidationError("phone_number is not valid")
    
    
def phone_parser(p_number, c_code=None):
    try:
        phone_checker(p_number)
        p_number = "+"+p_number
        return phonenumbers.parse(p_numbers, c_code)
    except Exception as e:
        raise ValidationError("Phone number is not valid")