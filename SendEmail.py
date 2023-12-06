import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import sqlite3
import base64


def send_email():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Query the image data from the database
    cursor.execute('SELECT image FROM images ORDER BY id DESC LIMIT 1')
    image_data = cursor.fetchone()

    # Close the database connection
    conn.close()

    # Replace these values with your own email and server information
    sender_email = "esp32project422@gmail.com"
    receiver_email = "azhr.lrhezzioui@mail.concordia.ca"
    subject = "Suspected activity in your house"
    body = """Greetings Azhr,

    The radar perceived a suspected activity in the house, so a picture was taken so you can decide whether or not to activate the alarm.

    If you want to activate it, please go to your account on https://homeradarproject.onrender.com/ and enter your credentials so you can access the alarm functionality.

    Stay Safe,

    homeRadar team
    """

    # Replace with the path to the JPEG file you want to attach
    png_attachment_path = "image.png"

    # Replace with your email server's information
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "esp32project422@gmail.com"
    smtp_password = "ijah yexk puwg ioov"

    # Create the MIME object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Attach the JPEG file
    # with open(png_attachment_path, "rb") as attachment:
    #     image_part = MIMEImage(attachment.read(), name="image.png")
    #     message.attach(image_part)
    if image_data:
        image_data = image_data[0]

        # Convert binary image data to base64
        base64_data = base64.b64encode(image_data).decode('utf-8')

        # Convert base64 data to binary
        binary_data = base64.b64decode(base64_data)
        image_part = MIMEImage(binary_data, name="image.png")
        message.attach(image_part)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
