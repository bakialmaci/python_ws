import cv2
import numpy as np
import math

raw_image = cv2.imread('shapes.jpg')
raw_image = raw_image[50:480, 0:1000]
bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
# cv2.imshow('Edge', edge_detected_image)
# cv2.waitKey(0)
cv2.imwrite('edge.jpg',edge_detected_image)

# edges = cv2.imread('edge.jpg')
# gray = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
# gray = np.float32(gray)
# dst = cv2.cornerHarris(gray,10,3,0.04)
# ret, dst = cv2.threshold(dst,0.1*dst.max(),255,0)
# dst = np.uint8(dst)
# ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
# corners = cv2.cornerSubPix(gray,np.float32(centroids),(10,5),(-1,-1),criteria)
# for i in range(1, len(corners)):
#     print(corners[i])
# print(len(corners))
# edges[dst>0.01*dst.max()]=[0,0,255]
# cv2.imshow('image', edges)
# cv2.waitKey(0)


def square_control(x1,y1,x2,y2,x3,y3,x4,y4):
    return 1 if (-10 < (x1 - x3) - (y1 - y3) < 10) else 0


def rect_control(x1,y1,x2,y2,x3,y3,x4,y4):
    if abs(math.sqrt((x1-x2)**2 + (y1-y2)**2) - math.sqrt((x1-x4)**2+(y1-y4)**2)) > 10:
        if abs(x1 - x2) <= 10 and abs(x3 - x4) <= 10:
            return 1
        else:
            return 2
    else:
        return 0

def circle_control(minx,miny,maxx,maxy):
    if abs(abs(minx-maxx) - abs(miny-maxy)) <= 5:
        return 1
    else:
        return 0


_, contours, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contour_list = []
count = 0
for contour in contours:
    approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    area = cv2.contourArea(contour)
    if ((len(approx) > 3) & (len(approx) < 5) & (area > 30)  and square_control(approx[0][0][0],approx[0][0][1],approx[1][0][0],approx[1][0][1],approx[2][0][0],approx[2][0][1],approx[3][0][0],approx[3][0][1]) == 1):
        count += 1
        if count == 2:
            contour_list.append(contour)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(raw_image,'SQUARE',(approx[0][0][0],approx[0][0][1]-10), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            print("SQUARE")
            # print(approx)
            count = 0

    elif ((len(approx) > 3) & (len(approx) < 5) & (area > 30)  and rect_control(approx[0][0][0],approx[0][0][1],approx[1][0][0],approx[1][0][1],approx[2][0][0],approx[2][0][1],approx[3][0][0],approx[3][0][1]) == 1):
        count += 1
        if count == 2:
            contour_list.append(contour)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(raw_image,'RECTANGLE',(approx[0][0][0],approx[0][0][1]-10), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            print("RECTANGLE")
            # print(approx)
            count = 0
    elif ((len(approx) > 3) & (len(approx) < 5) & (area > 30)  and rect_control(approx[0][0][0],approx[0][0][1],approx[1][0][0],approx[1][0][1],approx[2][0][0],approx[2][0][1],approx[3][0][0],approx[3][0][1]) == 2):
        count += 1
        if count == 2:
            contour_list.append(contour)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(raw_image,'YAMUK',(approx[0][0][0],approx[0][0][1]-10), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            print("YAMUK")
            # print(approx)
            count = 0
    elif ((len(approx) > 2) & (len(approx) < 4) & (area > 30)):
        count += 1
        if count == 2:
            contour_list.append(contour)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(raw_image,'TRIANGLE',(approx[0][0][0],approx[0][0][1]-10), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            print("TRIANGLE")
            # print(approx[0][0][1])
            count = 0
    elif ((len(approx) > 4) & (len(approx) < 6) & (area > 30) ):
        count += 1
        if count == 2:
            contour_list.append(contour)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(raw_image,'PENTAGON',(approx[0][0][0],approx[0][0][1]-10), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            print("PENTAGON")
            # print(approx)
            count = 0
    elif ((len(approx) > 7) & (len(approx) < 9) & (area > 30) ):
        count += 1
        if count == 2:
            contour_list.append(contour)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(raw_image,'OCTAGON',(approx[0][0][0],approx[0][0][1]-10), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            print("OCTAGON")
            # print(approx)
            count = 0
    elif ((len(approx) > 5) & (len(approx) < 7) & (area > 30) ):
        count += 1
        if count == 2:
            contour_list.append(contour)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(raw_image,'HEXAGON',(approx[0][0][0],approx[0][0][1]-10), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            print("HEXAGON")
            count = 0
    elif ((len(approx) > 10) & (area > 30)):
        arr = []
        arrx = []
        arry = []
        for i in approx:
            arr.append(i)
        for i in range(len(arr)):
            arrx.append(arr[i][0][0])
        for i in range(len(arr)):
            arry.append(arr[i][0][1])
        # print(arr)
        # print(arrx)
        # print(np.amin(arrx))
        # print(np.amax(arrx))
        # print(arry)
        # print(np.amin(arry))
        # print(np.amax(arry))
        count += 1
        if count == 2:
            if circle_control(np.amin(arrx),np.amin(arry),np.amax(arrx),np.amax(arry)) == 1:
                contour_list.append(contour)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(raw_image,'CIRCLE',(approx[0][0][0],approx[0][0][1]-10), font, 0.5,(0,0,0),1,cv2.LINE_AA)
                print("CIRCLE")
                # print(approx)
                count = 0
            else:
                contour_list.append(contour)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(raw_image,'ELLIPSE',(approx[0][0][0],approx[0][0][1]-10), font, 0.5,(0,0,0),1,cv2.LINE_AA)
                print("ELLIPSE")
                # print(approx)
                count = 0

cv2.drawContours(raw_image, contour_list,  -1, (0,0,0), 2)
cv2.imshow('Objects Detected',raw_image)
cv2.waitKey(0)


