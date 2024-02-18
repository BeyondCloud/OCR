import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('resources/btn_U.png', 0)
ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
cv2.imwrite(f"tmp/thres.jpg", th1)
