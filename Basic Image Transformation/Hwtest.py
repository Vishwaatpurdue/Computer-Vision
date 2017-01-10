# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 15:54:58 2016

@author: vishwa
"""

import cv2
import numpy as np
path = "/home/vishwa/661/PicsHw2"

image_1 = cv2.imread(path+"/1.jpg")
image_2 = cv2.imread(path+"/2.jpg")
image_3 = cv2.imread(path+"/3.jpg")
image_4 = cv2.imread(path+"/Seinfeld.jpg")

# Homogeneous points obtained from gimp
Points_1a=array([[421,2108,1],[531,3303,1],[1495,2148,1],[1357,3312,1]])
Points_1b=array([[795,1590,1],[768,2983,1],[1597,1616,1],[1518,2987,1]])
Points_1c=array([[562,999,1],[421,2425,1],[1412,1026,1],[1478,2406,1]])
Points_1d=array([[0,0,1],[0,2560,1],[1536,0,1],[1536,2560,1]])

# Finding Homography A of Ax=b
def Homography(points_src,points_dest):
    Mat_A=np.zeros((8,8))
    b = np.zeros((1,8))
    if points_src.shape[0] != points_dest.shape[0] or points_src.shape[1] != points_dest.shape[1]:
        print "No. of Source and destination points donot match"
        exit(1)
    for i in range(0,len(points_src)):
        Mat_A[i*2]=[points_src[i][0],points_src[i][1],points_src[i][2],0,0,0,(-1*points_src[i][0]*points_dest[i][0]),(-1*points_src[i][1]*points_dest[i][0])]
        Mat_A[i*2+1]=[0,0,0,points_src[i][0],points_src[i][1],points_src[i][2],(-1*points_src[i][0]*points_dest[i][1]),(-1*points_src[i][1]*points_dest[i][1])]
        b[0][i*2] = points_dest[i][0]
        b[0][i*2+1] = points_dest[i][1]        
    # A, b matrix formed
      
    # if no. of points is not 4 then using the below code
    tmp_H=np.dot(np.linalg.pinv(Mat_A),b.T)
    homography= np.zeros((3,3))
    homography[0]= tmp_H[0:3,0]
    homography[1]= tmp_H[3:6,0]
    homography[2][0:2]= tmp_H[6:8,0]
    homography[2][2]= 1
    return homography
# Function for finding Homography ends here
    
tmp_image=image_2
for i in range(0,image_4.shape[0]-1):
    for j in range (0,image_4.shape[1]-1):
        tmp_xy=[i,j,1]
        trans_val=np.dot(Homography(Points_1d,Points_1b),tmp_xy)
        tmp_image[trans_val[0]][trans_val[1]]=image_4[i][j]
        
# Write the output in a new file
#cv2.namedWindow('test',cv2.WINDOW_NORMAL)
#cv2.imshow('test',tmp_image)  

# Write the output in a new file
cv2.imwrite('test_1b.jpg',tmp_image)

# Find the Homography between Seinfeld image and 1a

tmp_image=image_1
for i in range(0,image_4.shape[0]-1):
    for j in range (0,image_4.shape[1]-1):
        tmp_xy=[i,j,1]
        trans_val=np.dot(Homography(Points_1d,Points_1a),tmp_xy)
        tmp_image[trans_val[0]][trans_val[1]]=image_4[i][j]
# Write the output in a new file
cv2.imwrite('test_2da.jpg',tmp_image)
"""
# Find the Homography between Seinfeld image and 1b
homo_trans_1da=np.dot(np.linalg.pinv(Points_1d),Points_1c)
homography_1da=homo_trans_1da.transpose()

tmp_image=image_3
for i in range(0,image_4.shape[0]-1):
    for j in range (0,image_4.shape[1]-1):
        tmp_xy=[i,j,1]
        trans_val=np.dot(homography_1da,tmp_xy)
        tmp_image[trans_val[0]][trans_val[1]]=image_4[i][j]
# Write the output in a new file
cv2.imwrite('test_1dc.jpg',tmp_image)
"""
