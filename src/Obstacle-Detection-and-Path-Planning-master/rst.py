import cv2
import numpy as np
import math
import warnings


def get_moments(img, param1, param2, mode=0):

    img1 = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array(param1)
    upper = np.array(param2)

    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(hsv, hsv, mask=mask)

    # Morphology operations are done to get a clean mask
    kernel = np.ones((5, 5), np.uint8)
    kernel_open = np.ones((2, 2), np.uint8)
    # res = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)

    res = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel_open)
    res = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)
    res = cv2.GaussianBlur(res, (5, 5), 0)
    # cv2.imshow("window", res)

    if mode > 0:
        f_name = 'Position/Start'+str(mode)+'.jpg'
        cv2.imwrite(f_name, res)

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("imshow", gray)
    ret, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_TOZERO)

    # Finding the centroid of the masked region by finding contours
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # largest_contour = get_largest_contour(contours)

    biggest = 0
    max_area = 0
    min_size = thresh.size/4
    index1 = 0
    peri = 1
    for i in contours:
        area = cv2.contourArea(i)
        if area > 10000:
            peri = cv2.arcLength(i, True)

        if area > max_area:
            biggest = index1
            max_area = area
        index1 = index1 + 1

    if len(contours):
        M = cv2.moments(contours[biggest])
        cx = int(M['m10']//M['m00'])
        cy = int(M['m01']//M['m00'])

        cv2.circle(img1, (cx, cy), 10, (0, 255, 0), -1)

        return cx, cy, img1
    else:
        return 0,0,img1



def get_direction(x1, x2, y1, y2):


    dx = x2-x1
    dy = y2-y1
    print (dx,dy)

    # Calculte the angle
    rads = math.atan2(dy, dx)
    degs = math.degrees(rads)

    return degs

def path_encode(car_angle, actual_angle):

    print('car_angle', car_angle)
    print('actual_angle', actual_angle)

    degs = car_angle - actual_angle

    
    if -15 <= degs <= 15:
        return '1'    #north
    elif 0<=degs <= 90:
        return '3'    #south
    elif -90 <= degs <= 0:
        return '4'  #left
        
    else:
        warnings.warn('Error in Direction Detection!')
        return '0'