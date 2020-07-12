#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 22:05:28 2020

@author: sourav
"""

import numpy as np
import json
from decrypt import Decrypt
from lsh import LSH
from cloud_api_sender import CloudAPISender
import mysql.connector


class CloudMain():
    def cloud_main(self, file_count):
        #establishing the connection
        conn = mysql.connector.connect(
           user='root', password='Sourav@98', host='127.0.0.1',
           database='ImageRetrieval')
        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        # Preparing SQL query to select a record from the database.
        sql_select_Query = "select * from images"
        with open('encrypted_vectors/feature_vectors.json') as data_file:
            feature_loaded = json.load(data_file)
        with open('encrypted_indices/indices.json') as data_file:
            indices_loaded = json.load(data_file)
        with open('encrypted_query/query_vectors.json') as data_file:
            query_loaded = json.load(data_file)
        d = Decrypt()
        feature_vectors = d.decrypt_indices_vector(bytes(feature_loaded))
        indices = d.decrypt_indices_vector(bytes(indices_loaded))
        query_vectors = d.decrypt_indices_vector(bytes(query_loaded))
        feature_vectors = np.frombuffer(feature_vectors, dtype=int)
        feature_vectors = np.reshape(feature_vectors, (file_count, -1))
        indices = json.loads(indices.decode())
        query_vectors = np.frombuffer(query_vectors, dtype=int)
        query_vectors = np.reshape(query_vectors, (-1, 6))
        print(feature_vectors.shape, indices, query_vectors.shape)
        l = LSH(feature_vectors, indices)
        n_neighbors, result = l.query(query_vectors, 6, 45)
        print(n_neighbors)
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            if row[0]-1 in result:
                image_name = row[1]
                print(image_name)
                CloudAPISender().cloud_api_sender(image_name)
        # Closing the connection
        conn.close()