from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO
from robotFunctions import *



camera = PiCamera()
camera.resolution = (320, 180)
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(320, 180))
time.sleep(0.1)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	Blackline = cv2.inRange(image, (0,0,100), (80,80,255))
	kernel = np.ones((3,3), np.uint8)
	Blackline = cv2.erode(Blackline, kernel, iterations=5)
	Blackline = cv2.dilate(Blackline, kernel, iterations=9)
	img_blk,contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	if len(contours_blk) > 0:
		blackbox = cv2.minAreaRect(contours_blk[0])
		(x_min, y_min), (w_min, h_min), ang = blackbox
		if ang < -45 :
			ang = 90 + ang
		if w_min < h_min and ang > 0:
			ang = (90-ang)*-1
		if w_min > h_min and ang < 0:
			ang = 90 + ang
		setpoint = 320
		error = int(x_min - setpoint)
		ang = int(ang)
		error = error + 160
		if error > 0 and error < 100:
			L,R = [0.8,0.2]
		elif error > 100:
			L,R = [1,-0.3]
		elif error < 0 and error > -100:
			L,R = [0.2,0.8]
		else:
			L,R = [-0.3,1]
		L,R = [L,R]
		robot.forward(L,R)
		print(ang,error,L,R)
	#box = cv2.boxPoints(blackbox)
	#box = np.int0(box)
	#cv2.drawContours(image,[box],0,(0,0,255),3)
	#cv2.putText(image,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
	#cv2.putText(image,str(error),(10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
	#cv2.line(image, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)


	#cv2.imshow("orginal with line", image)
	rawCapture.truncate(0)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
