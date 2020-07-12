#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 20:13:41 2020

@author: sourav
"""

import os
import json
import threading 
import subprocess
import numpy as np
from surf_bow import SurfBow
from harris_corner import HarrisCorner
from encrypt_decrypt import EncryptDecrypt
from encrypted_image_receiver import receive_en_images
from encrypted_query_vector_sender import send_encrypted_query_vectors

key = (0.1, 0.1)
num_of_random_vectors = 16
hc = HarrisCorner()
sb = SurfBow()
e = EncryptDecrypt()
image_name = "/home/sourav/FinalYearProject/images/lena.bmp"
feat_vec = []

if not os.path.exists("encrypted_vectors/"):
    cwd = os.getcwd()
    directory = "/encrypted_vectors"
    os.mkdir(cwd+directory)
if not os.path.exists("decrypted_images/"):
    cwd = os.getcwd()
    directory = "/decrypted_images"
    os.mkdir(cwd+directory)

def send():
    features = hc.harris_corner(image_name)
    feature_vectors = sb.run_surf_and_bow(features)
    feat_vec.append(feature_vectors)
    data_vectors = np.asarray(feat_vec)
    data_vectors = np.squeeze(data_vectors)
    encrypted = e.encrypt_vectors(data_vectors.tobytes())
    with open('encrypted_vectors/query_vectors.json', 'w') as f:  # writing JSON object
        json.dump(list(encrypted), f)
    for root, dirs, files in os.walk("encrypted_vectors/"):
        for filename in files:
            send_encrypted_query_vectors("encrypted_vectors/"+filename)
    print("sent query vectors")
    subprocess.call("rm -rf encrypted_vectors/", shell = True)
    
def receive():
    receive_en_images()

# creating thread 
t1 = threading.Thread(target=send) 
t2 = threading.Thread(target=receive) 
  
# starting thread 1 
t1.start() 
# starting thread 2 
t2.start()

def clear():
    for root, dirs, files in os.walk("decrypted_images/"):
        for filename in files:
            image_name = filename
            subprocess.call("rm -rf decrypted_images/{}".format(image_name))
