import math
import numpy
import cv2 as cv
def isNone(value):
  return value == None
def isNotNone(value):
  return not isNone(value)
def canHaveProperties(value):
  return isinstance(value, list) or isinstance(value, tuple) or isinstance(value, set) or isinstance(value, dict) or isinstance(value, numpy.ndarray)
def toNumericValueIfItIs(value):
  try:
    result = float(value)
  except:
    result = None
  return result
def isNumericValue(value):
  return isNotNone(toNumericValueIfItIs(value))
def toIntegerValueIfItIs(value):
  try:
    result = int(value)
  except:
    result = None
  return result
def isIntegerValue(value):
  return isNotNone(toIntegerValueIfItIs(value))
def toNaturalIntegerIfItIs(value):
  result = toIntegerValueIfItIs(value)
  return result if result >= 0 else None
def isNaturalInteger(value):
  return isNotNone(toNaturalIntegerIfItIs(value))
def isNumeric(value):
  pass
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
def isInteger(value): 
  return isinstance(value, int)
def isArrayLike(value):
  return isinstance(value, numpy.ndarray) or isinstance(value, list)
def isIntegerLike(value):
  return isInteger(value) or isinstance(value, numpy.ndarray) or isinstance(value, list) and MyArrayList(value).all(isInteger) or isinstance(value, dict) and MyArrayDict(value).all(isInteger)
def toSimpleArray(value):
  return value if isArrayLike(value) else [] if value == None else [value]
def toListArray(value):
  return MyListArray(toSimpleArray(value))
def toNumericArray(value):
  return MyNumericArray(toSimpleArray(value))
def toNumericArray(value):
  return value if isinstance(value, numpy.ndarray) else (numpy.ndarray([]) if value == None else (numpy.ndarray(value) if isinstance(value, list) else numpy.ndarray([value])))
def toArray(value):
  return value if isinstance(value, numpy.ndarray) else numpy.ndarray([]) if value == None else numpy.ndarray(value) if isinstance(value, list) else numpy.ndarray([value])
def getSameTypeArray(value):
  if(isinstance(value, tuple)):
    result = MyArrayTuple()
  elif(isinstance(value, numpy.ndarray)):
    result = MyNumericArray()
  else:
    result = MyArrayList()
def bindFunctionTo(func, maxCount):
  def result(*positional, **keyword):
    theNewPositional = []
    for index in range(maxCount):
      theNewPositional.append(positional[index])
    return func(*theNewPositional, **keyword)
  return result
"""def bindFunctionTo(func, maxCount = None, keepOnlyThisArguments = None, argumentsToRemove = None, argumentsToAdd = None):
  if isNotNone(maxCount):
    if isNone(keepOnlyThisArguments):
      keepOnlyThisArguments = []
    theRange = range(maxCount)
    for index, value in reversed(enumerate(keepOnlyThisArguments)):
      if not (value in theRange):
        keepOnlyThisArguments.pop(index)
    def theResult(*positional, **keyword):
      thePoisitional = []
      if keepOnlyThisArguments != None:
        for key in keyword:
"""          
class MyArray(object):
  __current_index = 0
  def getCount(this):
    return len(this.getKeys())
  def __init__(this, values = None):
    this.__current_index = 0
    this.values = values
    if values == None:
      super(MyArray, this).__init__()
    else:
      super(MyArray, this).__init__(values)
  def __iter__(this):
    return this
  def __next__(this):
    if this.__current_index >= this.getCount():
      raise StopIteration
      result = None
    else:
      result = (this.getKeys()[this.__current_index], this.getValues()[this.__current_index])
      this.__current_index += 1
    return result
  def getKeys(this):
    result = MyArrayList()
    for index, value in enumerate(this.values):
      result.append(index)
    return result
  def getValues(this):
    result = MyArrayList()
    for index, value in enumerate(this.values):
      result.append(value)
    return result
  def removeByIndexes(this, indexes):
    indexes = toNumericArray(indexes)
    indexes.sort().flip()
    for index in indexes:
      if(len(this) > index):
        this.removeByIndex(index)
    return this
  def removeByIndex(index):
    pass
  def isSame(this):
    result = None
    valueToCompare = None
    for key, value in this:
      if valueToCompare == None:
        valueToCompare = element
      elif value != valueToCompare:
        result = False
      if result != None:
        break
    return ifNone(result, True)
  def any(this, handler):
    result = None
    for key, value in this:
      if(handler(value, key)):
        result = True
      if result != None:
        break
    return ifNone(result, False)
  def filterNonZeroValues():
    return this.filter(bindFunctionTo(isNotZero, 1)).map(bindFunctionTo(getSign, 1))
  def all(this, handler):
    result = None
    for index, element in enumerate(this):
      if not (handler(element, index)):
        result = False
      if result != None:
        break
    if result == None:
      result = True
    return result
  def map(this, handler):
    result = MyArray()
    for index, element in enumerate(this):
      result.push(handler(element, index))
    return result
  def any(this, handler):
    result = None
    for index, element in enumerate(this):
      if(handler(element, index)):
        result = True
      if result != None:
        break
    if result == None:
      result = True
    return result
  def all(this, handler):
    result = None
    for element in this:
      if(not handler(element)):
        result = False
      if result != None:
        break
    if result == None:
      result = True
    return result
  def filter(this, handler):
    result = getSameTypeArray(this)
    for index, element in enumerate(this):
      if(handler(element, index)):
        result.push(element)
    
    return result    
class MyArrayList(MyArray, list):
  def removeByIndex(this, index):
    this.pop(0)
class MyArrayDictionary(MyArray, dict):
  def getKeys(this):
    result = MyArrayList()
    for key in this.values:
      result.append(key)
    return result
  def getValues(this):
    result = MyArrayList()
    for key in this.values:
      result.append(this.values[key])
    return result
  def removeByIndex(this, index):
    del this[index]
class MyNumericArray(MyArray, numpy.ndarray):
  def removeByIndex(this, index):
    this.delete(index, 0)
  def removeByIndexes(this, indexes):
    indexes = toArray(indexes).sort().flip()
    for index in indexes:
      if(len(this) > index):
        this.delete(index, 0)
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
        result.append(toArray(handler(element)))
    return result
  def filter(this, handler):
    result = MyArray()
    for element in this:
      if(handler(element)):
        result.append(toArray(element))
    return result
"""print(toNumericValueIfItIs("3.2"))
aa = MyArrayDictionary({"ss": True, "dd": False})
for ind, ff in aa:
  print(ind)
"""
print(cv.imread('monitor.jpg', cv.IMREAD_UNCHANGED).shape)
#print(type(aa.getValues()))
#print(enumerate(aa))
#arr = MyArray([2, 3])
#print(arr.filter(lambda x: (x == 2)))
#print(getLineParameters(numpy.array([2, 3]), numpy.array([1, 1])))