# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 11:59:07 2021
@author: EmR
"""

import queue
import cv2
import numpy as np
import time
import pyautogui
<<<<<<< HEAD


queue = [] #implemented a queue 
queue.append((0,0))
frame_num = 4 #initialised frame_num to read specific frames
=======
import EyeDetection 

# Constants
MOTION_UP = "Up"
MOTION_DOWN = "Down"
MOTION_LEFT = "Left"
MOTION_RIGHT = "Right"
NO_MOTION = "_"
>>>>>>> upstream/main

def empty(a):
    pass

def create_trackbars():
    cv2.namedWindow('Trackbars')
    cv2.resizeWindow('Trackbars', 640, 240)
    cv2.createTrackbar('HueMin', 'Trackbars', 0, 179, empty)
    cv2.createTrackbar('HueMax', 'Trackbars', 179, 179, empty)
    cv2.createTrackbar('SatMin', 'Trackbars', 0, 255, empty)
    cv2.createTrackbar('SatMax', 'Trackbars', 255, 255, empty)
    cv2.createTrackbar('ValMin', 'Trackbars', 0, 255, empty)
    cv2.createTrackbar('ValMax', 'Trackbars', 255, 255, empty)

def create_mask(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue_min = cv2.getTrackbarPos('HueMin', 'Trackbars')
    hue_max = cv2.getTrackbarPos('HueMax', 'Trackbars')
    sat_min = cv2.getTrackbarPos('SatMin', 'Trackbars')
    sat_max = cv2.getTrackbarPos('SatMax', 'Trackbars')
    val_min = cv2.getTrackbarPos('ValMin', 'Trackbars')
    val_max = cv2.getTrackbarPos('ValMax', 'Trackbars')
    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    return mask

def threshold(mask):
    _,thresh = cv2.threshold(mask,127,255,cv2.THRESH_BINARY) # if pixel intensity <= 127 then set it as 0 and pixel intensity > 127 set it as 255
    return thresh

def find_contours(thresh):
    contours,heirarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #give list of all essential boundary points
    return contours
    
def max_contour(contours):
    if len(contours) == 0:
        return []
    max_cntr = max(contours,key=lambda x: cv2.contourArea(x))
    epsilon = 0.005*cv2.arcLength(max_cntr,True)  # maximum distance from contour to approximated contour. It is an accuracy parameter
    max_cntr = cv2.approxPolyDP(max_cntr,epsilon,True)
    return max_cntr

def centroid(contour):
    if len(contour) == 0: # if the array is empty return (-1,-1) 
        return (-1,-1)
    M=cv2.moments(contour) # gives a dictionary of all moment values calculated
    try:
        x = int(M['m10']/M['m00'])  # Centroid is given by the relations, 𝐶𝑥 =𝑀10/𝑀00 and 𝐶𝑦 =𝑀01/𝑀00
        y = int(M['m01']/M['m00'])
    except ZeroDivisionError:
        return (-1,-1) 
    return (x,y)

<<<<<<< HEAD
def rateChange(x,y):
    global queue
    global frame_num
    st = time.time()
    queue.append((x,y)) #appending the coordinates in queue
    time.sleep(0.09)
    rox = queue[0][0] - queue[1][0] #rate change of x
    roy = queue[0][1] - queue[1][1] # rate change of y
    et = time.time()
    elapsed = et - st
    speed_x = float(rox)/((elapsed))
    speed_y = float(roy)/((elapsed))
    if(speed_x >150 and speed_x <600):
        pyautogui.press("right")
        frame_num = 25
    elif(speed_x<-150 and speed_x>-600):
        pyautogui.press("left")
        frame_num = 25
        
    elif(speed_y<-150 and speed_y>-400):
        pyautogui.scroll(-300) 
        frame_num = 25
    elif (speed_y>150 and speed_y <400):
        pyautogui.scroll(300) 
        frame_num = 25
    queue.pop(0)
    
=======
def clean_image(mask):
    img_eroded = cv2.erode(threshImg,(3,3), iterations=1)  
    img_dilated = cv2.dilate(img_eroded,(3,3),iterations = 1)
    return img_dilated

def detect_hand(mask):
    return np.average(mask) > 50
    
def velocity(x1,x2,t):
    return (x2 - x1)/t

def detect_motion(x1,y1,x2,y2,t):
    vel_x = velocity(x1,x2,t)
    vel_y = velocity(y1,y2,t)

    if vel_x > 500:
        return MOTION_RIGHT
    elif vel_x < -500:
        return MOTION_LEFT
    elif vel_y > 200:
        return MOTION_DOWN
    elif vel_y < -200:
        return MOTION_UP
    else:
        return NO_MOTION

# performing actions based on hand motion
def performAction(hand_motion):
    if hand_motion == MOTION_RIGHT:
        pyautogui.press('right')
    elif hand_motion == MOTION_LEFT:
        pyautogui.press('left')
    elif hand_motion == MOTION_UP:
        pyautogui.press('up')
    elif hand_motion == MOTION_DOWN:
        pyautogui.press('down')


#################################################################################
########## Driver Code ##########################################################
#################################################################################
>>>>>>> upstream/main

vid = cv2.VideoCapture(0);
create_trackbars()
frame_num = 4 # Counter for frame number
prev_x, prev_y, cur_x, cur_y = -1,-1,-1,-1 # Initializing the previous and current co-ordinates of the hand centroid
last_timestamp = 0 # Initializing the last recording timestamp

while(1):
    _,frame = vid.read()
    frame = cv2.flip(frame,1) # resolving mirror image issues
    # For eye detection
    fullScreenFrame=frame
    frame = frame[:300, 300:] # only considering frame from row 0-300 and col from 300-end so that main focus is on our hands
    frame = cv2.GaussianBlur(frame,(5,5),0) # to remove noise from frame

    mask = create_mask(frame)
    threshImg = threshold(mask)
<<<<<<< HEAD
    img_erosion = cv2.erode(threshImg,(3,3), iterations=1)  
    dilata = cv2.dilate(img_erosion,(3,3),iterations = 1) #image cleaning using dilation and erosion
    contours = find_contours(dilata)
=======
    cleaned_mask = clean_image(threshImg)
    contours = find_contours(cleaned_mask)
>>>>>>> upstream/main
    frame = cv2.drawContours(frame,contours,-1,(255,0,0),2) # drawing all contours 
    max_cntr = max_contour(contours)  # finding maximum contour of the thresholded area
    (centroid_x,centroid_y) = centroid(max_cntr) # finding centroid of the maximum contour
    if(centroid_x,centroid_y) != (-1,-1):
<<<<<<< HEAD
        frame = cv2.circle(frame , (centroid_x,centroid_y) , 5 , (255,255,0) , -1) # drawing a circle on the identified centre of mass
        if frame_num ==0:#to read specific frames
            rateChange(centroid_x,centroid_y)
            frame_num = 4
        else:
            frame_num -= 1
=======
        frame = cv2.circle(frame , (centroid_x,centroid_y) , 5 , (255,255,0) , -1) # drawing a circle on the identified centroid
        hand_detected = cv2.contourArea(max_cntr) >= 3000 # Max contour area must be greater than thois threshold 
        if hand_detected:
            if prev_x == -1:
                prev_x, prev_y = centroid_x, centroid_y
                frame_num = 10
            
            if frame_num == 0:
                cur_time = time.time()
                time_elapsed = cur_time - last_timestamp
                hand_motion = detect_motion(prev_x, prev_y, centroid_x, centroid_y, time_elapsed)
                print(hand_motion)
                performAction(hand_motion)
                prev_x, prev_y = centroid_x, centroid_y
                last_timestamp = time.time()

                # Re-initializing the frame counter
                if hand_motion != NO_MOTION:
                    frame_num = 4
                else:
                    frame_num = 10
            else:
                frame_num -= 1
        else:
            prev_x, prev_y = -1, -1
            frame_num = 4
>>>>>>> upstream/main
    
    cv2.imshow('video',frame)
    cv2.imshow("mask",mask)
    key = cv2.waitKey(10)
    
    if key == ord('q'):
        break
    
vid.release()

<<<<<<< HEAD
cv2.destroyAllWindows()    
=======
cv2.destroyAllWindows()
>>>>>>> upstream/main
