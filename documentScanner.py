# author: jasper lee
# github: yatshunlee
# email: yatshunlee@gmail.com

import os
import cv2
import numpy as np
from helper import *
from tkinter import messagebox

def documentScanner(img_name):
    im = cv2.imread(img_name)
    pts = []
    isEdit = False
    first = True

    while True:
        if first:
            first = False

            # create trackbars
            cv2.namedWindow('Auto Detect')
            cv2.createTrackbar('HIST EQ.', 'Auto Detect', 0, 1, update)
            cv2.createTrackbar('GAUSSIAN BLUR', 'Auto Detect', 5, 9, update)

        # get parameters from trackbars
        GAUSSIAN_BLUR_SIZE = cv2.getTrackbarPos('GAUSSIAN BLUR', 'Auto Detect') * 2 + 1
        HIST_EQ = True if cv2.getTrackbarPos('HIST EQ.', 'Auto Detect')==1 else False

        # draw largest detected contour
        img = np.copy(im)
        max, largest = get_largest_contour(im, GAUSSIAN_BLUR_SIZE, HIST_EQ, CANNY_SOFT=20, CANNY_HARD=160)
        cv2.drawContours(img, largest, -1, (0, 255, 0), 50)

        # resize image by percent of original size
        resized = resize_img(img, scale_percent = 10)
        cv2.imshow("Auto Detect", resized)

        key = cv2.waitKey(90)
        # press Esc or press q to quit
        if key == ord('q') or key == 27:
            exit(0)
        # press E to select ROI
        elif key == ord('e'):
            cv2.destroyAllWindows()
            messagebox.showinfo(
                title='How to edit',
                message='Select the corners from the top left corner to top right corner anticlockwise'
            )
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

                    cv2.imshow('Crop Image', roi_img)

                # create a copy and resize it
                img = np.copy(im)
                scale_percent = 15
                resized = resize_img(img, scale_percent)

                # create a window to select roi
                cv2.namedWindow('Crop Image')
                cv2.setMouseCallback('Crop Image', draw_roi)

                # press Enter to continue after selected ROI
                # press Esc or press q to leave
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:
                    exit(0)
                elif key == 13:
                    isEdit = True
                    break
                elif key == ord('a'):
                    first = True
                    break

            cv2.destroyAllWindows()
            if isEdit:
                break

        elif key == 13:  # press Enter
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

        # # Debug use
        # img = np.copy(im)
        # cv2.drawContours(img, ch_largest, -1, (0,255,0), 100)
        # resized = resize_img(img, 15)
        # cv2.imshow('convex hull',resized)
        # cv2.waitKey(0)

        ch_largest = np.squeeze(ch_largest)

        for pt in ch_largest:
            co_x.append(pt[0])
            co_y.append(pt[1])

    A4_size = (3508, 2480)
    LENGTH, WIDTH = A4_size[0], A4_size[1]

    warped = projective_transform(im, co_x, co_y, LENGTH, WIDTH, isEdit)
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    cv2.namedWindow('Filter')
    cv2.createTrackbar('ORIGINAL/GRAY/B&W','Filter',0,2,update)
    cv2.createTrackbar('THRESHOLDING (For B&W)','Filter',127,255,update)

    while True:
        ORIGINAL = cv2.getTrackbarPos('ORIGINAL/GRAY/B&W', 'Filter')
        THRESHOLDING = cv2.getTrackbarPos('THRESHOLDING (For B&W)', 'Filter')

        if ORIGINAL==2: # B&W image
            ret,thresh_BI = cv2.threshold(gray,THRESHOLDING,255,cv2.THRESH_BINARY)
            resized = resize_img(thresh_BI, scale_percent=15)
        elif ORIGINAL==1: # grayscale image
            resized = resize_img(gray, scale_percent=15)
        else: # original image
            resized = resize_img(warped, scale_percent=15)

        cv2.imshow("Filter", resized)

        key = cv2.waitKey(90)
        if key == ord('q') or key == 27:  # Esc or press q
            exit(0)
        elif key == 13:  # press Enter
            output = thresh_BI if ORIGINAL==2 else gray if ORIGINAL==1 else warped
            break

    if not os.path.exists('./tmp'):
        os.mkdir('./tmp')

    file_name = img_name.split('/')[-1]
    output_name = './tmp/' + file_name.split('.')[0] + "_tmp." +file_name.split('.')[1]
    cv2.imwrite(output_name, output)
    cv2.destroyAllWindows()