import cv2
import numpy as np


def find_all_mushrooms(img):
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    bounds = ([0, 0, 0], [10, 255, 255])
    lower = np.array(bounds[0])
    upper = np.array(bounds[1])
    mask = cv2.inRange(image, lower, upper)
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    result = cv2.bitwise_and(image, image, mask=mask)
    print(np.count_nonzero(result) / image.size)
    cv2.imshow('result', result)
    cv2.waitKey(5000)
    return np.count_nonzero(result) / image.size > 0.05


def find_flowering_mushrooms(img):
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    bounds = ([0, 0, 0], [10, 255, 255])
    lower = np.array(bounds[0])
    upper = np.array(bounds[1])
    mask = cv2.inRange(image, lower, upper)
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    result = cv2.bitwise_and(image, image, mask=mask)
    print(np.count_nonzero(result) / image.size)
    cv2.imshow('result', result)
    cv2.waitKey(5000)
    return np.count_nonzero(result) / image.size > 0.3
