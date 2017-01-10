# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 23:21:22 2016

@author: vishwa
"""

import cv2
import numpy as np
import math
path = "/home/vishwa/661/PicsHw2"

image_1 = cv2.imread(path+"/1.jpg")
image_2 = cv2.imread(path+"/2.jpg")
image_3 = cv2.imread(path+"/3.jpg")
image_4 = cv2.imread(path+"/Seinfeld.jpg")

# Homogeneous points obtained from gimp
Points_1a=np.array([[421,2108,1],[531,3303,1],[1495,2148,1],[1357,3312,1]])
Points_1b=np.array([[795,1590,1],[768,2983,1],[1597,1616,1],[1518,2987,1]])
Points_1c=np.array([[562,999,1],[421,2425,1],[1412,1026,1],[1478,2406,1]])
Points_1d=np.array([[0,0,1],[0,2560,1],[1536,0,1],[1536,2560,1]])

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

# get the color of a pixel in photo from 'real painting'
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
# getcolor function end

# image mapping code starts here
def image_mapping(src_image,dest_image,points_src,Homography):
    tmp_srcimage=np.zeros((src_image.shape[0],src_image.shape[1],3),dtype='uint8')
    pts = np.array([[points_src[0][1],points_src[0][0]],[points_src[1][1],points_src[1][0]],[points_src[3][1],points_src[3][0]],[points_src[2][1],points_src[2][0]]])
    cv2.fillPoly(tmp_srcimage,[pts],(255,255,255))
    src_image2 = src_image
    for i in range(0,(src_image.shape[0]-1)):
        for j in range(0,(src_image.shape[1]-1)):
            if tmp_srcimage[i,j,1]==255 and tmp_srcimage[i,j,0]==255 and tmp_srcimage[i,j,2]==255:
                point_tmp = np.array([i, j, 1])
                trans_coord = np.array(np.dot(Homography,point_tmp))
                trans_coord = trans_coord/trans_coord[2]            
                src_image[i][j]=getdata(trans_coord,dest_image)
                
            else:
                continue
    cv2.imwrite('testnobilinear.jpg',src_image2)
    return src_image
# image mapping code ends here.
  
# Transforming the image in 1d to 1a
H=Homography(Points_1a,Points_1d)
output=image_mapping(image_1,image_4,Points_1a,H)
cv2.imwrite('test_image1_bil.jpg',output)

# Transforming the image in 1d to 1b
H=Homography(Points_1b,Points_1d)
output=image_mapping(image_2,image_4,Points_1b,H)
cv2.imwrite('test_image2_bil.jpg',output)

# Transforming the image in 1d to 1c
H=Homography(Points_1c,Points_1d)
output=image_mapping(image_3,image_4,Points_1c,H)
cv2.imwrite('test_image3_bil.jpg',output)
