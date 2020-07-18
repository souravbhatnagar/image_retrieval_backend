#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 16:59:57 2020

@author: sourav
"""
"""
Server receiver of the file
"""


import socket
import tqdm
import os
from encrypt_decrypt import EncryptDecrypt

# device's IP address
SERVER_HOST = "18.188.19.1"
SERVER_PORT = 4006
# receive 4096 bytes each time
BUFFER_SIZE = 512
SEPARATOR = "<SEPARATOR>"
e = EncryptDecrypt()
key = (0.1, 0.1)

def receive_en_images():
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    # accept connection if there is any
    while True:
        # create the server socket
        # TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to our local address
        s.connect((SERVER_HOST, SERVER_PORT))
        # enabling our server to accept connections
        # 1 here is the number of unaccepted connections that
        # the system will allow before refusing new connections
        received = s.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)
        s.send("Send".encode())
        # if below code is executed, that means the sender is connected
        print(f"[+] {SERVER_HOST} is connected.")
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(".decrypted_images/"+filename, "wb") as f:
            for _ in progress:
                # read 512 bytes from the socket (receive)
                bytes_read = s.recv(BUFFER_SIZE)
                while bytes_read:
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    bytes_read = s.recv(BUFFER_SIZE)
                # update the progress bar
                progress.update(len(bytes_read))
        e.decrypt_image(".decrypted_images/", filename, key)
        print(f"Decrypted {filename}")
        # close the client socket
        s.close()
