# author: jasper lee
# github: yatshunlee
# email: yatshunlee@gmail.com

import os
import cv2
import numpy as np
from helper import *
import easygui
import argparse

parser = argparse.ArgumentParser(description='Scanning A4 size document.')
parser.add_argument('image', metavar='img', type=str, help='image to process')

args = parser.parse_args()
img_name = args.image
im = cv2.imread(img_name)

cv2.namedWindow('Tuner')

cv2.createTrackbar('GAUSSIAN BLUR','Tuner',5,9,update)
cv2.createTrackbar('CANNY SOFT','Tuner',20,255,update)
cv2.createTrackbar('CANNY HARD','Tuner',160,255,update)

pts = []

while True:
    GAUSSIAN_BLUR_SIZE = cv2.getTrackbarPos('GAUSSIAN BLUR', 'Tuner') * 2 + 1
    CANNY_SOFT = cv2.getTrackbarPos('CANNY SOFT', 'Tuner')
    CANNY_HARD = cv2.getTrackbarPos('CANNY HARD', 'Tuner')

    # convert into canny edge image
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    blurred = cv2.GaussianBlur(gray, (GAUSSIAN_BLUR_SIZE, GAUSSIAN_BLUR_SIZE), 0)
    binaryIMG = cv2.Canny(blurred, CANNY_SOFT, CANNY_HARD)

    # find contours
    contours, hierarchy = cv2.findContours(binaryIMG, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    max, largest = 0, None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max:
            max = area
            largest = cnt

    # draw largest detected contour
    img = np.copy(im)
    cv2.drawContours(img, largest, -1, (0, 255, 0), 50)

    # resize image by percent of original size
    resized = resize_img(img, scale_percent = 10)

    cv2.imshow("Tuner", resized)
    key = cv2.waitKey(90)

    # press Esc or press q to quit
    if key == ord('q') or key == 27:
        exit(0)

    # press E to select ROI
    elif key == ord('e'):
        cv2.destroyAllWindows()

        while True:

            def draw_roi(event, x, y, flags, param):
                roi_img = resized.copy()

                if event == cv2.EVENT_LBUTTONDOWN:  # LEFT CLICK: select corner
                    pts.append((x, y))

                if event == cv2.EVENT_RBUTTONDOWN:  # RIGHT CLICK: cancel selected corner
                    pts.pop()

                # if more than one point drawn, connect the points with a line
                if len(pts) > 0:
                    cv2.circle(roi_img, pts[-1], 3, (0, 255, 0), -1)

                if len(pts) > 1:
                    for i in range(len(pts) - 1):
                        cv2.circle(roi_img, pts[i], 5, (0, 0, 255), -1)  # x ,y 为鼠标点击地方的坐标
                        cv2.line(img=roi_img, pt1=pts[i], pt2=pts[i + 1], color=(0, 255, 0), thickness=2)

                cv2.imshow('crop image', roi_img)

            # create a copy and resize it
            img = np.copy(im)
            scale_percent = 15
            resized = resize_img(img, scale_percent)

            # create a window to select roi
            cv2.namedWindow('crop image')
            cv2.setMouseCallback('crop image', draw_roi)

            # press Enter to continue after selected ROI
            # press Esc or press q to leave
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                print('exit')
                exit(0)
            elif key == 13:
                break
        cv2.destroyAllWindows()
        break

    elif key == 13:  # press Enter
        print('selected')
        cv2.destroyAllWindows()
        break

co_x, co_y = [], []

# points from customized roi
if pts:
    for pt in pts:
        co_x.append(pt[0]/scale_percent*100)
        co_y.append(pt[1]/scale_percent*100)
# points from convex hull
else:
    ch_largest = cv2.convexHull(largest)
    ch_largest = np.squeeze(ch_largest)

    for pt in ch_largest:
        co_x.append(pt[0])
        co_y.append(pt[1])

A4_size = (3508, 2480)
LENGTH, WIDTH = A4_size[0], A4_size[1]

warped = projective_transform(im, co_x, co_y, LENGTH, WIDTH)
gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('Threshold Tuner')
cv2.createTrackbar('ORIGINAL/GRAY/B&W','Threshold Tuner',0,2,update)
cv2.createTrackbar('THRESHOLDING','Threshold Tuner',127,255,update)

while True:
    ORIGINAL = cv2.getTrackbarPos('ORIGINAL/GRAY/B&W', 'Threshold Tuner')
    THRESHOLDING = cv2.getTrackbarPos('THRESHOLDING', 'Threshold Tuner')

    if ORIGINAL==2: # B&W image
        ret,thresh_BI = cv2.threshold(gray,THRESHOLDING,255,cv2.THRESH_BINARY)
        resized = resize_img(thresh_BI, scale_percent=15)
    elif ORIGINAL==1: # grayscale image
        resized = resize_img(gray, scale_percent=15)
    else: # original image
        resized = resize_img(warped, scale_percent=15)

    cv2.imshow("Resized image", resized)

    key = cv2.waitKey(90)
    if key == ord('q') or key == 27:  # Esc or press q
        print('break')
        exit(0)
    elif key == 13:  # press Enter
        print('save photo')
        output = thresh_BI if ORIGINAL==2 else gray if ORIGINAL==1 else warped
        break

if not os.path.exists('./output'):
    os.mkdir('./output')

output_name = './output/' + img_name.split('.')[0] + "_output." +img_name.split('.')[1]
cv2.imwrite(output_name, output)