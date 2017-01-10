# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 20:50:00 2016

@author: vishwa
"""

def func_img_transform(src_img,homography,dest_img,start_point,end_point):
    tmp_image=dest_img
    for i in range(start_point[0],end_point[0]):
        for j in range (start_point[1],end_point[1]):
            tmp_xy=[i,j,1]
            trans_val=np.dot(homography,tmp_xy)
            tmp_image[trans_val[0]][trans_val[1]]=src_img[i][j]
            
return tmp_image