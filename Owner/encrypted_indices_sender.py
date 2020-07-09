#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 16:56:35 2020

@author: sourav
"""
"""
Client that sends the file (uploads)
"""
import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4 #4KB

def send_encrypted_indices(filename):
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to 127.0.0.1:4002")
    s.connect(("127.0.0.1", 4002))
    print("[+] Connected.")
    filesize = os.path.getsize(filename)
    # start sending the file
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    trigger = s.recv(4096)
    if trigger.decode() == 'Send':
        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            for _ in progress:
                while True:
                    data = f.read(512)
                    if len(data) == 0:
                        break
                    s.send(data)
                # update the progress bar
                progress.update(len(data))
    # close the socket
    s.close()
