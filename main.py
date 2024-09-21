import ssl
import time
import requests
import selectorlib
import os
import sqlite3
import smtplib

connection = sqlite3.connect("data.db")
# cursor = connection.cursor()

"""
SELECT * FROM events WHERE city='Ben City'
INSERT INTO events VALUES ('Ben','Ben City','2034.10.09')
DELETE FROM events WHERE band='Ben'
"""

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
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", extracted)
    connection.commit()

# execute tuple verir executemany liste verir !!!!!!


def read(values):
    cursor = connection.cursor()
    # cursor.execute("SELECT * FROM events")
    # veri = cursor.fetchall()
    band, city, date = values
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    veri = cursor.fetchall()
    print(veri)
    return veri


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
        # value2 = value.split(", ")
        value2 = value.split(",")
        value2 = [i.strip() for i in value2]
        # value2 = [tuple(value2)]
        if value != "No upcoming tours":
            check = read(value2)
            # if value2[0] not in read():
            if not check:
                store(value2)
                send_email(value)
        time.sleep(2)
