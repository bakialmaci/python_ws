from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import this
import imutils
import time
import picamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Global variables
P_K = 0.08
I_K = 0
D_K = 0.5
HIZ_MAX = 23
HIZ = 20

error_lst = 0
sol_ileri = 27
sol_geri = 17
sol_en = 22
sag_ileri  = 24
sag_geri = 23
sag_en = 25

p = 0
i = 0
d = 0
t = 0

GPIO.setup(sol_ileri, GPIO.OUT)
GPIO.setup(sol_geri, GPIO.OUT)
GPIO.setup(sol_en, GPIO.OUT)
GPIO.setup(sag_geri, GPIO.OUT)
GPIO.setup(sag_ileri, GPIO.OUT)
GPIO.setup(sag_en, GPIO.OUT)

solen = GPIO.PWM(sol_en, 255)
sagen = GPIO.PWM(sag_en, 255)

def search():
   solpwm1 = -t + HIZ
   if solpwm1 > HIZ_MAX:
       solpwm1 = HIZ_MAX
   elif solpwm1 < 0:
       solpwm1 = 0
   if solpwm1 >= 0:
       solen.start(solpwm1)
       GPIO.output(sol_ileri, GPIO.HIGH)
       GPIO.output(sol_geri, GPIO.LOW)
   elif solpwm1 < 0:
       GPIO.output(sol_ileri, GPIO.LOW)
       GPIO.output(sol_geri, GPIO.HIGH)
       solen.start(-solpwm1)
   sagpwm1 = t + HIZ
   if sagpwm1 > HIZ_MAX:
       sagpwm1 = HIZ_MAX
   elif sagpwm1 < 0:
       sagpwm1 = 0
   if sagpwm1 >= 0:
       sagen.start(sagpwm1)
       GPIO.output(sag_ileri, GPIO.HIGH)
       GPIO.output(sag_geri, GPIO.LOW)
   elif sagpwm1 < 0:
       sagen.start(-sagpwm1)
       GPIO.output(sag_ileri, GPIO.LOW)
       GPIO.output(sag_geri, GPIO.HIGH)

def stop():
   GPIO.output(sag_ileri, GPIO.LOW)
   GPIO.output(sag_geri, GPIO.LOW)
   GPIO.output(sol_ileri, GPIO.LOW)
   GPIO.output(sol_geri, GPIO.LOW)
   sagen.start(0)
   solen.start(0)

def pid_kontrol(error,en2=0):
   global t
   global HIZ
   global error_lst
   global i
   global en
   global HIZ_MAX
   if HIZ_MAX > HIZ:
       HIZ = HIZ+1

   error_dif = error - error_lst
   error_lst = error

   p = P_K * error
   i = i + (I_K * error_dif)
   d = D_K * error_dif
   t = p + d
   t = t

   # sol motor
   sagpwm1 = t + HIZ
   solpwm1 = HIZ - t
   if(en2==1):
       if sagpwm1 > HIZ_MAX:
           sagpwm1 = HIZ_MAX
       elif sagpwm1 < 0:
           sagpwm1 = 0
       if sagpwm1 >= 0:
           sagen.start(sagpwm1)
           GPIO.output(sag_ileri, GPIO.HIGH)
           GPIO.output(sag_geri, GPIO.LOW)
       elif sagpwm1 < 0:
           sagen.start(-sagpwm1)
           GPIO.output(sag_ileri, GPIO.LOW)
           GPIO.output(sag_geri, GPIO.HIGH)
   # sag motor
       if solpwm1 > HIZ_MAX:
           solpwm1 = HIZ_MAX
       elif solpwm1 < 0:
           solpwm1 = 0
       if solpwm1 >= 0:
           solen.start(solpwm1)
           GPIO.output(sol_ileri, GPIO.HIGH)
           GPIO.output(sol_geri, GPIO.LOW)
       elif solpwm1 < 0:
           GPIO.output(sol_ileri, GPIO.LOW)
           GPIO.output(sol_geri, GPIO.HIGH)
           solen.start(-solpwm1)
   else:
       GPIO.output(sol_ileri, GPIO.LOW)
       GPIO.output(sol_geri, GPIO.LOW)
       GPIO.output(sag_ileri, GPIO.LOW)
       GPIO.output(sag_geri, GPIO.LOW)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=120,
       help="of frames to loop over for FPS test")
ap.add_argument("-v", "--video",
 help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
 help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

green_l = (31,70,20)
green_u = (72,255,255)

pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
 vs = VideoStream(src=0).start()

# otherwise, grab a reference to the video file
else:
 vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(0.2)

# keep looping
while True:
 # grab the current frame
 frame = vs.read()

 # handle the frame from VideoCapture or VideoStream
 frame = frame[1] if args.get("video", False) else frame

 # if we are viewing a video and we did not grab a frame,
 # then we have reached the end of the video
 if frame is None:
   break

 # resize the frame, blur it, and convert it to the HSV
 # color space
 frame = imutils.resize(frame, width=320, height=240)
 blurred = cv2.GaussianBlur(frame, (11, 11), 0)
 hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

 # construct a mask for the color "green", then perform
 # a series of dilations and erosions to remove any small
 # blobs left in the mask
 mask = cv2.inRange(hsv, green_l,green_u)
 mask = cv2.erode(mask, None, iterations=2)
 mask = cv2.dilate(mask, None, iterations=2)
 # find contours in the mask and initialize the current
 # (x, y) center of the ball
 cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
   cv2.CHAIN_APPROX_SIMPLE)
 cnts = imutils.grab_contours(cnts)
 center = None
 # only proceed if at least one contour was found
 if len(cnts) > 0:
   # find the largest contour in the mask, then use
   # it to compute the minimum enclosing circle and
   # centroid
   c = max(cnts, key=cv2.contourArea)
   ((x, y), radius) = cv2.minEnclosingCircle(c)
   M = cv2.moments(c)
   center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
   print("Radius",radius)
   # only proceed if the radius meets a minimum size
   if radius > 0.01:
     # draw the circle and centroid on the frame,
     # then update the list of tracked points
     print("X AXIS:",x,"Y AXIS:",y-45)
     x_middle_point = 160
     y_middle_point = 120


     cv2.circle(frame, (int(x), int(y)), int(radius),
       (0, 255, 255), 2)
     cv2.circle(frame, center, 5, (0, 0, 255), -1)
     if(radius<=40 and y < 190):
                           pid_kontrol(x_middle_point - x,1)
     else:
         pid_kontrol(x_middle_point -x,0)
         stop()

 # update the points queue
 pts.appendleft(center)
 # loop over the set of tracked points

 #show the frame to our screen
 # cv2.imshow("Frame", img)
 # key = cv2.waitKey(1) & 0xFF
 #
 # if the 'q' key is pressed, stop the loop
 # if key == ord("q"):
 # 	break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
 vs.stop()

# otherwise, release the camera
else:
 vs.release()

# close all windows
cv2.destroyAllWindows()
