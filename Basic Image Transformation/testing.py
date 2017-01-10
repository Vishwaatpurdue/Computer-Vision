# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 21:20:49 2016

@author: vishwa
"""

import cv2
import numpy as np
path = "/home/vishwa/661/PicsHw2"

image_1 = cv2.imread(path+"/1.jpg")
cv2.namedWindow('test',cv2.WINDOW_NORMAL)
cv2.imshow('test',image_1)