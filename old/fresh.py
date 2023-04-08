import copy
import numpy
import cv2 as cv
from matplotlib import pyplot as plt
def canHaveProperties(value):
  return isinstance(value, list) or isinstance(value, tuple) or isinstance(value, set) or isinstance(value, dict) or isinstance(value, numpy.ndarray)
class MyCommonObject(object):
  theId = None
  values = None
  def __init__(this, value1 = None, value2 = None, value3 = None):
    this.theId = MyCommonObject.id
    MyCommonObject.id += 1
    if(canHaveProperties(value1)):
      this.values = value1
    else:
      this.values = []
      if(value1 != None):
        this.values.append(value1)
      if(value2 != None):
        this.values.append(value2)
      if(value3 != None):
        this.values.append(value3)
def getValuesByArguments(value1 = None, value2 = None, value3 = None):
  if(canHaveProperties(first)):
    result = first
  else:
    result = []
    if(value1 != None):
      result.append(value1)
    if(value2 != None):
      result.append(value2)
    if(value3 != None):
      result.append(value3)
  return result
class Color(MyCommonObject):
  pass
class Coordinate(MyCommonObject):
  def __hash__(this):
    return this.values[0] + ":" + this.values[1]
  def __eq__(this, other):
    return this.__hash__() == other.__hash__()
def toMyArray(value):
  result = None
  if isinstance(value, tuple) and not(isinstance(value, MyArrayTuple)):
    result = MyArrayTuple(value)
  elif isinstance(value, dict) and not(isinstance(value, MyArrayDictionary)):
    result = MyArrayDictionary(value)
  elif isinstance(value, list) and not(isinstance(value, MyArrayList)):
    result = MyArrayList(value)
  elif isinstance(value, numpy.ndarray) and not(isinstance(value, MyNumericArray)):
    result = MyNumericArray(value)
  if isNone(result):
    result = value
  return result
def clone(value):
  return copy.deepcopy(value)
def forEach(receivedElement, handler, deptch = 1, preKeys = []):
  element = toMyArray(receivedElement)
  deptch -= 1
  index = len(preKeys)
  preKeys.append(None)
  result = True
  for key, value in element:
    preKeys[index] = key
    if deptch == 0:
      result = handler(preKeys, value)
    else:
      result = forEach(value, handler, deptch, preKeys)
    if result == False:
      break
  return result 
class Image(MyArrayDictionary):
  def __init__(this, path):
    this.image = cv.imread(path, cv.IMREAD_UNCHANGED)
    this.values = dict()
    def processPixel(coordinate, color):
      this.values[Coordinate(coordinate)] = Color(color)
    forEach(this.image, processPixel, 2)
MyCommonObject.id = 0
color = Color()
print(color.theId)
print(super(type(range(3))))
def fn(*b, **a):
    for i in a.items():
        print (i)
fn(3)
def bindFunctionTo(func, maxCount):
  def result(*positional, **keyword):
    theNewPositional = []
    for index in range(maxCount):
      theNewPositional.append(positional[index])
    return func(*theNewPositional, **keyword)
  return result
myPrint = bindFunctionTo(print, 2)
print(3, 2, 1)
myPrint(3, 2, 1);