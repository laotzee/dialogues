from os import environ
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

SENDER_EMAIL = environ.get("from_email")
RECEIVER_EMAIL = environ.get("to_email")
EMAIL_KEY = environ.get("email_key")
PORT = int(environ.get("port"))
SMTP_SERVER = environ.get("smtp_server")
EMAIL_SUBJECT = "Someone wants to contact you through Dialogues!"

def send_email(msg):
    """Establish connection to the stmp server and sends a formatted message"""

    with smtplib.SMTP(SMTP_SERVER, PORT) as conn:

        conn.starttls()
        conn.login(
            SENDER_EMAIL,
            EMAIL_KEY,
        )
        conn.sendmail(
            SENDER_EMAIL,
            RECEIVER_EMAIL,
            msg.as_string(),
        )

def format_message(body):
    """Formats an email to be sent using a body of text, and a sender and receiver emails"""

    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = EMAIL_SUBJECT
    message.attach(MIMEText(body, "plain"))

    return message

def message_template(name, email, text):

    message = f'''"{text}"\n Message from {name}\n{email}'''
    return message

if __name__ == "__main__":

    pass