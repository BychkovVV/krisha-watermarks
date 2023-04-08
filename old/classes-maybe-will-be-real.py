import copy, numpy, cv2
from functions import die, clone, isNone, isLikable, isNotNone, isDefined, canHaveProperties, toMyArray, toNumericValueIfItIs, isNumericValue, toIntegerValueIfItIs, isIntegerValue, toNaturalIntegerIfItIs, isNaturalInteger, divMaybeOnZero, haveOneSign, arrayIsLikable, allNoLessThan, allNoMoreThan, arrayGetAvg
from common import MyCommonObject
from arrays import MyArray, ArrayWithNaturalKeys, MyArrayList, MyNumericArray, MyArrayDictionary, MyArrayTuple, MyArraySet
from constants import IS_DEBUGGING, COEFFICIENTS_COMPARING_MAX_ERROR, MAX_WATERMARK_VALUE, WATERMARK_COEFFICIENT_MAX_DIFFERENCE_WITH_AVG, WATERMARK_COEFFICIENT_MAX_DIFFERENCE_IN_PIXELS
def to3dTuple(value):
  if(not isinstance(value, tuple)):
    value = (value, value, value)
  return value
def getCoefficientByColorValue(waterMarkValue, oldColor, newColor):
  return abs(newColor - waterMarkValue) / abs(oldColor - waterMarkValue)
def getCoefficient(watermarkColor, oldColor, newColor):
  return waterMarkValue.absdiff(newColor) / waterMarkValue.absdiff(oldColor)
class Watermark(object):
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
  def isLike(this, other):
    return this.color.isEqual(other.color) and isLikable(arrayGetAvg(this.coefficients), arrayGetAvg(other.coefficients), COEFFICIENTS_COMPARING_MAX_ERROR)
  def __repr__(this):
    return "Watermark (Color: {}, coefficients: {})".format(this. color, this.coefficients)
  def __init__(this, color, coefficients):    
    this.color = Color.get(color)
    this.coefficients = coefficients
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
  Debug.log("White: {}, black: {}".format(white, black))
  if(haveOneSign(absDiff)):
    if allNoLessThan(white, 1 - MAX_WATERMARK_VALUE) and ((haveToBeWhite == True) or (haveToBeWhite != False) and allNoMoreThan(white, 1)) and arrayIsLikable(white, WATERMARK_COEFFICIENT_MAX_DIFFERENCE_WITH_AVG):
      result = Watermark(255, white)
    elif allNoLessThan(black, 1 - MAX_WATERMARK_VALUE) and ((haveToBeWhite == False) or (haveToBeWhite != True) and allNoMoreThan(black, 1)) and arrayIsLikable(black, WATERMARK_COEFFICIENT_MAX_DIFFERENCE_WITH_AVG):
      result = Watermark(0, black)
  return result
Watermark.detect = detectWatermark
class Image(MyArrayDictionary):
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
  def getColor(this, pixel):
    return Color(this.inColor[pixel[1]][pixel[0]][::-1])
  def setColor(this, pixel, color):
    this.wasPixels.append([pixel, this.getColor(pixel)])
    this.inColor[pixel[1]][pixel[0]] = color[::-1]
  def save(this, path):    
    _, array = cv2.imencode('.jpeg', this.inColor)
    with open(path, 'wb') as fp:
      fp.write(bytes(array))
class Pixel(MyArrayTuple):
  pass
def getPixel(value):
  return Pixel(value)
class Color(MyArrayTuple):
  def isEqual(this, other):
    return (this[0] == other[0]) and (this[1] == other[1]) and (this[2] == other[2])
  def isBlack(this):
    return (this[0] == 0) and (this[1] == 0) and (this[2] == 0)
def getColor(parameter):
  if type(parameter) == bool:
    parameter = 255 if parameter else 0
  return Color(to3dTuple(parameter))
Color.get = getColor
class Coordinate(MyArrayList):
  def __hash__(this):
    return this.values[0] + this.values[1] * type(this).MAX_WIDTH
  def __eq__(this, other):
    return this.__hash__() == other.__hash__()
Coordinate.MAX_WIDTH = 10000
class Area(MyArraySet):
  pass