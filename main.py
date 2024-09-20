import ssl
import time
import requests
import selectorlib
import os
import smtplib

PASSWORD = os.getenv("PASS3")
SENDER = "infocukamuran@gmail.com"
RECIEVER = "infocukamuran@gmail.com"
URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrap(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    valuel = extractor.extract(source)["tours"]
    return valuel


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


def read():
    with open("data.txt", "r") as file:
        cevap = file.read()
    return cevap


def send_email(message):
    message = f"""Subject: Hey new event was found\

{message}"""
    host = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECIEVER, message)
    print("Email was sent")


if __name__ == "__main__":
    while True:
        scrapped = scrap(URL)
        value = extract(scrapped)
        print(value)
        check = read()
        if value != "No upcoming tours":
            if value not in read():
                store(value)
                send_email(value)
        time.sleep(2)
