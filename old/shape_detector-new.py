import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
def removeWaterMark(inputFile, outputFile):
  originalImage = cv.imread(inputFile, cv.IMREAD_UNCHANGED)
  byValueInHSV = cv.cvtColor(originalImage, cv.COLOR_RGB2HSV)[:, :, 2]
  edges = cv.Canny(byValueInHSV, 0, 300)
  contours = cv.findContours(byValueInHSV, cv.RETR_FLOODFILL, cv.CHAIN_APPROX_NONE)
  drawContours(originalImage, contours, -1, (0, 0, 255))
  plt.subplot(111), plt.imshow(originalImage)
  plt.show()
#result is dilated for marking the corners, not important
#dst = cv.dilate(dst,None)
# Threshold for an optimal value, it may vary depending on the image.
#img[dst>0.01*dst.max()]=[0,0,255]

#lines = cv.HoughLinesP(edges, 1, np.pi / 360, 0, np.array([]), 0, 0)
#print(lines.shape)
# iterate over the output lines and draw them
#for line in lines:
#    for x1, y1, x2, y2 in line:
#        cv.line(img, (x1, y1), (x2, y2), color=(20, 220, 20), thickness=3)
removeWaterMark("C:/Users/Administrator/Pictures/10-full.jpg", "C:/Users/Administrator/Pictures/10-full-output.jpg")