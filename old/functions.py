from constants import STANDARD_MAX_ERROR, THE_LOGS_FOLDER, DEBUG_IS_ON
from common import die, isDefined, isUndefined, clone, isNone, isNotNone,MyArray, isBoolean, isScalar, isArray, isKey, isNumeric, isString, outStatus, profilePrint
import traceback, sys, numpy, copy, os
from datetime import datetime
def isBetter(value1, value2, isMore = False):
  return isDefined(value1) if isUndefined(value2) else (False if isUndefined(value1) else ((value1 > value2) if isMore else (value2 > value1)))
def purgeFolder(folder):
  if os.path.exists(folder) and os.path.isdir(folder):
    files = os.listdir(folder)
    for file in files:
      thisPath = os.path.join(folder, file)
      if os.path.exists(thisPath):
        if os.path.isdir(thisPath):
          purgeFolder(thisPath)
          os.rmdir(thisPath)
        elif os.path.isfile(thisPath):
          os.remove(thisPath)
logThisCalled = False
def isNotEmptyColorDifference(values):
  return (values[0] != 0) or (values[1] != 0) or (values[2] != 0)
def detectColorDifferenceFast(oldColor, newColor):
  theOldColor = [int(oldColor[0]), int(oldColor[1]), int(oldColor[2])]
  theNewColor = [int(newColor[0]), int(newColor[1]), int(newColor[2])]
  firstMore = theNewColor[0] > theOldColor[0]
  EMPTY = [0, 0, 0]
  printDebug("((((FirstMore = theNewColor[0] > theOldColor[0]) = {}) != (((theNewColor[1] > theOldColor[1]) = {}))) or ((firstMore != ((theNewColor[2] > theOldColor[2]) = {})))) = {}".format(firstMore, theNewColor[1] > theOldColor[1], theNewColor[2] > theOldColor[2], (firstMore != (theNewColor[1] > theOldColor[1])) or (firstMore != (theNewColor[2] > theOldColor[2]))))
  if (firstMore != (theNewColor[1] > theOldColor[1])) or (firstMore != (theNewColor[2] > theOldColor[2])):    
    printDebug("return empty")
    return EMPTY  
  try:
    diff1 = theNewColor[0] - theOldColor[0]
  except:
    print('theNewColor[0] = {}, theOldColor[0] = {}'.format(theNewColor[0], theOldColor[0]))
  absDiff1 = abs(diff1)
  printDebug("diff1 = {}, absDiff1 = {}".format(diff1, absDiff1))
  if absDiff1 > 70:
    printDebug("absDiff1 > 70, return empty")
    return EMPTY
  diff2 = theNewColor[1] - theOldColor[1]
  absDiff2 = abs(diff2)  
  printDebug("diff2 = {}, absDiff2 = {}".format(diff2, absDiff2))
  if absDiff2 > 70:
    printDebug("absDiff2 > 70, return empty")
    return EMPTY
  if((abs(theNewColor[1] - theNewColor[0]) > 40) and abs(diff2 - diff1) > 20):
    return EMPTY
  diff3 = theNewColor[2] - theOldColor[2]
  absDiff3 = abs(diff3)
  printDebug("diff3 = {}, absDiff3 = {}".format(diff3, absDiff3))
  if absDiff3 > 70:
    printDebug("absDiff3 > 70, return empty")
    return EMPTY
  if((abs(theNewColor[2] - theNewColor[0]) > 40) and abs(diff3 - diff1) > 20):
    printDebug("((abs(theNewColor[2] - theNewColor[0]) > 40) and abs(diff3 - diff1) > 20), return empty")
    return EMPTY
  if((abs(theNewColor[2] - theNewColor[1]) > 40) and abs(diff3 - diff2) > 20):
    printDebug("((abs(theNewColor[2] - theNewColor[1]) > 40) and abs(diff3 - diff2) > 20), return empty")
    return EMPTY
  if((absDiff1 >= 4) or (absDiff2 >= 4) or (absDiff3 >= 4)):
    maxError1 = int(absDiff1 / 12)
    maxError2 = int(absDiff2 / 12)
    printDebug("maxError1 = {}, maxError2 = {}".format(maxError1, maxError2))
    if abs(absDiff2 - absDiff1) <= maxError1 + maxError2:
      maxError3 = int(absDiff3 / 12)
      if (abs(absDiff3 - absDiff1) <= maxError1 + maxError3) and (abs(absDiff3 - absDiff2) <= maxError2 + maxError3):
        printDebug("passed all conditions, return [{}, {}, {}]".format(diff1, diff2, diff3))
        return [diff1, diff2, diff3]
      else:
        printDebug("(abs(absDiff3 - absDiff1) > maxError1 + maxError3) or (abs(absDiff3 - absDiff2) > maxError2 + maxError3), return empty")
    else:
      printDebug("abs(absDiff2 - absDiff1) > maxError1 + maxError2, return empty")
  else:
    printDebug("(absDiff1 < {}) and (absDiff2 < {}) and (absDiff3 < {}), return empty".format(4, 4, 4))
  return EMPTY
