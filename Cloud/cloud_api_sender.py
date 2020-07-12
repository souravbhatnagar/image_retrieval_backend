#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 22:05:28 2020

@author: sourav
"""

import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"

class CloudAPISender():
        def cloud_api_sender(self, result_image):
                # create the client socket
                s = socket.socket()
                print("[+] Connecting to 127.0.0.1:4002")
                s.connect(("127.0.0.1", 4006))
                print("[+] Connected.")
                filesize = os.path.getsize(result_image)
                # start sending the file
                s.send(f"{result_image}{SEPARATOR}{filesize}".encode())
                trigger = s.recv(4096)
                if trigger.decode() == 'Send':
                    # start sending the file
                    progress = tqdm.tqdm(range(filesize), f"Sending {result_image}", unit="B", unit_scale=True, unit_divisor=1024)
                    with open(result_image, "rb") as f:
                        for _ in progress:
                            while True:
                                data = f.read(512)
                                if len(data) == 0:
                                    break
                                s.sendall(data)
                            # update the progress bar
                            progress.update(len(data))
                # close the socket
                s.close()