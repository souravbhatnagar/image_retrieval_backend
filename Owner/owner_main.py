#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 18:41:09 2020

@author: sourav
"""
from harris_corner import HarrisCorner
from surf_bow import SurfBow
from encrypt import Encrypt
from lsh import LSH
from encrypted_image_sender import send_encrypted_images
from encrypted_indices_sender import send_encrypted_indices
from encrypted_feature_vector_sender import send_encrypted_feature_vectors
import os
import json
import subprocess
import numpy as np
import mysql.connector

#establishing the connection
#MySQL related information needs to be update here
conn = mysql.connector.connect(
   user='<user>', password='<password>', host='127.0.0.1', database='ImageRetrieval')
#Creating a cursor object using the cursor() method
cursor = conn.cursor()
# Preparing SQL query to INSERT a record into the database.
insert_stmt = (
   "insert into images (path)"
   "values (%s)"
)
key = (0.1, 0.1)
num_of_random_vectors = 16
hc = HarrisCorner()
sb = SurfBow()
e = Encrypt()
l = LSH()
#Image directory path to be mentioned here
img_dir = "../images/"
feat_vec=[]

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

for root, dirs, files in os.walk(img_dir):
    for filename in files:
        image_name = filename
        e.encrypt_image(img_dir, image_name, key)
        print("Encrypted image:",image_name)
        features = hc.harris_corner(img_dir+image_name)
        feature_vectors = sb.run_surf_and_bow(features)
        feat_vec.append(feature_vectors)
        data = ('encrypted_images/'+image_name.split(".")[0]+".png",)
        try:
           # Executing the SQL command
           cursor.execute(insert_stmt, data)
           # Commit your changes in the database
           conn.commit()
        except:
           # Rolling back in case of error
           conn.rollback()
# Closing the connection
conn.close()
print("Generated vectors")
data_vectors = np.asarray(feat_vec)
data_vectors = np.squeeze(data_vectors)
encrypted_fv = e.encrypt_vectors(data_vectors.tobytes())
indices = l.generate_indices(data_vectors, num_of_random_vectors)
indices = json.dumps(indices)
encrypted_i = e.encrypt_indices(str.encode(indices))
with open('encrypted_indices/indices.json', 'w', encoding='utf-8') as f:
    json.dump(list(encrypted_i), f, ensure_ascii=False, indent=4)
with open('encrypted_vectors/feature_vectors.json', 'w', encoding='utf-8') as f:
    json.dump(list(encrypted_fv), f, ensure_ascii=False, indent=4)
for root, dirs, files in os.walk("encrypted_images/"):
    for filename in files:
        print(filename)
        send_encrypted_images("encrypted_images/"+filename)
print("sent library")
#removing enrypted images directory
subprocess.call("rm -rf encrypted_images/", shell = True)
for root, dirs, files in os.walk("encrypted_vectors/"):
    for filename in files:
        send_encrypted_feature_vectors("encrypted_vectors/"+filename)
print("sent feature vectors")
#removing enrypted vectors directory
subprocess.call("rm -rf encrypted_vectors/", shell = True)
for root, dirs, files in os.walk("encrypted_indices/"):
    for filename in files:
        send_encrypted_indices("encrypted_indices/"+filename)
print("sent indices")
#removing enrypted indices directory
subprocess.call("rm -rf encrypted_indices/", shell = True)
