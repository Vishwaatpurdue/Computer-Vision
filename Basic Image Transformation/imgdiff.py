# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 22:58:39 2016

@author: vishwa
"""

import cv2
import numpy as np

img1=cv2.imread('final_image1.jpg') 
img2=cv2.imread('test_image1_bil.jpg') 
diff= img1-img2
cv2.imwrite('difference_wavg_non.jpg',diff)