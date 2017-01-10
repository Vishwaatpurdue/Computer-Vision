# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 01:30:04 2016

@author: vishwa
"""

# -*- coding: utf-8 -*-
"""
@author: vishwa
"""

import cv2
import numpy as np
import math
#from Hw_VJ import Homography as Hm
#from Hw_VJ import image_mapping as Im
path = "/home/vishwa/661/PicsHw2"

# Function for finding Homography starts here
def Homography(points_src,points_dest):
    Mat_A=np.zeros((points_src.shape[0]*2,8),dtype='float')
    b = np.zeros((1,points_src.shape[0]*2),dtype='float')
    if points_src.shape[0] != points_dest.shape[0] or points_src.shape[1] != points_dest.shape[1]:
        print "No. of Source and destination points donot match"
        exit(1)
    for i in range(0,len(points_src)):
        Mat_A[i*2]=[points_src[i][0],points_src[i][1],points_src[i][2],0,0,0,(-1*points_src[i][0]*points_dest[i][0]),(-1*points_src[i][1]*points_dest[i][0])]
        Mat_A[i*2+1]=[0,0,0,points_src[i][0],points_src[i][1],points_src[i][2],(-1*points_src[i][0]*points_dest[i][1]),(-1*points_src[i][1]*points_dest[i][1])]
        b[0][i*2] = points_dest[i][0]
        b[0][i*2+1] = points_dest[i][1]        
    # A, b matrix formed
      
    # If no. of points is not 4 then using the below code
    tmp_H=np.dot(np.linalg.pinv(Mat_A),b.T)
    homography= np.zeros((3,3))
    homography[0]= tmp_H[0:3,0]
    homography[1]= tmp_H[3:6,0]
    homography[2][0:2]= tmp_H[6:8,0]
    homography[2][2]= 1
    return homography
# Function for finding Homography ends here
# Getting RGB data function using weighted average starts here
def getdata(point, img):
    tp_left =img[(math.floor(point[0])%img.shape[0]),(math.floor(point[1])%img.shape[1])]
    tp_right =img[math.floor(point[0])%img.shape[0],math.floor(point[1]+1)%img.shape[1]]
    bt_left =img[math.floor(point[0]+1)%img.shape[0],math.floor(point[1])%img.shape[1]]
    bt_right =img[math.floor(point[0]+1)%img.shape[0],math.floor(point[1]+1)%img.shape[1]]
    diff_x = point[0] - math.floor(point[0])
    diff_y = point[1] - math.floor(point[1])
    tp_left_weight= pow(pow(diff_x,2)+pow(diff_y,2),-0.5)
    tp_right_weight = pow(pow(diff_x,2)+pow(1-diff_y,2),-0.5)
    bt_left_weight = pow(pow(1-diff_x,2)+pow(diff_y,2),-0.5)
    bt_right_weight = pow(pow(1-diff_x,2)+pow(1-diff_y,2),-0.5)
    resultant_pt = (tp_left*tp_left_weight+tp_right*tp_right_weight+bt_left*bt_left_weight+bt_right*bt_right_weight)/(tp_left_weight+tp_right_weight+bt_left_weight+bt_right_weight)
    return resultant_pt
# getting RGB data function using weighted average ends here
    
# Image mapping code starts here
def image_mapping(src_image,dest_image,points_src,Homography):
    tmp_srcimage=np.zeros((src_image.shape[0],src_image.shape[1],3),dtype='uint8')
    for i in range(0,src_image.shape[0]-1):
        for j in range(0,src_image.shape[1]-1):
                point_tmp = np.array([i, j, 1])
                trans_coord = np.array(np.dot(Homography,point_tmp))
                trans_coord = trans_coord/trans_coord[2]
                if (trans_coord[0]>0) and (trans_coord[0]<dest_image.shape[0]) and (trans_coord[1]>0) and (trans_coord[1]<dest_image.shape[1]):
                    tmp_srcimage[i][j]=getdata(trans_coord,dest_image)
    return tmp_srcimage
# Image mapping code ends here.

image_1 = cv2.imread(path+"/Left.jpg")
image_2 = cv2.imread(path+"/Middle.jpg")
image_3 = cv2.imread(path+"/Right.jpg")
image_4 = cv2.imread(path+"/My.jpg")

# Homogeneous points obtained from gimp
Points_1a=np.array([[1102,1192,1],[1136,1978,1],[2301,1238,1],[2157,1972,1],[1011,2300,1],[1026,2575,1],[1493,2298,1],[1482,2572,1],[1541,3089,1],[1523,3283,1],[1933,3087,1],[1897,3287,1]])
Points_1b=np.array([[1091,860,1],[1102,1669,1],[2176,839,1],[2199,1663,1],[947,2098,1],[950,2528,1],[1506,2096,1],[1512,2520,1],[1653,3533,1],[1652,4000,1],[2226,3536,1],[2232,3994,1]])
Points_1c=np.array([[1057,1094,1],[1053,1421,1],[1845,1051,1],[1924,1413,1],[915,1616,1],[904,1838,1],[1384,1612,1],[1403,1836,1],[1570,2445,1],[1599,2781,1],[2140,2442,1],[2211,2776,1]])


H1=Homography(Points_1b,Points_1a)
H2=Homography(Points_1c,Points_1b)

Final_Homography=np.dot(H1,H2)
points_for_trans=np.array([[0,0],[image_3.shape[0],0],[0,image_3.shape[1]],[image_3.shape[0],image_3.shape[1]]])
final_output= image_mapping(image_3,image_1,points_for_trans,Final_Homography)
cv2.imwrite('Left_transform_Right.jpg',final_output)
