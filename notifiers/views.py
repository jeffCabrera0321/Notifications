from django.shortcuts import render
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
import os

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

load_dotenv()


# Create your views here.
@api_view(["POST"])
def sendEmail(request):
    senderInfo = {
        "userName": os.getenv("username"),
        "email": os.getenv("email"),
        "password": os.getenv("password")
    }

    msg = MIMEMultipart()
    msg["From"] = os.getenv("email")
    msg["To"] = request.data["email"]
    msg["Subject"] = "SmartHomie"

    msg.attach(MIMEText(request.data["message"], "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(senderInfo["email"], senderInfo["password"])

        server.sendmail(senderInfo["email"], request.data["email"], msg.as_string())
        return Response(data="Success", status=status.HTTP_200_OK)
    except Exception as _:
        return Response(data="Fail", status=status.HTTP_403_FORBIDDEN)
    finally:
        server.quit()
