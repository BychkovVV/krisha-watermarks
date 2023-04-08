import math, copy, numpy, cv2
from sty import bg, ef, fg, rs
from common import canHaveProperties, MyCommonObject, MyArray
from functions import isUndefined, isDefined, isArray, isScalar, isNumeric, isString, die, clone, isNone, isLikable, isNotNone, toMyArray, toNumericValueIfItIs, isNumericValue, toIntegerValueIfItIs, isIntegerValue, toNaturalIntegerIfItIs, isNaturalInteger, divMaybeOnZero, haveOneSign, haveAlmostOneSign, arrayIsLikable, allNoLessThan, allNoMoreThan, arrayGetAvg, arrayGetMaxDifference, outForUser, arrayDiff, getMultiRange
from arrays import ArrayWithNaturalKeys, MyArrayList, MyArrayListNumeric, MyNumericArray, MyArrayDictionary, MyArrayTuple, MyArraySet
from constants import IS_DEBUGGING, COEFFICIENTS_COMPARING_MAX_ERROR, MIN_WATERMARK_VALUE, MAX_WATERMARK_VALUE, WATERMARK_COEFFICIENT_MAX_DIFFERENCE_WITH_AVG, WATERMARK_COEFFICIENT_MAX_DIFFERENCE_IN_PIXELS, OUTPUT_TO_CONSOLE, COLOR_DIFFERENCE_MAX_ERROR_OF_THE_ONE_SIGN_CHECK_TO_DETECT_WATERMARK
from functools import partial
class PointsCache(dict):
  def getAll(this):
    result = []
    for element in this.keys():
      result.append(type(this).getPoint(element))
    return result
  def isIn(this, point):
    key = type(this).getKey(point)
    return key in this
    try:
      this.index(key)
      return True
    except:
      return False
  def addIfNotIsIn(this, point):
    key = type(this).getKey(point)
    result = key not in this
    if result:
      this[key] = True
    return result
PointsCache.KEY_SEPARATOR = ', '
def getKeyByPoint(point):
  return PointsCache.KEY_SEPARATOR.join(map(str, point))  
def getPointByKey(key):
  return list(map(toNaturalIntegerIfItIs, key.split(PointsCache.KEY_SEPARATOR)))
PointsCache.getKey = getKeyByPoint
PointsCache.getPoint = getPointByKey
def to3dTuple(value):
  if(not (isinstance(value, tuple) or isinstance(value, list))):
    value = (value, value, value)
  return value
def getCoefficientByColorValue(waterMarkValue, oldColor, newColor):
  return abs(newColor - waterMarkValue) / abs(oldColor - waterMarkValue)
def getCoefficient(watermarkColor, oldColor, newColor):
  return waterMarkValue.absdiff(newColor) / waterMarkValue.absdiff(oldColor)
class Watermark(object):
  def __add__(this, other):
    newColor = []
    newCoefs = []
    for index in range(3):
      newColor.append(int((float(this.color[index]) + float(other.color[index])) / 2))
    for index, theCoef in enumerate(this.coefficients):
      newCoefs.append((theCoef + other.coefficients[index]) / 2)
    return Watermark(newColor, newCoefs)
  def __iadd__(this, other):
    newCoefs = []
    this.color = Color.getAvg(this.color, other.color)
    for index, theCoef in enumerate(this.coefficients):
      this.coefficients[index] = (theCoef + other.coefficients[index]) / 2
    return this
  def __mul__(this, other):
    newColor = []
    newCoefs = []
    for index in range(3):
      newColor.append(int((float(this.color[index]) + float(other.color[index])) / 2))
    for index, theCoef in enumerate(this.coefficients):
      newCoefs.append(theCoef * other.coefficients[index])
    return Watermark(newColor, newCoefs)
  def __imul__(this, other):
    newCoefs = []
    print(this.color)
    newColor = []
    this.color = Color.getAvg(this.color, other.color)
    for index, theCoef in enumerate(this.coefficients):
      #print("this.coefficients[{}] ({}) *= other.coefficients[{}] ({}) = {}".format(index, this.coefficients[index], index, other.coefficients[index], this.coefficients[index] * other.coefficients[index]))
      this.coefficients[index] *= other.coefficients[index]
    return this
  def isLikeZero(this):
    return allNoMoreThan(this.coefficients, 1) and not allNoMoreThan(this.coefficients, 1 - 0.01)
  def decode(this, color):
    result = []
    for index in range(3):   
      result.append(int((float(color[index]) - (1 - this.coefficients[index]) * float(this.color[index])) / float(this.coefficients[index])))
    return Color.get(result)
  def getColorIndex(this):
    return + this.isWhite()
  def isWhite(this):
    return (this.color[0] == 255) and (this.color[1] == 255) and (this.color[2] == 255)
  def getCoefs(this):
    result = []
    for value in this.coefficients:
      result.append(1 - value)
    return result
  def isAnti(this, other):
    for index in range(3):
      if(int(this.color[index]) != (255 - int(other.color[index]))):
        return False
    return True
  def getAvgCoef(this):
    return arrayGetAvg(this.getCoefs())
  def getMaxDifference(this):
    return arrayGetMaxDifference(this.getCoefs())
  def isLike(this, other):
    return this.color.isEqual(other.color) and isLikable(arrayGetAvg(this.coefficients), arrayGetAvg(other.coefficients), COEFFICIENTS_COMPARING_MAX_ERROR)
  def __repr__(this):
    if this.inDetail:
      result = "Watermark (Color: {}, coefficients: {})".format(this.color, this.getCoefs())
    else:
      result = "Watermark (Color: {}, avg coef: {}, max diff: {}".format("black" if this.color.isBlack() else "white", outForUser(this.getAvgCoef()), outForUser(this.getMaxDifference()))
      if isDefined(this.source):
        result += ', max col diff: {}'.format(arrayGetMaxDifference(arrayDiff(this.source[0].getValues(), this.source[1].getValues())))
      result += ')'
    return result
  def __init__(this, color, coefficients, byColors = None):    
    this.inDetail = False
    this.color = Color.get(color)
    this.coefficients = coefficients
    if isDefined(byColors):
      this.source = byColors
    else:
      this.source = None