def setFilePathToLog(value):
  global theFilePathToLog
  theFilePathToLog = value
theFilePathToLog = None
def logThis(string, filename = None):
  global logThisCalled, theFilePathToLog
  if not logThisCalled:
    purgeFolder(THE_LOGS_FOLDER)
    logThisCalled = True
  if isUndefined(theFilePathToLog):
    if isUndefined(filename):
      filename = 'main'
    thePath = os.path.join(THE_LOGS_FOLDER, filename + '.log')
  else:
    thePath = theFilePathToLog
  with open(thePath, 'a', encoding='utf-8') as theFile:
    prefix = "\n" if (os.path.exists(thePath) and os.path.isfile(thePath) and (os.path.getsize(thePath) > 0)) else ""
    theDate = str(datetime.now())
    print(prefix + theDate + ': ' + string, file = theFile, end = '')
thisDebugString = ''
isDebugging = False
def outDebug():
  global DEBUG_IS_ON
  if DEBUG_IS_ON:
    global isDebugging, thisDebugString
    if isDebugging:
      print(thisDebugString)
    logThis(thisDebugString)
    thisDebugString = ''
def processString(string, *elements):
  if len(elements):
    string = string.format(* elements)
  return string
def printDebug(string, *values):
  global DEBUG_IS_ON
  if DEBUG_IS_ON:
    string = processString(string, *values)
    global isDebugging
    if True or isDebugging:
      global thisDebugString
      if len(thisDebugString) > 0:
        thisDebugString += ", "
      thisDebugString += string      
def getAllDirections():
  result = []
  for index1 in range(-1, 2):
    for index2 in range(-1, 2):
      result.append([index1, index2])
  return result
def isInRect(pix, rect):
  return (pix[0] >= 0) and (pix[1] >= 0) and (pix[0] < rect[0]) and (pix[1] < rect[1])
def eachPixelsPair(size, handler, coords = None):
  def isCompletedMark(value):
    return value == False
  thisPixel = [0, 0]
  print("Loop")
  def getRange(index, isReversed = False):
    if coords is None:
      result = range(size[index])
    else:
      result = range(coords[0][index], coords[0][index] + coords[1][index])
    if(isReversed):
      result = reversed(result)
    return result
  for thisPixel[0] in getRange(0):
    print(thisPixel[0])
    beforePixel = None
    handler(thisPixel[0], True)
    for thisPixel[1] in getRange(1):
      if beforePixel is not None:
        result = handler(beforePixel, thisPixel)
        if(isCompletedMark(result)):
          return result
      beforePixel = clone(thisPixel)
  return
  print("Loop")
  for thisPixel[0] in getRange(0):
    beforePixel = None
    handler(thisPixel[0], False)
    for thisPixel[1] in getRange(1, True):
      if beforePixel is not None:
        result = handler(beforePixel, thisPixel)
        if(isCompletedMark(result)):
          return result
      beforePixel = clone(thisPixel)
  thisPixel = [0, 0]
  for thisPixel[1] in getRange(1):
    beforePixel = None
    handler(True, thisPixel[1])
    for thisPixel[0] in getRange(0):
      if beforePixel is not None:
        result = handler(beforePixel, thisPixel)
        if(isCompletedMark(result)):
          return result
      beforePixel = clone(thisPixel)
  for thisPixel[1] in getRange(1):
    beforePixel = None
    handler(False, thisPixel[1])
    for thisPixel[0] in getRange(0, True):
      if beforePixel is not None:
        result = handler(beforePixel, thisPixel)
        if(isCompletedMark(result)):
          return result
      beforePixel = clone(thisPixel)
  """for x in range((-1) * size[1] + 1, size[1]):
    handler(x, True, True)
    thisPixel[0] = max([0, x])
    for thisPixel[1] in range(max([0, ])):
      if beforePixel is not None:
        if(isInRect(beforePixel, size) and isInRect(thisPixel, size)):
          handler(beforePixel, thisPixel)
      beforePixel = clone(thisPixel)
      thisPixel[1] += 1
      
  for y in range((-1) * size[1] + 1, size[1]):
    handler(y, True, True)
    thisPixel[1] = y
    for thisPixel[0] in range((- 1) * y, size[0] - abs(y) - y):
      if beforePixel is not None:
        if(isInRect(beforePixel, size) and isInRect(thisPixel, size)):
          handler(beforePixel, thisPixel)
      beforePixel = clone(thisPixel)
      thisPixel[1] += 1
  for y in range((-1) * size[1] + 1, size[1]):
    handler(y, False, False)
    thisPixel[1] = y + size[0] - abs(y) - y - 1
    for thisPixel[0] in range(size[0] - abs(y) - y - 1, (- 1) * y - 1, -1):
      if beforePixel is not None:
        if(isInRect(beforePixel, size) and isInRect(thisPixel, size)):
          handler(beforePixel, thisPixel)
      beforePixel = clone(thisPixel)
      thisPixel[1] -= 1
  for x in range((-1) * size[0] + 1, size[0]):
    handler(y, True, False)
    thisPixel[0] = x
    for thisPixel[0] in range((- 1) * y, size[0] - abs(y) - y):
      if beforePixel is not None:
        if(isInRect(beforePixel, size) and isInRect(thisPixel, size)):
           handler(beforePixel, thisPixel)
      beforePixel = clone(thisPixel)
      thisPixel[1] += 1
  """
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
def toNumericValueIfItIs(value):
  try:
    result = float(value)
  except:
    result = None
  return result
