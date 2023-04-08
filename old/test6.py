import cv2
import numpy
from matplotlib import pyplot as plt
from functions import isNone
def getByParam(image, index, maxOffset = 81, isForImage = True):
  return cv2.Canny(cv2.cvtColor(numpy.stack(((cv2.cvtColor(image, cv2.COLOR_RGB2HSV)[:, :, index]), ) * 3, axis=-1), cv2.COLOR_BGR2GRAY), 12, 12 + maxOffset).astype(numpy.ubyte) if isForImage else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(numpy.ubyte);
def printEdges(edges):
  plt.subplot(1, 1, printEdges.plotIndex), plt.imshow(edges)
  printEdges.plotIndex += 1
def getImage(path):
  stream = open('images/' + path, 'rb')
  bytes = bytearray(stream.read())
  array = numpy.asarray(bytes, dtype=numpy.uint8)
  return cv2.imdecode(array, cv2.IMREAD_COLOR)  
def getCountours(path):
  original = getImage(path)
  byValueInHSV = getByParam(original, 2, isForImage = (path[0:11] == "watermarked"))
  (contours, _) = cv2.findContours(byValueInHSV, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  print(contours[0])
  return contours
  cv2.drawContours(original, contours, -1, (0, 0, 255))
  plt.subplot(111), plt.imshow(original)
  plt.show()
  
KCountours = getCountours("letters/К.png")
theCountours = getCountours("watermarked/1.jpg")
theMins = []
for indexOfTheContour, countour in enumerate(theCountours):
  value = cv2.matchShapes(countour, KCountours[0], cv2.CONTOURS_MATCH_I1, 0)
  #if value <= 0.3:
  theMins.append((indexOfTheContour, value))
#print(theCountours[theMins[0]])
original = getImage("watermarked/2.jpg")
for theMin in theMins:
  cv2.drawContours(original, [theCountours[theMin[0]]], -1, (0, 0, 255))
plt.subplot(111), plt.imshow(original)
plt.show()
cv2.imread("images/watermarked/1.jpg", cv2.IMREAD_UNCHANGED)

stream = open("images/letters/К.png", 'rb')
bytes = bytearray(stream.read())
array = numpy.asarray(bytes, dtype=numpy.uint8)
bgrImage = cv2.imdecode(array, cv2.IMREAD_UNCHANGED)

#cv2.imread(().encode("utf8").decode('cp866'), cv2.IMREAD_UNCHANGED)