def debugLog(*values, **params):
  if IS_DEBUGGING:
    print(*values, **params)
class Debug(object):
  pass
Debug.log = debugLog
def detectWatermark(oldColor, newColor, haveToBeWhite = None):
  black = []
  white = []
  absDiff = []
  whiteAbs = []
  for index in range(3):
    black.append(divMaybeOnZero(newColor[index], oldColor[index], 1))
    white.append(divMaybeOnZero(255 - newColor[index], 255 - oldColor[index], 1))
    absDiff.append(int(newColor[index]) - int(oldColor[index]))
  result = None
  #print("Detection, white: {}, black: {}, haveToBeWhite: {}, absDiff: {}, haveOneSign: {}, MAX_WATERMARK_VALUE: {}, allNoLessThan(white, 1 - MAX_WATERMARK_VALUE): {}, MIN_WATERMARK_VALUE: {}, allNoMoreThan(white, 1 - MIN_WATERMARK_VALUE): {}, arrayIsLikable(white, WATERMARK_COEFFICIENT_MAX_DIFFERENCE_WITH_AVG): {}".format(white, black, haveToBeWhite, absDiff, haveOneSign(absDiff), MAX_WATERMARK_VALUE, allNoLessThan(white, 1 - MAX_WATERMARK_VALUE), MIN_WATERMARK_VALUE, allNoMoreThan(white, 1 - MIN_WATERMARK_VALUE), arrayIsLikable(white, WATERMARK_COEFFICIENT_MAX_DIFFERENCE_WITH_AVG)))
  if(haveAlmostOneSign(absDiff, COLOR_DIFFERENCE_MAX_ERROR_OF_THE_ONE_SIGN_CHECK_TO_DETECT_WATERMARK)):
    if allNoLessThan(white, 1 - MAX_WATERMARK_VALUE) and ((haveToBeWhite == True) or allNoMoreThan(white, 1 - MIN_WATERMARK_VALUE)) and ((haveToBeWhite == True) or (haveToBeWhite != False) and allNoMoreThan(white, 1)) and arrayIsLikable(white, WATERMARK_COEFFICIENT_MAX_DIFFERENCE_WITH_AVG):
      result = Watermark(255, white, [oldColor, newColor])
    elif allNoLessThan(black, 1 - MAX_WATERMARK_VALUE) and ((haveToBeWhite == False) or allNoMoreThan(black, 1 - MIN_WATERMARK_VALUE)) and ((haveToBeWhite == False) or (haveToBeWhite != True) and allNoMoreThan(black, 1)) and arrayIsLikable(black, WATERMARK_COEFFICIENT_MAX_DIFFERENCE_WITH_AVG):
      result = Watermark(0, black, [oldColor, newColor])
  return result
def getWatermarkByMax(watermarks):
  sumColors = ([], [], [])
  sumCoefs = ([], [], [])
  theRangeOf3 = range(3)
  for watermark in watermarks:
    for index in theRangeOf3:
      sumColors[index].append(watermark.color[index])
      sumCoefs[index].append(watermark.coefficients[index])
  color = []
  coef = []
  for index in theRangeOf3:
    color.append(arrayGetAvg(sumColors[index]))
    coef.append(min(sumCoefs[index]))
  return Watermark(color, coef)
