import json

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
    msg["To"] = request.data["Email"]
    msg["Subject"] = "SmartHomie"
    data = {"status": "Success",
            "name": request.data["Name"],
            "manufacturer": request.data["Manufacturer"],
            "versionNumber": request.data["Version Number"],
            "description": request.data["Description"],
            "location": request.data["Location"],
            "message": request.data["Message"]}
    msg.attach(MIMEText(json.dumps(data, sort_keys=True, indent=4), "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:

        server.login(senderInfo["email"], senderInfo["password"])
        server.sendmail(senderInfo["email"], request.data["Email"], msg.as_string())

        return Response(data=json.dumps(data), status=status.HTTP_200_OK)
    except Exception as _:
        return Response(data="Fail", status=status.HTTP_403_FORBIDDEN)
    finally:
        server.quit()
