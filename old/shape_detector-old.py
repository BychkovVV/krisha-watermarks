import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img = cv.cvtColor(cv.imread('monitor.jpg', cv.IMREAD_UNCHANGED), cv.COLOR_RGB2HSV)[:, :, 2]
img = np.stack((img,)*3, axis=-1)
edges = cv.Canny(img, 32, 210)
lines = cv.HoughLinesP(edges, 1, np.pi / 360, 0, np.array([]), 0, 0)
print(lines.shape)
# iterate over the output lines and draw them
for line in lines:
    for x1, y1, x2, y2 in line:
        cv.line(img, (x1, y1), (x2, y2), color=(20, 220, 20), thickness=3)
print(edges[0][0])
plt.subplot(111),plt.imshow(img)
plt.show()