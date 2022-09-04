"""
Steps to completion of project:
1. Find the lower and upper values of Hue, Saturation, Value of each intended color.
2. Create a mask
3. Detect the contour using the mask
4. Draw the color on screen in real time.
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

my_colors = [[89, 55, 29, 154, 244, 219],       #blue
             [42, 60, 10, 92, 255, 111],        #Green
             [17, 188, 54, 30, 255, 245],       #yellow
             [152, 77, 32, 179, 224, 255]]     #Pink
#[hue_min, sat_min, val_min, hue_max, sat_max, val_max]

my_colors_value = [[255, 0, 0],
                   [0, 255, 0],
                   [0, 255, 255],
                   [117, 3, 173]]

my_points = []          # [x, y, colorIndex]

def find_color(img):
    HSV_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    new_points = []
    for color in my_colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(HSV_img, lower, upper)
        #cv2.imshow(str(color), mask)
        x, y = get_contours(mask)
        cv2.circle(result_img, (x, y), 10, my_colors_value[count], cv2.FILLED)
        if x != 0 and y != 0:
            new_points.append([x, y, count])
        count += 1
    return new_points

def get_contours(mask):
    countours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in countours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(result_img, cnt, -1, (255, 0, 0), 2)
            perimeter = cv2.arcLength(cnt, True)
            corners = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            x, y, w, h = cv2.boundingRect(corners)
    return x + w//2, y

def draw_on_canvas(points):
    for point in points:
        cv2.circle(result_img, (point[0], point[1]), 10, my_colors_value[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    result_img = img.copy()

    new_points = find_color(img)

    if len(new_points) != 0:
        for p in new_points:
            my_points.append(p)

    if len(my_points) != 0:
        draw_on_canvas(my_points)

    cv2.imshow("Result", result_img)

    if cv2.waitKey(1) & 0xFF == 'q':
        break