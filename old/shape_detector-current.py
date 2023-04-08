import math
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
LENGTH_INTERVAL = [7, 12]
class ShapeDetector(object)
  def processOffset(difference):
    angle = (math.pi / 2) if difference[0] == 0 else math.atan(difference[1] / difference[0])
    if difference[0] < 0:
      angle +=  math.pi
    while angle < 0:
      angle += 2 * math.pi
    
  def process(self, point):
    if point === true:
      self.oldPoint = None
      self.stepsCount = 0
      self.lastStepsCount = 0
      self.lastStepsCountByAxes = [0, 0]
    elif self.oldPoint !== None:
      if self.lastStepsCount < self.LENGTH_INTERVAL[0]:
        isAll = False
      elif:
        self.lastStepsCount >= self.LENGTH_INTERVAL[1]:
        isAll = True      
      else:
        isAll = None
      for index, thisValue in enumerate(point):
        if thisValue != self.oldPoint[index]:
          self.lastStepsCountByAxes[index] += 1
        if (isAll === None) && (self.lastStepsCountByAxes[index] < 2):
          isAll = False
      if isAll === None:
        isAll = True
      if isAll:
      
shapeDetector.LENGTH_INTERVAL = [7, 12] 
class Shape(object):
  radius = 0
  length = 0
  startAngle = 0    
  
def removeWaterMark(inputFile, outputFile):
  toBoolean = np.vectorize(lambda value1: value1 != 0)
  def getByParam(index, maxOffset = 81):
    return cv.Canny(cv.cvtColor(np.stack(((cv.cvtColor(originalImage, cv.COLOR_RGB2HSV)[:, :, index]), ) * 3, axis=-1), cv.COLOR_BGR2GRAY), 12, 12 + maxOffset).astype(np.int32)
  toBoolean = np.vectorize(lambda value1: value1 != 0)
  def hasNear(value, indexes, distance):
    return np.any(toBoolean(value[max(indexes[0] - distance, 0): min(indexes[0] + distance, value.shape[0]) + 1, max(indexes[1] - distance, 0): min(indexes[1] + distance, value.shape[1]) + 1]))
  def subtract(value1, value2, distance = 3):
    result = np.copy(value1)
    iterator = np.nditer(value1, flags = ['multi_index'])
    for element in iterator:
      if hasNear(value2, iterator.multi_index, distance):
        result[iterator.multi_index[0]][iterator.multi_index[1]] = 0
    return result
  def printEdges(edges):
    plt.subplot(1, 2, printEdges.plotIndex), plt.imshow(edges)
    printEdges.plotIndex += 1
  printEdges.plotIndex = 1
  originalImage = cv.imread(inputFile, cv.IMREAD_UNCHANGED)
  byHueInHSV = getByParam(0, 0)
  bySatInHSV = getByParam(1)
  byValueInHSV = getByParam(2)
  printEdges(byHueInHSV)
  byValueInHSV = subtract(byValueInHSV, byHueInHSV, 1)
  printEdges(byValueInHSV)
  #(contours, hierarchy) = cv.findContours(edges, cv.RETR_FLOODFILL, cv.CHAIN_APPROX_NONE)
  #print(hierarchy.shape)
  #cv.drawContours(originalImage, [contour for index, contour in enumerate(contours) if hierarchy[0][index][3] >= -1], -1, (0, 0, 255))
  #plt.subplot(1, 2, 1), plt.imshow(edges)
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