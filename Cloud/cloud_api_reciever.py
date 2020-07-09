#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 22:05:28 2020

@author: sourav
"""


import os
import threading
from encrypted_images_receiver import receive_images
from encrypted_indices_receiver import receive_indices
from encrypted_query_vector_receiver import receive_query_vectors
from encrypted_feature_vector_receiver import receive_feature_vectors

if not os.path.exists("encrypted_images/"):
        cwd = os.getcwd()
        directory = "/encrypted_images"
        os.mkdir(cwd+directory)
if not os.path.exists("encrypted_indices/"):
        cwd = os.getcwd()
        directory = "/encrypted_indices"
        os.mkdir(cwd+directory)
if not os.path.exists("encrypted_vectors/"):
        cwd = os.getcwd()
        directory = "/encrypted_vectors"
        os.mkdir(cwd+directory)
if not os.path.exists("encrypted_query/"):
        cwd = os.getcwd()
        directory = "/encrypted_query"
        os.mkdir(cwd+directory)

def receive_en_images():
    receive_images()
    
def receive_en_indices():
    receive_indices()
    
def receive_en_feature_vectors():
    receive_feature_vectors()

def receive_en_query_vectors():
    receive_query_vectors()

# creating thread 
t1 = threading.Thread(target=receive_en_images) 
t2 = threading.Thread(target=receive_en_indices) 
t3 = threading.Thread(target=receive_en_feature_vectors)
t4 = threading.Thread(target=receive_en_query_vectors)

# starting thread 1 
t1.start() 
# starting thread 2 
t2.start()
# starting thread 3
t3.start()
# starting thread 4
t4.start()