def isNumericValue(value):
  return isNotNone(toNumericValueIfItIs(value))
def getSign(value):
  if value == 0:
    return None
  else:
    return 1 if (value > 0) else -1
def haveAlmostOneSign(values, maxError):
  return haveOneSign(list(map(lambda value: value if (abs(value) > maxError) else 0, values)))
def haveOneSign(values):
  theSign = None
  for value in values:
    thisSign = getSign(value)
    if thisSign != None:
      if((theSign != None) and (thisSign != theSign)):
        return False
      theSign = thisSign
  return True
def allNoLessThan(values, value):
  for theValue in values:
    if(theValue < value):
      return False
  return True    
def allNoMoreThan(values, value):
  for theValue in values:
    if(theValue > value):
      return False
  return True
def divMaybeOnZero(value1, value2, maxValue):
  if value2 == 0:
    return maxValue
  else:
    return value1 / value2
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
def isLikable(value1, value2, maxError = None):
  if isUndefined(maxError):
    maxError = STANDARD_MAX_ERROR
  return abs(value1 - value2) <= maxError
def arrayGetSum(values):
  res = 0
  for val in values:
    res += val
  return res
def arrayDiff(value1, value2):
  result = []
  for index, value in enumerate(value1):
    result.append(value - value2[index])
  return result
def outForUser(value):
  return round(value, 2)
def getArrayReprValue(values, theType = None):
  if isUndefined(theType): 
    theType = "avg"
  result = None
  if(theType == "avg"):
    result = arrayGetAvg(values)
  elif theType == "max":
    result = max(values)
  elif theType == "min":
    result = min(values)
  return result
def arrayGetMaxDifference(values):
  return max(values) - min(values)
def arrayGetAvg(values):
  return arrayGetSum(values) / len(values)
def arrayIsLikable(values, maxError = None):
  avg = arrayGetAvg(values)
  for value in values:
    if not (isLikable(avg, value, maxError)):
      return False
  return True
def getPointSurrounding(point):
  result = []
  for diffX in range(-1, 2):
    for diffY in range(-1, 2):
      if((diffX != 0) or (diffY != 0)):
        result.append([point[0] + diffX, point[1] + diffY])
  return result
def getMultiRange(dim, theRange):
  result = []
  if(isArray(dim)):
    theRange, dim = dim, theRange
  if not isinstance(theRange, range):
    theRange = range(theRange[0], theRange[1] + 1)
  def getByDimensions(count):
    if count == 1:
      result = list(map(lambda value: [value], theRange))
    else:
      resultBefore = getByDimensions(count - 1)
      result = []
      for thisResult in resultBefore:
        for thisValue in theRange:
          result.append(clone(thisResult) + [thisValue])
    return result
  return getByDimensions(dim)