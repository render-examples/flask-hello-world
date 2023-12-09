import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import sqlite3
import base64


def send_email_temperature(temperature):

    # Replace these values with your own email and server information
    sender_email = "put sender email here"
    receiver_email = "put receiver here"
    subject = "High temperature in the house"
    body = f"""Greetings Azhr,

    The radar perceived a temperature of {temperature} celsius which above the threshold set previously, you can decide whether or not to activate the alarm.

    If you want to activate it, please go to your account on https://homeradarproject.onrender.com/ and enter your credentials so you can access the alarm functionality.

    Stay Safe,

    homeRadar team
    """

    # Replace with your email server's information
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "put sender email here"
    smtp_password = "put password here"

    # Create the MIME object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
