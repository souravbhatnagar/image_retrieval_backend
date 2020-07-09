#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 19:52:33 2020

@author: sourav
"""


import numpy as np
import cv2 as cv

class HarrisCorner():
    def harris_corner(self, image):
        _img = cv.imread(image)
        gray = cv.cvtColor(_img, cv.COLOR_BGR2GRAY)
        gray = np.float32(gray)
        features = cv.cornerHarris(gray, 2, 3, 0.04)
        features = cv.dilate(features,None)
        ret, features = cv.threshold(features,0.01*features.max(),255,0)
        features = np.uint8(features)
        return features