def getWatermarkByAvg(watermarks):
  sumColors = ([], [], [])
  sumCoefs = ([], [], [])
  theRangeOf3 = range(3)
  for watermark in watermarks:
    for index in theRangeOf3:
      sumColors[index].append(watermark.color[index])
      sumCoefs[index].append(watermark.coefficients[index])
  color = []
  coef = []
  for index in theRangeOf3:
    color.append(arrayGetAvg(sumColors[index]))
    coef.append(arrayGetAvg(sumCoefs[index]))
  return Watermark(color, coef)
Watermark.detect = detectWatermark
Watermark.getByMax = getWatermarkByMax
Watermark.getByAvg = getWatermarkByAvg
class Image(MyArrayDictionary):
  def processPairs(this, handler, intervals = None):
    if isUndefined(size):
      intervals = list(map(lambda value: [0, value - 1], this.getSize()))
    theXRange = range(intervals[0][0], intervals[0][1] + 1)
    theYRange = range(intervals[1][0], intervals[1][1] + 1)
    def getByPoint(coordinate):
      return [coordinate, this.getColor(coordinate)]
    directionStep = 1
    for x in theXRange:
      thePrev = [None, None]
      theNext = getByPoint(Coordiate([x, theYRange.start]))
      theNext = getByPoint(Coordiate([x, theYRange.start + directionStep]))     
      for y in theYRange:
        thePrev[0] = Coordinate[]
        theCurrent[0][1] += directionStep
        theNext[0][1] += directionStep
    for y in theYRange:
      thePrev = [None, None]
      theNext = getByPoint(Coordiate([theYRange.start, y]))
      theNext = getByPoint(Coordiate([x, theYRange.start + directionStep]))     
      for x in theXRange:
        thePrev[0] = Coordinate[]
        theCurrent[0][1] += directionStep
        theNext[0][1] += directionStep
    
  def getCountours(this):
    
  def detectElement(start, coef, detector):
    theStart = clone(start)
    theIterator = LineIterator(start, coef)
    for point in theIterator:
      if detector(point):
        result = point
        break
    return result
  def __init__(this, path):
    with open(path, 'rb') as stream:
      bytes = bytearray(stream.read())
      array = numpy.asarray(bytes, dtype=numpy.uint8)
      this.inColor = cv2.imdecode(array, cv2.IMREAD_COLOR)
      this.wasPixels = []
  def getWidth(this):
    return this.getSize()[0]
  def getHeight(this):
    return this.getSize()[1]
  def getSize(this):
    return [this.inColor.shape[1], this.inColor.shape[0]]
  def undoLast(this, theCount):
    last = clone(this.wasPixels[- theCount:])
    for el in last:
      this.inColor[el[0][1]][el[0][0]] = el[1][::-1]
    this.wasPixels = this.wasPixels[0:- theCount]
  def has(this, coordinate):
    return (coordinate[0] >= 0) and (coordinate[0] < this.getWidth()) and (coordinate[1] >= 0) and (coordinate[1] < this.getHeight())
  def getColor(this, pixel):
    return Color(this.inColor[pixel[1]][pixel[0]][::-1])
  def setColor(this, pixel, color):
    pixels = Coordinates.convertTo(pixel)
    for index, pixel in pixels.getValues():
      this.wasPixels.append([pixel, this.getColor(pixel)])
      this.inColor[pixel[1]][pixel[0]] = color[::-1]
  def save(this, path):    
    _, array = cv2.imencode('.jpeg', this.inColor)
    with open(path, 'wb') as fp:
      fp.write(bytes(array))
class Pixel(MyArraySet):
  pass
def getPixel(value):
  return Pixel(value)
def getAvgColor(old, new):
  result = []
  for index in range(3):
    result.append(int((float(old[index]) + float(new[index])) / 2))
  return Color(result)
class Color(MyArrayList):
  def getValues(this):
    return [this[0], this[1], this[2]]
  def isEqual(this, other):
    return (this[0] == other[0]) and (this[1] == other[1]) and (this[2] == other[2])
  def isBlack(this):
    return (this[0] == 0) and (this[1] == 0) and (this[2] == 0)
  def __repr__(this):
    if OUTPUT_TO_CONSOLE:
      prefix = fg(this[0], this[1], this[2])
      postfix = fg.rs
    else:
      prefix = postfix = ''
    return prefix + "RGB({}, {}, {})".format(this[0], this[1], this[2]) + postfix
    #return fg(this[0], this[1], this[2]) + "RGB({}, {}, {})".format(this[0], this[1], this[2]) + fg.rs
