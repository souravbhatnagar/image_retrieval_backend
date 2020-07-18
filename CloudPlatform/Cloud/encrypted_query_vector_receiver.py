#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 16:20:53 2020

@author: sourav
"""
"""
encrypted query vectors receiver of the file
"""


import tqdm
import os
from cloud_main import CloudMain
import socket

SEPARATOR = "<SEPARATOR>"

def receive_query_vectors(sendersock):
    # device's IP address
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 4004
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    # create the server socket
    # TCP socket
    s = socket.socket()
    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))
    # enabling our server to accept connections
    # 1 here is the number of unaccepted connections that
    # the system will allow before refusing new connections
    s.listen(1)
    # if below code is executed, that means the sender is connected
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    while True:
        client_socket, address = s.accept()
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)
        client_socket.send("Send".encode())
        # if below code is executed, that means the sender is connected
        print(f"[+] {address} is connected.")
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(".encrypted_query/"+filename, "wb") as f:
            for _ in progress:
                # read 4096 bytes from the socket (receive)
                bytes_read = client_socket.recv(BUFFER_SIZE)
                while bytes_read:
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                # update the progress bar
                progress.update(len(bytes_read))
        path, dirs, files = next(os.walk(".encrypted_images/"))
        file_count = len(files)
        CloudMain().cloud_main(file_count, sendersock)
        # close the client socket
        client_socket.close()
