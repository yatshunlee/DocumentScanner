# author: jasper lee
# github: yatshunlee
# email: yatshunlee@gmail.com

import cv2
import numpy as np
from skimage import transform

def update(x):
    pass

def resize_img(img, scale_percent=20):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized

def crop_image(img, scale_percent):
    resized = resize_img(img, scale_percent)
    cv2.namedWindow('crop image')
    cv2.setMouseCallback('crop image', draw_roi)

def get_corners(co_x,co_y):
    min_co_x, min_co_y = np.min(co_x), np.min(co_y)
    max_co_x, max_co_y = np.max(co_x), np.max(co_y)
    co_x = [(x - min_co_x)/(max_co_x - min_co_x) for x in co_x]
    co_y = [(y - min_co_y)/(max_co_y - min_co_y) for y in co_y]
    inv_co_x = [1/(i) if i!=0 else 999 for i in co_x]

    left_min_idx = np.argmin(np.add(co_x,co_y)) # argmin x+y
    right_min_idx = np.argmin(np.add(inv_co_x,co_y)) # argmin 1/x+y
    left_max_idx = np.argmax(np.add(inv_co_x,co_y)) # argmax 1/x + y
    right_max_idx = np.argmax(np.add(co_x,co_y)) # argmax x + y

    x_lmin, y_lmin = co_x[left_min_idx]*(max_co_x - min_co_x) + min_co_x, \
                     co_y[left_min_idx]*(max_co_y - min_co_y) + min_co_y
    x_rmin, y_rmin = co_x[right_min_idx]*(max_co_x - min_co_x) + min_co_x,\
                     co_y[right_min_idx]*(max_co_y - min_co_y) + min_co_y
    x_lmax, y_lmax = co_x[left_max_idx]*(max_co_x - min_co_x) + min_co_x, \
                     co_y[left_max_idx]*(max_co_y - min_co_y) + min_co_y
    x_rmax, y_rmax = co_x[right_max_idx]*(max_co_x - min_co_x) + min_co_x, \
                     co_y[right_max_idx]*(max_co_y - min_co_y) + min_co_y

    return (x_lmin, y_lmin), (x_rmin, y_rmin), (x_lmax, y_lmax), (x_rmax, y_rmax)

def projective_transform(im, co_x, co_y, LENGTH, WIDTH):
    (x_lmin, y_lmin), (x_rmin, y_rmin),\
    (x_lmax, y_lmax), (x_rmax, y_rmax) = get_corners(co_x, co_y)

    src = np.array([[0, 0], [0, LENGTH], [WIDTH, LENGTH], [WIDTH, 0]])
    dst = np.array([[x_lmin, y_lmin], [x_lmax, y_lmax],
                    [x_rmax, y_rmax], [x_rmin, y_rmin]])

    tform3 = transform.ProjectiveTransform()
    tform3.estimate(src, dst)
    warped = transform.warp(im, tform3, output_shape=(LENGTH, WIDTH))

    warped *= 255.0
    warped = warped.astype(np.uint8)

    return warped