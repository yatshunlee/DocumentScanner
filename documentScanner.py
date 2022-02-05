# author: jasper lee
# github: yatshunlee
# email: yatshunlee@gmail.com

import cv2
import numpy as np
from skimage import transform

import argparse

parser = argparse.ArgumentParser(description='Scanning A4 size document.')
parser.add_argument('image', metavar='img', type=str, help='image to process')

args = parser.parse_args()
img_name = args.image
im = cv2.imread(img_name)

cv2.namedWindow('Tuner')

def update(x):
    pass

cv2.createTrackbar('GAUSSIAN BLUR','Tuner',5,9,update)
cv2.createTrackbar('CANNY SOFT','Tuner',20,255,update)
cv2.createTrackbar('CANNY HARD','Tuner',160,255,update)

while True:
    GAUSSIAN_BLUR_SIZE = cv2.getTrackbarPos('GAUSSIAN BLUR', 'Tuner') * 2 + 1
    CANNY_SOFT = cv2.getTrackbarPos('CANNY SOFT', 'Tuner')
    CANNY_HARD = cv2.getTrackbarPos('CANNY HARD', 'Tuner')

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    blurred = cv2.GaussianBlur(gray, (GAUSSIAN_BLUR_SIZE, GAUSSIAN_BLUR_SIZE), 0)
    binaryIMG = cv2.Canny(blurred, CANNY_SOFT, CANNY_HARD)
    contours, hierarchy = cv2.findContours(binaryIMG, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    max, largest = 0, None

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max:
            max = area
            largest = cnt

    img = np.copy(im)
    cv2.drawContours(img, largest, -1, (0,255,0),100)
    scale_percent = 20  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow("Resized image", resized)
    key = cv2.waitKey(90)

    if key == ord('q') or key == 27:  # Esc or press q
        print('break')
        exit(0)
    elif key == 13:  # press Enter
        print('crop image')
        cv2.destroyAllWindows()
        break

ch_largest = cv2.convexHull(largest)
ch_largest = np.squeeze(ch_largest)
co_x, co_y = [], []
for pt in ch_largest:
    co_x.append(pt[0])
    co_y.append(pt[1])

min_co_x, min_co_y = np.min(co_x), np.min(co_y)
max_co_x, max_co_y = np.max(co_x), np.max(co_y)
co_x = [(x - min_co_x)/(max_co_x - min_co_x) for x in co_x]
co_y = [(y - min_co_y)/(max_co_y - min_co_y) for y in co_y]
inv_co_x = [1/(i) if i!=0 else 999 for i in co_x]

left_min_idx = np.argmin(np.add(co_x,co_y)) # min x+y
right_min_idx = np.argmin(np.add(inv_co_x,co_y)) # min 1/x+y
left_max_idx = np.argmax(np.add(inv_co_x,co_y)) # max 1/x + y
right_max_idx = np.argmax(np.add(co_x,co_y)) # max x + y

x_lmin, y_lmin = co_x[left_min_idx]*(max_co_x - min_co_x) + min_co_x, \
                 co_y[left_min_idx]*(max_co_y - min_co_y) + min_co_y
x_rmin, y_rmin = co_x[right_min_idx]*(max_co_x - min_co_x) + min_co_x,\
                 co_y[right_min_idx]*(max_co_y - min_co_y) + min_co_y
x_lmax, y_lmax = co_x[left_max_idx]*(max_co_x - min_co_x) + min_co_x, \
                 co_y[left_max_idx]*(max_co_y - min_co_y) + min_co_y
x_rmax, y_rmax = co_x[right_max_idx]*(max_co_x - min_co_x) + min_co_x, \
                 co_y[right_max_idx]*(max_co_y - min_co_y) + min_co_y

src = np.array([[0, 0], [0, 2970], [2100, 2970], [2100, 0]])
dst = np.array([[x_lmin, y_lmin], [x_lmax, y_lmax],
                [x_rmax, y_rmax], [x_rmin, y_rmin]])

tform3 = transform.ProjectiveTransform()
tform3.estimate(src, dst)
warped = transform.warp(im, tform3, output_shape=(2970, 2100))

warped *= 255.0
warped = warped.astype(np.uint8)

gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('Threshold Tuner')
cv2.createTrackbar('THRESHOLDING','Threshold Tuner',127,255,update)

while True:
    THRESHOLDING = cv2.getTrackbarPos('THRESHOLDING', 'Threshold Tuner')
    ret,thresh_BI = cv2.threshold(gray,THRESHOLDING,255,cv2.THRESH_BINARY)

    scale_percent = 20  # percent of original size
    width = int(thresh_BI.shape[1] * scale_percent / 100)
    height = int(thresh_BI.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(thresh_BI, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow("Resized image", resized)
    key = cv2.waitKey(90)

    if key == ord('q') or key == 27:  # Esc or press q
        print('break')
        exit(0)
    elif key == 13:  # press Enter
        print('save photo')
        break

output_name = img_name.split('.')[0] + "_output." +img_name.split('.')[1]
cv2.imwrite(output_name, thresh_BI)