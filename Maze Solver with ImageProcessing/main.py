# çizgileri kalınlaştırmam lazım. bu sayede kalın ve tam bir kare oluşturmuş olacağım.

import cv2
import numpy as np
import math
contour_list = []
count = 0

img = cv2.imread("realmaze.jpg")
dst = cv2.fastNlMeansDenoisingColored(img,None,3,150,10,21)
gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,130,200,3)
edges = cv2.Canny(thresh, 150, 200)
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

def square_control(x1,y1,x2,y2,x3,y3,x4,y4):
    if -150 < (x1 - x3) - (y1 - y3) < 150:
        return 1
    else:
        return 0

for contour in contours:
    approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    area = cv2.contourArea(contour)
    if ((len(approx) > 3) and (len(approx) < 5) and area >= 100  and square_control(approx[0][0][0],approx[0][0][1],approx[1][0][0],approx[1][0][1],approx[2][0][0],approx[2][0][1],approx[3][0][0],approx[3][0][1]) == 1):
        count += 1
        if count == 2:
            contour_list.append(contour)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(edges,'SQUARE',(approx[0][0][0],approx[0][0][1]-10), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            count = 0

def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(edges,(x,y),5,(0,0,255),-1)
        mouseX,mouseY = x,y
        print(int(math.sqrt(((target()[0]-mouseX)**2)+((target()[1]-mouseY)**2))),"| Current::",mouseX,mouseY,"| Target::",target()[0],target()[1])

def target():
    x = 0
    y = 0
    len_contour = len(contour_list[0])
    for i in range(len_contour):
        x += contour_list[0][i][0][0]
        y += contour_list[0][i][0][1]
    return int(x/len_contour),int(y/len_contour)

# print(target())
edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
cv2.drawContours(edges, contour_list,  -1, (0, 255, 0), 2)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
while(1):
    cv2.imshow('image',edges)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
