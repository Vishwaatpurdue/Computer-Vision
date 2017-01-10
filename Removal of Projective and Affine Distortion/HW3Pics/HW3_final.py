# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 23:50:40 2016

@author: Rohan Sarkar
"""

import cv2
import numpy as np
import math


# Finding homography to remove perspective distortion
# Function to find homography using 2 pair of parallel lines
def Find_Physical_Point(Point):
    return (Point/Point[2])
def Normalise_line(Line):
    return (Line/Line[2])
def Homography_Projective(points):
	""" As per notes Finding the cross product of the two points to find the line connecting the points
	Line1 is formed by the cross product of P,Q. Line1 is formed by the cross product of P,Q. Line3 is formed by P,R and Line4 is formed by Q,S """
	Line1= Normalise_line(np.cross(points[2,:],points[3,:]))
 	Line2= Normalise_line(np.cross(points[0,:],points[1,:]))
	Line3= Normalise_line(np.cross(points[2,:],points[0,:]))
	Line4= Normalise_line(np.cross(points[3,:],points[1,:]))
	"""Finding the two ideal points by the cross product of the lines obtained A = cross product Line1 and Line2. while B= crossproduct of Line3 and Line4."""
	Vanishing_point_1= Find_Physical_Point(np.cross(Line3,Line4))
	Vanishing_point_2= Find_Physical_Point(np.cross(Line1,Line2))
	""" Finding the line at infinity. Normalizing the line at infinity"""
	vanishing_line= Normalise_line(np.cross(Vanishing_point_1,Vanishing_point_2))
	# Generating homography matrix
	H = np.matrix([[1.0,0,0],[0,1.0,0],[vanishing_line[0],vanishing_line[1],vanishing_line[2]]])
	print H
	return H
 
# Function to find homography using 2 pair of parallel lines ends here

# Finding the dimensions and offset for the new image in world plane
 
def Find_Boundary_Offset_Dimension(Homography,image):
	bp_image=np.array([[0,0,1],[0,image.shape[1],1],[image.shape[0],0,1],[image.shape[0],image.shape[1],1]])
	bp_world=np.zeros((bp_image.shape[1],bp_image.shape[0]))
	bp_world=np.array((np.dot(Homography,bp_image.T)).T)
	for i in range(0,bp_image.shape[0]):
	  bp_world[i]=bp_world[i]/bp_world[i,2]
        bp_world=bp_world.T
	offset_x=int(min(bp_world[0]))
	offset_y=int(min(bp_world[1]))
	height=int(max(bp_world[0])-min(bp_world[0]))
	width=int(max(bp_world[1])-min(bp_world[1]))
	return offset_x,offset_y,height,width
# Finding dimension and offset function ends here

# Getting RGB data function using weighted average starts here
def Weighted_Interpolation(point, image):
    P_lu =image[math.floor(point[0,0]),math.floor(point[0,1])]
    P_uu =image[math.floor(point[0,0]),math.ceil(point[0,1])]
    P_ll =image[math.ceil(point[0,0]),math.floor(point[0,1])]
    P_ul =image[math.ceil(point[0,0]),math.ceil(point[0,1])]
    D_x = point[0,0] - math.floor(point[0,0])
    D_y = point[0,1] - math.floor(point[0,1])
    W_lu= pow(pow(D_x,2)+pow(D_y,2),-0.5)
    W_uu = pow(pow(D_x,2)+pow(1-D_y,2),-0.5)
    W_ll = pow(pow(1-D_x,2)+pow(D_y,2),-0.5)
    W_ul = pow(pow(1-D_x,2)+pow(1-D_y,2),-0.5)
    WI_data = (P_lu*W_lu+P_uu*W_uu+P_ll*W_ll+P_ul*W_ul)/(W_lu+W_uu+W_ll+W_ul)
    return WI_data
# getting RGB data function using weighted average ends here
    
# Image mapping code starts here
def image_mapping(image,Homography,offset_x,offset_y,height,width):
    output_image=np.zeros((height,width,3),dtype='uint8')
    Homography_inv=np.linalg.inv(Homography)
    #cv2.imwrite('test_src.jpg',output_image)
    for rows in range(0,height):
        for cols in range(0,width):
            point_image = np.array([(rows+offset_x), (cols+offset_y), 1])
            point_world = np.array(np.dot(Homography_inv,point_image))
            point_world = point_world/point_world[0,2]
            if (point_world[0,0]>0) and (point_world[0,0]<image.shape[0]-1) and (point_world[0,1]>0) and (point_world[0,1]<image.shape[1]-1):
                    output_image[rows][cols]=Weighted_Interpolation(point_world,image)
    return output_image
# Image mapping code ends here. 
 
# Input images
image_1 = cv2.imread("flatiron.jpg")
#image_2 = cv2.imread(path+"/monalisa.jpg")
#image_3 = cv2.imread(path+"/wideangle.jpg")

# Points obtained from gimp converted into homogeneous coordinates
# Frame Coordinates for Flatiron.jpg
Points_1=np.array([[273,96,1],[153,552,1],[493,28,1],[412,581,1]],dtype='float')

H_persp = Homography_Projective(Points_1)
[Off_X,Off_Y,Dim_X,Dim_Y]= Find_Boundary_Offset_Dimension(H_persp,image_1)
print Off_X,'\n',Off_Y,'\n',Dim_X,'\n',Dim_Y
output_persp=image_mapping(image_1,H_persp,Off_X,Off_Y,Dim_X,Dim_Y)
cv2.imwrite('Output1.jpg',output_persp)
input_aff_1=output_persp
#####################################################
""" Removing Affine Distortion"""
# Finding Lines
def Lines(point1,point2):
	Line=np.cross(point1,point2)
	#Line_n=Line/Line[2]
	return Line
# Finding Homography of Affine
def Homography_Affine(points):
	# Finding two orthogonal lines from 3 points
	Line1=Lines(points[1,:],points[0,:])
	M1=Lines(points[1,:],points[2,:])
	Line2=Lines(points[4,:],points[3,:])
	M2=Lines(points[4,:],points[5,:])
	# Finding S matrix which is ATA
	Mat_A=np.zeros((2,2),dtype='float')
	b=np.array([0,0])
	Mat_A[0]=np.array([Line1[0]*M1[0],M1[0]*Line1[1]+M1[1]*Line1[0]])
	Mat_A[1]=np.array([Line2[0]*M2[0],M2[0]*Line2[1]+M2[1]*Line2[0]])
	b=np.array([-M1[1]*Line1[1],-M2[1]*Line2[1]])
	[s11, s12]= (np.linalg.pinv(Mat_A).dot(b))
	print s11,s12
	S=np.zeros((2,2),dtype='float')
	# Generating S matrix
	S[0]=np.array([s11,s12])
	S[1]=np.array([s12,1])
	# Find SVD decomposition of S to find A
	V,D_S,Vt=np.linalg.svd(S,full_matrices=1)
	D_A=np.sqrt(D_S)
	# Reconstructing D_A matrix from the S
	D = np.zeros((2,2),dtype='float')
	D[0]= np.array([D_A[0],0])
	D[1]= np.array([0,D_A[1]])
	A=V.dot(D).dot(Vt)
	# Finally the homography is 
	H=np.matrix([[A[0,0],A[0,1],0],[A[1,0],A[1,1],0],[0,0,1]])
	return H
# Points to find pair of line that will be orthogonal in undistorted image
points_affine=np.array([[74,264,1],[164,58,1],[246,15,1],[114,243,1],[95,253,1],[46,185,1]])
H_Affine=Homography_Affine(points_affine)
print H_Affine
H_Affine_inv=np.linalg.inv(H_Affine)
[Off_XA,Off_YA,Dim_XA,Dim_YA] = Find_Boundary_Offset_Dimension(H_Affine_inv,input_aff_1)
print Off_XA,'\n',Off_YA,'\n',Dim_XA,'\n',Dim_YA
output_affine=image_mapping(input_aff_1,H_Affine_inv,Off_XA,Off_YA,Dim_XA,Dim_YA)
cv2.imwrite('output2.jpg',output_affine)
