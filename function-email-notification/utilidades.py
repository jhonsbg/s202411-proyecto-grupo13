from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_email(to, subject, body):
    sender = "grupo13.nubeuniandes@gmail.com"
    password = "jzed jiux mhfm wfsg"

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, to, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False