Color.getAvg = getAvgColor
def getColor(parameter):
  if type(parameter) == bool:
    parameter = 255 if parameter else 0
  return Color(to3dTuple(parameter))
class Coordinates(object):
  pass
class CoordinatesSet(Coordinates, MyArraySet):
  def __init__(this, values = None):
    if(isArray(values) and isScalar(values[0])):
      print('is Array')
      values = [values]
    values = list(map(lambda value: value if isinstance(value, Coordinate) else Coordinate(value), values))
    #print('values', type(values[0]))
    #set(this).__init__(values)
    print('Before calling MyArray (251)')
    this.theId = 333
    MyArray.__init__(this, values)
    #MyArray.__init__(this, values)
    #print('Count: {}'.format(len(this)))
    for el in this:
      print('El: {}'.format(el))
    return None
class CoordinatesSequence(Coordinates, MyArrayList):
  def __init__(this, values = None):
    if(isArray(values) and isScalar(values[0])):
      values = [values]
    values2 = list(map(lambda value: value if isinstance(value, Coordinate) else Coordinate(value), values))
    #print(str(values2[0]))
    #list(this).__init__(values)
    MyArray.__init__(this, values)
    print('Count in: {}'.format(len(this)))
    for el in this:
      print('El: {}'.format(el))
def toCoordinates(value):
  if(isinstance(value, Coordinate)):
    result = CoordinateSet([value])
  elif(isinstance(value, Coordinates)):
    result = value
  else:
    result = CoordinateSet()
  return result
Coordinates.convertTo = toCoordinates
Color.get = getColor
class Coordinate(MyArrayListNumeric):
  def getNearestSurrounding(this, withDiagonals = True):
    result = []
    for coordOffsets in getMultiRange([-1, 1], len(this)):
      if any(map(lambda value: value != 0, coordOffsets)) and (withDiagonals or any(map(lambda value: value == 0, coordOffsets))):
        result.append(this + coordOffsets)     
    return CoordinatesSet(result)
  def __str__(this):
    result = '['
    firstValue = ord('x')
    values = []
    for index, value in this:
      values.append(str(value))
    result = ']'
    return '[' + ', '.join(values) + ']'
  def __float__(this):
    result = 0
    for index, value in this:
      result += value ** 2
    return result ** 0.5
  def __repr__(this):
    result = '['
    firstValue = ord('x')
    values = []
    for index, value in this:
      values.append('{}: {}'.format(chr(firstValue + index), value))
    result = ']'
    return '[' + ', '.join(values) + ']'
  def __hash__(this):
    return this[0] + this[1] * type(this).MAX_WIDTH
  def __eq__(this, other):
    return this.__hash__() == other.__hash__()
Coordinate.MAX_WIDTH = 10000
class ArrayProcessingException(Exception):
  pass
class LineIterator(CoordinatesSequence):
  def __init__(this, start, angle, maxLength):
    #this.angle = (angle / 180) * math.pi
    this.angle = angle
    at = math.atan(this.angle)
    this.offsets = Coordinate([math.cos(at), math.sin(at)])
    this.offsetLength = this.offsets.length()
    this.startPoint = Coordinate(start)
    this.currentPoint = None
    this.currentOffset = 0
    this.currentLength = 0
    this.length = 0
    this.maxLength = maxLength
  def __iter__(this):
    return this
  def __next__(this):
    if isUndefined(this.currentPoint):
      this.currentPoint = this.startPoint
    else:
      this.currentPoint += this.offsets
      this.length += this.offsetLength
    if this.length > this.maxLength:
      raise StopIteration
      result = None
    else:
      result = round(this.currentPoint)
    return result
def isBetter(this, was, isMax = False):
  return True if isUndefined(was) else ((this > was) if isMax else (this < was))
class Area(object):
  def getBounds(this):
    result = [[None, None], [None, None]]
    def compareByIndex(coord, index):
      if(isBetter(coord[index], result[index][0], False)):
        result[index][0] = coord[index]
      if(isBetter(coord[index], result[index][1], True)):
        result[index][1] = coord[index]      
    for coord in this.value:
      for thisIndex in range(2):
        compareByIndex(coord, thisIndex)
    return result
  def add(this, value):
    return this.value.add(value)
  def __repr__(this):
    return "Area (length: {}, ".format(len(this.value)) + repr(this.value) + ")";
  def __contains__(this, key):
    return key in this.value
  def __init__(this, value = None):
    if isDefined(value):
      this.value = set(value)
