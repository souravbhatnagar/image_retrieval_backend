#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 19:56:09 2020

@author: sourav
"""

import cv2
import numpy as np
from sklearn import cluster as cl

class SurfBow():
    def __init__(self):
        self.num_cluster = 6

    def read_and_clusterize(self):
        surf_keypoints = []
        # surf extraction
        surf = cv2.xfeatures2d.SURF_create()
        kp, descriptors = surf.detectAndCompute(self.val, None)
        #append the descriptors to a list of descriptors
        surf_keypoints.append(descriptors)
        surf_keypoints=np.asarray(surf_keypoints)
        surf_keypoints=np.concatenate(surf_keypoints, axis=0)
        #with the descriptors detected, lets clusterize them
        kmeans = cl.MiniBatchKMeans(n_clusters=self.num_cluster, random_state=0).fit(surf_keypoints)
        #return the learned model
        return kmeans

    def calculate_centroids_histogram(self, model):
        feature_vectors=[]
        #SURF extraction
        surf = cv2.xfeatures2d.SURF_create()
        kp, descriptors = surf.detectAndCompute(self.val, None)
        #classification of all descriptors in the model
        predict_kmeans=model.predict(descriptors)
        #calculates the histogram
        hist, bin_edges=np.histogram(predict_kmeans, bins=6)
        #histogram is the feature vector
        feature_vectors.append(hist)
        feature_vectors=np.asarray(feature_vectors)
        #return vectors
        return feature_vectors

    def run_surf_and_bow(self, data):
        self.val = data
        model= self.read_and_clusterize()
        feature_vectors = self.calculate_centroids_histogram(model)
        return feature_vectors
