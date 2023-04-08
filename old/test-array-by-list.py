import math
import numpy
import cv2 as cv
def getAntiIndex(index):
  return 0 if index == 1 else 1
def minInPoint(point):
  return min(point[0], point[1])
def getAngle(point1, point2):
  difference = point2 - point1
  angle = (math.pi / 2) if difference[0] == 0 else math.atan(difference[1] / difference[0])
  if difference[0] < 0:
    angle +=  math.pi
  while angle < 0:
    angle += 2 * math.pi
  return angle
def isNotZero(value):
  return value != 0
def getSign(value):
  return 1 if value >= 0 else -1
def getLineParameters(point1, point2):
  distance = math.dist(point2, point1)
  return dict([("length", distance), ("angle", getAngle(point2, point1))] if distance > 0 else [("length", 0), ("angle", None)])
def toArray(value):
  return value if isinstance(value, list) else [] if value == None else [value]
class MyArray(list):
  def removeByIndexes(this, indexes):
    indexes = toArray(indexes)
    indexes.sort(reverse=True)
    for index in indexes:
      if(len(this) > index):
        this.pop(index)
    return this
  def isSame(this):
    result = None
    value = None
    for element in this:
      if value == None:
        value = element
      elif element != value:
        result = False
      if result != None:
        break
    if result == None:
      result = True
    return result
  def filterNonZeroValues():
    return this.filter(isNotZero).map(getSign)
  def map(this, handler):
    result = MyArray()
    for element in this:
        result.append(handler(element))
    return result
  def filter(this, handler):
    result = MyArray()
    for element in this:
      if(handler(element)):
        result.append(element)
    return result  
print(toArray(MyArray([3, 2, 4])).removeByIndexes([1, 99]))

#arr = MyArray([2, 3])
#print(arr.filter(lambda x: (x == 2)))
#print(getLineParameters(numpy.array([2, 3]), numpy.array([1, 1])))