import math, copy, numpy, cv2, os, sys
from constants import IS_DEBUGGING, MAX_WATERMARK_VALUE, MIN_COEFICIENT_DIFFERENCE_WITH_ONE_TO_DETECT, MIN_WATERMARK_VALUE_FOR_DETECTION, MIN_WATERMARK_VALUE_FOR_DETECTION_GETTER, MAX_COUNT_OF_PIXELS_FOR_DETECT, MIN_WATERMARK_SIZE, MAX_WATERMARK_SIZE, MIN_LETTER_SIZE
from classes import Coordinate, Pixel, Color, Image, Watermark, Debug, Area, PointsCache
from functions import die, isLikable, arrayIsLikable, haveOneSign, divMaybeOnZero, eachPixelsPair, isUndefined, isDefined, arrayGetAvg, getArrayReprValue, allNoLessThan, clone, arrayDiff, getPointSurrounding, isBetter, purgeFolder, printDebug, outDebug, logThis, haveAlmostOneSign, outForUser, detectColorDifferenceFast, isNotEmptyColorDifference
from arrays import MyArrayListNumeric
import cv2
import cProfile
import pstats
import io
from pstats import SortKey
from datetime import datetime
from threading import Timer
ob = cProfile.Profile()
ob.enable()
LINES_OF_THE_LETTER = {'krisha.kz': [[[0, 0], 35], [[27, 9], 26], [[47, 9], 26], [[85, 0], 35]], 'krisha-logo': [[[0, 33], 37], [[37, 31], 39], [[72, 33], 37]]}
def outStatus():
  global theTimer
  ob.disable()
  now = datetime.now()
  path = 'C:\\Работа\\Александр Болтенков\\Водяные знаки\\wrservice-main\\tests\\pythoncode-tutorials\\machine-learning\\shape-detection\\profiling\\status-cumulative-time-{}-{}-{}.txt'.format(int(now.hour), int(now.minute), int(now.second))
  with open(path, 'w') as stream:
    sec = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(ob, stream = stream).sort_stats(sortby)
    ps.print_stats()
  path = 'C:\\Работа\\Александр Болтенков\\Водяные знаки\\wrservice-main\\tests\\pythoncode-tutorials\\machine-learning\\shape-detection\\profiling\\status-time-{}-{}-{}.txt'.format(int(now.hour), int(now.minute), int(now.second))
  with open(path, 'w') as stream:
    sec = io.StringIO()
    sortby = SortKey.TIME
    ps = pstats.Stats(ob, stream = stream).sort_stats(sortby)
    ps.print_stats()  
  #ps.dump_stats('C:\\Работа\\Александр Болтенков\\Водяные знаки\\wrservice-main\\tests\\pythoncode-tutorials\\machine-learning\\shape-detection\\profiling\\status-{}-{}-{}.txt'.format(int(now.hour), int(now.minute), int(now.second)))
  ob.enable()
  theTimer = Timer(30, outStatus)
  theTimer.start()
theTimer = Timer(30, outStatus)
theTimer.start()  
  
#Timer(30.0, )
#purgeFolder('C:\\Работа\\Александр Болтенков\\Водяные знаки\\wrservice-main\\tests\\pythoncode-tutorials\\machine-learning\\shape-detection\\logs')
def endProfiling():
  ob.disable()
  sec = io.StringIO()
  sortby = SortKey.CUMULATIVE
  ps = pstats.Stats(ob, stream=sec).sort_stats(sortby)
  ps.print_stats()
  print(sec.getvalue())
  die()
Debug.log(Watermark.detect([48, 63, 60], [118, 133, 130]))
Debug.log(Watermark.detect([120, 120, 120], [150, 150, 150]))
Debug.log(divMaybeOnZero(2, 0, 10))
byLetters = {}
GET_ALL_FIGURE = True
area = Area([Coordinate([0, 0])])
area.add(Coordinate([0, 0]))
def getProbableMeasuresCountByLetter(letterData, size = None):
  if type(letterData) == str:
    letterData = getLetterPoints(letterData, size)
  theWidth = letterData.shape[1]
  theHeight = letterData.shape[0]
  result = 0
  for x in range(theWidth):
    wasIn = False    
    willIn = letterData[0][x] == 1    
    for y in range(theHeight):
      isIn = willIn
      willIn = False if (y == (theHeight - 1)) else (letterData[y + 1][x] == 1)
      if isIn:
        if not wasIn:
          result += 1
        if not willIn:
          result += 1
      wasIn = isIn
  for y in range(theHeight):
    wasIn = False    
    willIn = (letterData[y][0] == 1)    
    for x in range(theWidth):
      isIn = willIn
      willIn = False if (x == (theWidth - 1)) else (letterData[y][x + 1] == 1)
      if isIn:
        if not wasIn:
          result += 1
        if not willIn:
          result += 1
      wasIn = isIn
  return result
class MyLetterPoints(numpy.ndarray):
  measuringsCount = None
  def __new__(cls, value):
    return super().__new__(cls, value.shape, value.dtype, value.data)
def getLetterPoints(letter, size = None, dimensionIndex = 1):
  global GET_ALL_FIGURE, byLetters
  if letter not in byLetters:
    image = cv2.cvtColor(Image("C:\\Работа\\Александр Болтенков\\Водяные знаки\\wrservice-main\\tests\\pythoncode-tutorials\\machine-learning\\shape-detection\\images\\letters\\" + str(letter) + ".png").inColor, cv2.COLOR_BGR2GRAY)
    result = numpy.zeros_like(image)
    width = image.shape[1]
    height = image.shape[0]
    theSum = 0
    for x in range(width):
      wasIn = None    
      for y in range(height):
        isIn = (image[y][x] == 0)
        willIn = None if (y == (height - 1)) else (image[y + 1][x] == 0)
        #print("point: {}, wasIn: {}, isIn: {}, willIn: {}".format((x, y), wasIn, isIn, willIn))
        if isIn and (GET_ALL_FIGURE or ((not (GET_ALL_FIGURE)) and ((wasIn != isIn) or (willIn != isIn)))):
          result[y][x] = 1
          if wasIn != True:
            theSum += 1
          if willIn != True:
            theSum += 1
        wasIn = isIn
    for y in range(height):
      wasIn = None    
      for x in range(width):
        isIn = (image[y][x] == 0)
        willIn = None if (x == (width - 1)) else (image[y][x + 1] == 0)
        #print("point: {}, wasIn: {}, isIn: {}, willIn: {}".format((x, y), wasIn, isIn, willIn))
        if isIn and (GET_ALL_FIGURE or ((not (GET_ALL_FIGURE)) and ((wasIn != isIn) or (willIn != isIn)))):
          result[y][x] = 1
          if wasIn != True:
            theSum += 1
          if willIn != True:
            theSum += 1
        wasIn = isIn     
    byLetters[letter] = result
  result = clone(byLetters[letter])
  if(isDefined(size)):
    coef = size / result.shape[(dimensionIndex == 0) if 1 else 0]
    result = cv2.resize(result, (int(result.shape[1] * coef), int(result.shape[0] * coef)))
  result = MyLetterPoints(result)
  return result
PATH_TO_THE_IMAGE_PARTS = ["images/watermarked/6", ".jpg"]
PATHS_TO_THE_IMAGES = [sys.argv[1], sys.argv[2]] if (len(sys.argv) >= 3) else ["".join(PATH_TO_THE_IMAGE_PARTS), "-processed".join(PATH_TO_THE_IMAGE_PARTS)]

img = Image(PATHS_TO_THE_IMAGES[0])
newImg = Image(PATHS_TO_THE_IMAGES[0])
newImg.save(PATHS_TO_THE_IMAGES[1])

Debug.log(img.getSize())
coef = None
coefBlack = [1, 1, 1]
coefWhite = [1, 1, 1]
coords = [[6, 0], [1, 33]] if IS_DEBUGGING else None
haveToBeWhite = None
countOfThis = 0
countOfLastRealThis = countOfRealThis = countOfLastNotRealThis = 0
IS_DEBUGGING = False
DEBUG_X_COORDINATE = 314
IS_DEBUGGING_DETAILS = False
SEARCH_ONLY_IN_INTERESTING_RECTANGLE = IS_DEBUGGING
#interestingRectangle = [[403, 376], [1, 27]]
#interestingRectangle = [[306, 230], [5, 16]]
interestingRectangle = [[30, 43], [1, 43]]
#interestingRectangle = [[30, 49], [1, 43]]
#interestingRectangle[1][1] += interestingRectangle[0][1] - 350
#interestingRectangle[0][1] = 350
def resetDetector():
  global coefBlack, coefWhite, haveToBeWhite, countOfThis, countOfRealThis, countOfLastRealThis, countOfLastNotRealThis
  for index in range(3):
    coefBlack[index] = 1
    coefWhite[index] = 1
  haveToBeWhite = None
  countOfThis = countOfRealThis = countOfLastRealThis = countOfLastNotRealThis = 0
def processThis(old, new):
  global coefBlack, coefWhite, haveToBeWhite, countOfThis, countOfRealThis, countOfLastRealThis, countOfLastNotRealThis
  if (type(old) == bool) or (type(new) == bool):
    resetDetector()
  else:
    oldColor = img.getColor(old)
    currentColor = img.getColor(new)
    Debug.log("Pixels: {} (Color: {}) - {} (Color: {})".format(old, oldColor, new, currentColor))
    Debug.log("For detection, haveToBeWhite: {}".format(haveToBeWhite))
    current = Watermark.detect(oldColor, currentColor, haveToBeWhite)
    undoCount = 0
    if(isDefined(current)):
      isBlack = current.color.isBlack()
      if(isBlack):
        coef = coefBlack
      else:
        coef = coefWhite
      Debug.log("Detected {}".format(current))
      coef[0] *= current.coefficients[0]
      coef[1] *= current.coefficients[1]
      coef[2] *= current.coefficients[2]
      theAvgValue = arrayGetAvg(coef)
      if not allNoLessThan(coef, 1 - MAX_WATERMARK_VALUE):
        undoCount = countOfThis - 1
      else:
        if(theAvgValue > 1 - MIN_COEFICIENT_DIFFERENCE_WITH_ONE_TO_DETECT):
          if isDefined(haveToBeWhite):
            haveToBeWhite = None
        elif isUndefined(haveToBeWhite):
          haveToBeWhite = not isBlack
          countOfThis = countOfRealThis = countOfLastRealThis = 0
        if isDefined(haveToBeWhite):
          countOfThis += 1
          if getArrayReprValue(coef, MIN_WATERMARK_VALUE_FOR_DETECTION_GETTER) <= 1 - MIN_WATERMARK_VALUE_FOR_DETECTION:
            countOfRealThis += 1
            countOfLastRealThis += 1
            countOfLastNotRealThis = 0
            if countOfLastRealThis > MAX_WATERMARK_SIZE[1]:
              undoCount = countOfThis - 1
          else:
            if countOfLastRealThis > 0 and countOfLastRealThis < MIN_WATERMARK_SIZE[1]:
              undoCount = countOfThis - 1
            countOfLastRealThis = 0
            countOfLastNotRealThis += 1
          if (countOfLastRealThis == 0) and (countOfLastNotRealThis > MAX_COUNT_OF_PIXELS_FOR_DETECT):
            undoCount = countOfThis - 1
        Debug.log("haveToBeWhite: {}".format(haveToBeWhite))
    else:
      Debug.log("Not detected")
    if undoCount > 0:
      newImg.undoLast(undoCount)
      resetDetector()
    Debug.log("White: {}, black: {}".format(coefWhite, coefBlack))
    avgCoef = min([arrayGetAvg(coefBlack), arrayGetAvg(coefWhite)])
    coef = min(MAX_WATERMARK_VALUE, 1 - avgCoef) / MAX_WATERMARK_VALUE
    newImg.setColor(new, [currentColor[0] * (1 - coef) + 255 * coef, currentColor[1], currentColor[2]])
class WatermarksDict(dict):
  def set(this, point, watermark):
    thePointStr = PointsCache.getKey(point)
    if thePointStr in this.keys():
      this[thePointStr] += watermark
    else:
      this[thePointStr] = watermark
  def undo(this):
    for thePointKey in this:
      thePoint = PointsCache.getPoint(thePointKey)
      newImg.setColor(thePoint, this[thePointKey].decode(img.getColor(thePoint)))
theDict = {}
def outDescriptions(x):
  if IS_DEBUGGING and (x == DEBUG_X_COORDINATE):
    thePointsAndValues = []
    def compare(element):
      return element['point'][1]
    for key in theDict:
      thisPoint = PointsCache.getPoint(key)
      if x == thisPoint[0]:
        thePointsAndValues.append({"point": thisPoint, "value": theDict[key]})
    thePointsAndValues.sort(key = compare)
    for element in thePointsAndValues:
      if isDefined(element['value']['watermark']):
        newColor = element['value']['watermark'].decode(img.getColor(element['point']))
        newImg.setColor(element['point'], newColor)
        newImg.save(PATHS_TO_THE_IMAGES[1])
      else:
        newColor = None
      print("Point \"{}\", watermark \"{}\", new color \"{}\": ".format(element['point'], element['value']['watermark'], newColor) + ", ".join(element['value']['strings']))
      #input()
def describe(point, string = None, watermark = None, theDict = theDict):
  if point[0] == DEBUG_X_COORDINATE:
    thePointAsString = PointsCache.getKey(point)
    if thePointAsString not in theDict.keys():
      theDict[thePointAsString] = {'strings': [], 'watermark': None}
    if isDefined(watermark):
      theDict[thePointAsString]['watermark'] = watermark
    if isDefined(string):
      theDict[thePointAsString]['strings'].append(string)
class MyPointsList(list):
  """def forEachPoint(this, handler):
    for x in range(this.coordinate[0], this.coordinate[0] + this.size[0]):
      for y in range(this.coordinate[1], this.coordinate[1] + this.size[1]):
        theResult = handler([x, y])
        if theResult == False:
          break
      if theResult == False:
        break
  """
  coordinate = None
  size = None
  def getClosestPointAndDistance(this, point):
    theValue = [None, None]
    for thePoint in this:
      currentValue = math.dist(thePoint, point)
      if isBetter(currentValue, theValue[1], False):
        theValue = [thePoint, currentValue]
    return theValue
  def getDistanceToPoint(this, point):
    return this.getClosestPointAndDistance(point)[1]
  def isIn(this, point):
    for thisPoint in this:
      if (point[0] == thisPoint[0]) and (point[1] == thisPoint[1]):
        return True
    return False
  def getOuterBorder(this):
    result = PointsCache()
    for element in this:
      surrounding = getPointSurrounding(element)
      for theSurroundingElement in surrounding:
        result.addIfNotIsIn(theSurroundingElement)
    return result.getAll()
  def getRanges(this, offset = 0):
    result = [[None, None], [None, None]]
    for thisPoint in this:
      for coordIndex, coordValue in enumerate(thisPoint):
        for isMore in range(0, 2):
          if isBetter(coordValue, result[coordIndex][isMore], isMore == 1):
            result[coordIndex][isMore] = coordValue
    return [range(result[0][0] - offset, result[0][1] + 1 + offset), range(result[1][0] - offset, result[1][1] + 1 + offset)]
  def forEachDiff(this, handler, offset = 0):
    theRanges = this.getRanges(offset)
    for x in theRanges[0]:
      haveToBeWhite = None
      theMarks = []
      thisMark = None
      prevPoint = None
      nextPoint = [x, theRanges[1][0]]
      print(theRanges[1])
      for y in theRanges[1]:
        thisPoint = nextPoint
        thisPointCloned = clone(thisPoint)
        if isDefined(thisPointCloned) and img.has(thisPointCloned) and isDefined(prevPoint) and img.has(prevPoint):
          theMark = Watermark.detect(img.getColor(prevPoint), img.getColor(thisPointCloned), None if isUndefined(thisMark) else thisMark.isWhite())
          #describe(thisPointCloned, "For points {} (Color: {}, distance: {}) - {} (Color: {}, distance: {}), detected: {}, previus: {}".format(prevPoint, img.getColor(prevPoint), this.getDistanceToPoint(prevPoint), thisPointCloned, img.getColor(thisPointCloned), this.getDistanceToPoint(thisPointCloned), theMark, thisMark))
          if IS_DEBUGGING:
            logThis("For points {} (Color: {}) - {} (Color: {}), watermark detected: {}, this mark: {}".format(prevPoint, img.getColor(prevPoint), thisPointCloned, img.getColor(thisPointCloned), theMark, thisMark), 'also')
          if isDefined(theMark) and isUndefined(thisMark) and ((theMark.getAvgCoef() < 0.01)):
            describe(thisPointCloned, "< {}, This watermark to zero".format(0.01))
            theMark = None
          if isDefined(theMark):
            if isUndefined(thisMark):
              thisMark = theMark
              describe(thisPointCloned, "Watermark before was undefined")
            else:
              describe(thisPointCloned, "Watermark before was {}".format(thisMark))
              thisMark *= theMark
              describe(thisPointCloned, "new mark: {}".format(thisMark))
              if thisMark.isLikeZero():
                describe(thisPointCloned, "new mark is like zero, so thisMark = None")
                thisMark = None
          """if IS_DEBUGGING and (x == 322):
            print("After multiplying, this mark is: {}".format(thisMark))
            input()
          """
          describe(thisPointCloned, "Setting {} to theMarks".format(thisMark))
          if isDefined(thisMark):
            if(thisMark.isLikeZero()):
              describe(thisPointCloned, "this mark is like zero, so thisMark = None")
              thisMark = None
            elif thisMark.getAvgCoef() < 0:
              thisMark = Watermark.detect(img.getColor(prevPoint), img.getColor(thisPointCloned))
              describe(thisPointCloned, "This mark is negative, getting current open-mindly, is: {}".format(thisMark))              
              """if IS_DEBUGGING and (x == 322):
                print("This mark is negative, getting current open-mindly, is: {}".format(thisMark))
              """
          else:
            thisMark = None
        theMarks.append(clone(thisMark))
        prevPoint = thisPoint
        nextPoint = [x, y + 1]
      stayOnlyThisIndexes = []
      startFrom = None
      startWhite = None
      wasEffectiveCount = 0
      thisPoint = [x, theRanges[1][0]]
      for theMarkIndex, theMark in enumerate(theMarks):
        if isDefined(theMark):
          thisWhite = theMark.isWhite()
          thisCurrentPoint = clone(thisPoint)
          describe(thisCurrentPoint, "the mark is defined \"{}\"".format(theMark))
          if theMark.getAvgCoef() > 0.15:
            wasEffectiveCount += 1
            describe(thisCurrentPoint, "This is effective point, new effective count = {}".format(wasEffectiveCount))
            for thisIndex in range(max([0, theMarkIndex - 5]), min(theMarkIndex + 6, len(theMarks))):
              try:
                stayOnlyThisIndexes.index(thisIndex)
              except:
                stayOnlyThisIndexes.append(thisIndex)
                describe([thisCurrentPoint[0], theRanges[1][0] + thisIndex], "This node fixed as stay only (as near {})".format(thisCurrentPoint))
        else:
          thisWhite = None
        if (startWhite != thisWhite):
          if isDefined(startWhite) and (wasEffectiveCount < 2):
            if IS_DEBUGGING:
              logThis("wasEffectiveCount = {}, from {} to {}".format(wasEffectiveCount, theRanges[1] + startFrom, theRanges[1] + theMarkIndex - 1), 'also')
              #input()
            for thisIndex in range(startFrom, theMarkIndex):
              describe([thisCurrentPoint[0], theRanges[1][0] + thisIndex], "Interval with this point (points from {} to {}) fixed as part of intervalwith effective watermarks count = {} and it\'s wetermark flag is removed".format([thisCurrentPoint[0], theRanges[1][0] + startFrom], [thisCurrentPoint[0], theRanges[1][0] + theMarkIndex - 1], wasEffectiveCount))
              theMarks[thisIndex] = None
          startFrom = theMarkIndex
          startWhite = thisWhite
          wasEffectiveCount = 0
        thisPoint[1] += 1
      for theMarkIndex, theMark in enumerate(theMarks):
        try:
          stayOnlyThisIndexes.index(theMarkIndex)
        except:
          theMarks[theMarkIndex] = None
      currentMarkIndex = 0
      thisMark = None
      prevPoint = None
      nextPoint = [x, theRanges[1][0]]
      for y in theRanges[1]:
        thisPoint = clone(nextPoint)
        if isDefined(prevPoint):
          theMark = theMarks[currentMarkIndex]
          describe(thisPoint, "MARK: {}".format(theMark))
          if isDefined(theMark) and (theMark.getAvgCoef() < 0.01):
            describe(thisPoint, "The mark {} with avg coefficient < {}, so, setting it to none".format(theMark, 0.01))
            theMark = None
          """if isDefined(theMark):
            if isUndefined(thisMark):
              thisMark = theMark
            else:
              thisMark *= theMark
            print(thisMark)
          """
          describe(thisPoint, watermark = theMark)
          handler([prevPoint, thisPoint], theMark)
          if isDefined(thisMark) and thisMark.isLikeZero():
            thisMark = None
        currentMarkIndex += 1
        prevPoint = thisPoint
        nextPoint = [x, y + 1]        
      outDescriptions(x)
    return
    for y in theRanges[1]:
      haveToBeWhite = None
      theMarks = []
      thisMark = None
      prevPoint = None
      nextPoint = [theRanges[0][0], y]
      for x in theRanges[0]:
        thisPoint = nextPoint
        if isDefined(prevPoint):
          theMark = Watermark.detect(img.getColor(prevPoint), img.getColor(thisPoint), None if isUndefined(thisMark) else thisMark.isWhite())
          #print("For points {} (Color: {}) - {} (Color: {}), watermark detected: {}, this mark: {}".format(prevPoint, img.getColor(prevPoint), thisPoint, img.getColor(thisPoint), theMark, thisMark))
          if isDefined(theMark) and isUndefined(thisMark) and ((theMark.getAvgCoef() < 0.03)):
            theMark = None
          if isDefined(theMark):
            if isUndefined(thisMark):
              thisMark = theMark
            else:
              thisMark *= theMark
          #print("After multiplying, this mark is: {}".format(thisMark))
          theMarks.append(clone(thisMark))
          if isDefined(thisMark) and thisMark.isLikeZero():
            thisMark = None
        prevPoint = thisPoint
        nextPoint = [x + 1, y]
      stayOnlyThisIndexes = []
      for theMarkIndex, theMark in enumerate(theMarks):
        if(isDefined(theMark) and (theMark.getAvgCoef() > 0.15)):
          for thisIndex in range(max([0, theMarkIndex - 5]), min(theMarkIndex + 6, len(theMarks))):
            try:
              stayOnlyThisIndexes.index(thisIndex)
            except:
              stayOnlyThisIndexes.append(thisIndex)
      for theMarkIndex, theMark in enumerate(theMarks):
        try:
          stayOnlyThisIndexes.index(theMarkIndex)
        except:
          theMarks[theMarkIndex] = None
      currentMarkIndex = 0
      thisMark = None
      prevPoint = None
      nextPoint = [theRanges[0][0], y]
      for x in theRanges[0]:
        thisPoint = nextPoint
        if isDefined(prevPoint):
          theMark = theMarks[currentMarkIndex]
          if isDefined(theMark) and (theMark.getAvgCoef() < 0.03):
            theMark = None
          """if isDefined(theMark):
            if isUndefined(thisMark):
              thisMark = theMark
            else:
              thisMark *= theMark
            print(thisMark)
          """
          handler([prevPoint, thisPoint], theMark)
          if isDefined(thisMark) and thisMark.isLikeZero():
            thisMark = None
          currentMarkIndex += 1
        prevPoint = thisPoint
        nextPoint = [x + 1, y]
    return
    for y in theRanges[1]:
      prevPoint = None
      nextPoint = [theRanges[0][0], y]
      thisMark = None
      haveToBeWhite = None
      for x in theRanges[0]:
         thisPoint = nextPoint
         if isDefined(prevPoint):
           theMark = Watermark.detect(img.getColor(prevPoint), img.getColor(thisPoint), None if isUndefined(thisMark) else thisMark.isWhite())
           if isDefined(theMark):
             if isUndefined(thisMark):
               thisMark = theMark
             else:
               thisMark *= theMark
           handler([prevPoint, thisPoint], thisMark)             
           if thisMark.isLikeZero():
             thisMark = None
         prevPoint = thisPoint
         nextPoint = [x + 1, y]  
  def getInnerWatermarksAndCoordinates(this, maxCount = 5):
    theWatermarksAndCoordinates = []
    for index in range(maxCount + 1):
      theWatermarksAndCoordinates.append([[[], []], PointsCache()])
    def processThis(thePoints = None, processedPointsAsString = None):
      if isUndefined(thePoints):
        for element in this.getOuterBorder():
          processThis([element])
      else:
        if isUndefined(processedPointsAsString):
          processedPointsAsString = PointsCache()
        theCurrentLevel = len(thePoints) - 1
        surr = getPointSurrounding(thePoints[theCurrentLevel])
        theCurrentLevel = min([maxCount, theCurrentLevel])
        for thePoint in surr:
          if(this.isIn(thePoint) and processedPointsAsString.addIfNotIsIn(thePoint)):
            theWatermarksAndCoordinates[theCurrentLevel][1].addIfNotIsIn(thePoint)
            theWatermark = Watermark.detect(img.getColor(thePoints[0]), img.getColor(thePoint))
            if(isDefined(theWatermark)):
              theWatermarksAndCoordinates[theCurrentLevel][0][theWatermark.getColorIndex()].append(theWatermark)
            theNewPoints = clone(thePoints) if isDefined(thePoints) else []
            theNewPoints.append(thePoint)
            processThis(theNewPoints, processedPointsAsString)
    processThis()
    for theWatermarkAndCoordinates in theWatermarksAndCoordinates:
      theWatermarks = theWatermarkAndCoordinates[0]
      (theWatermarks[0 if (len(theWatermarks[0]) > len(theWatermarks[1])) else 1][0]).inDetail = True
      theWatermarkAndCoordinates[0] = Watermark.getByMax(theWatermarks[0 if (len(theWatermarks[0]) > len(theWatermarks[1])) else 1])      
      theWatermarkAndCoordinates[1] = theWatermarkAndCoordinates[1].getAll()
    return theWatermarksAndCoordinates
  def unwatermark(this, maxCount = 5, watermark = None):
    theDict = WatermarksDict()
    def theHandler(points, mark):
      if isDefined(watermark) and isDefined(mark) and (watermark.isWhite() != mark.isWhite()) and (mark.getAvgCoef() >= 0.05):
        mark = None
      if isDefined(mark):
        theDict.set(points[1], mark)
        #newImg.setColor(points[1], theDict[PointsCache.getKey(points[1])].decode(img.getColor(points[1])))
        #newImg.save(PATHS_TO_THE_IMAGES[1])
        #print("Points = {} (color: {}) - {} (colors: {} - {}), water mark: {}".format(points[0], img.getColor(points[0]), points[1], img.getColor(points[1]), theDict[PointsCache.getKey(points[1])].decode(img.getColor(points[1])), theDict[PointsCache.getKey(points[1])]))
        #input()
    this.forEachDiff(theHandler, 2)
    theDict.undo()
    newImg.save(PATHS_TO_THE_IMAGES[1])
    """theWatermarksAndCoordinates = this.getInnerWatermarksAndCoordinates(maxCount)
    for theWatermarkAndCoordinates in theWatermarksAndCoordinates:
      theWatermark = theWatermarkAndCoordinates[0]
      for thePoint in theWatermarkAndCoordinates[1]:
        newImg.setColor(thePoint, theWatermark.decode(img.getColor(thePoint)))
    """
def getMatchesByLetters(coordinates, letters, size):
  result = []
  nextCoordinates = [clone(coordinates)]
  def getThisResultPosition(element):
    return element[1].coordinate[0]
  for letter in letters:
    if len(nextCoordinates) > 0:
      theCoordinates = clone(nextCoordinates)
    nextCoordinates = []
    xCoords = []
    for coord in theCoordinates:
      xCoords.append([coord[0][0], coord[0][1]])
    print("letter: {}, theCoordinates: {}".format(letter, xCoords))
    for coord in theCoordinates:
      toContinue = True
      while(toContinue):
        print("coord before = {}".format(coord))
        thisResult = isMatchesByLetter(coord, letter, size, theNameOfTheLetter = str(letter))
        print("coord after = {}".format(coord))
        if isDefined(thisResult):
          print("Match: {}, size: {}".format(thisResult[1].coordinate[0], thisResult[1].size[0]))
          thisResult[1].letter = str(letter)
          result.append(thisResult)
          positionDifference = thisResult[1].coordinate[0] + thisResult[1].size[0] - coord[0][0]
          theNewLeftWidth = thisResult[1].coordinate[0] - coord[0][0]
          theNewRightWidth = coord[0][0] + coord[0][1] - (thisResult[1].coordinate[0] + thisResult[1].size[0])
          if(theNewLeftWidth >= MIN_LETTER_SIZE[0]):
            thisCoord = clone(coord)
            thisCoord[0][0] = coord[0][0]
            thisCoord[0][1] = theNewLeftWidth
            nextCoordinates.append(thisCoord)
          if(theNewRightWidth >= MIN_LETTER_SIZE[0]):
            thisCoord = clone(coord)
            thisCoord[0][0] = thisResult[1].coordinate[0] + thisResult[1].size[0]
            thisCoord[0][1] = theNewRightWidth
            #nextCoordinates.append(thisCoord)          
          print("coord = {}".format(coord))
          if(coord[0][1] > positionDifference):
            coord[0][0] += positionDifference
            coord[0][1] -= positionDifference
          else:
            toContinue = False
        else:
          toContinue = False
      if(coord[0][1] >= MIN_LETTER_SIZE[0]):
        nextCoordinates.append(coord)
  result.sort(key = getThisResultPosition)
  letters = ''
  for element in result:
    letters += element[1].letter
  return (result, letters) 
theCache = dict()
def getMatchesByLine(coordinate, detectedHeight, letter):
  points = getLetterPoints(letter)
  letterLines = LINES_OF_THE_LETTER[letter]
  topCoordinate = clone(coordinate)
  topCoordinate[1] -= detectedHeight - 1
  printDebug("Searching for {}, initial coordinates: {}, height: {}, probable matches count: {}".format(letter, topCoordinate, detectedHeight, len(letterLines)))
  result = None
  for theLineParameters in letterLines:
    thisHeight = theLineParameters[1]
    coefficient = detectedHeight / thisHeight
    thisSize = coefficient * points.shape[0]
    currentTopLeft = clone(topCoordinate)
    currentTopLeft[0] -= coefficient * theLineParameters[0][0]
    currentTopLeft[1] -= coefficient * theLineParameters[0][1]
    currentTopLeft = list(map(lambda value: int(value), currentTopLeft))
    if (currentTopLeft[0] >= 0) and (currentTopLeft[1] >= 0) and (currentTopLeft[0] < img.getWidth()) and (currentTopLeft[1] < img.getHeight()):
      result = isMatchesByLetter(currentTopLeft, letter, thisSize)
    if(isDefined(result)):
      break
  return result
def isMatchesByLetter(coordinate, letter, size, rejectImmediatelyIfNotPassed = False, theNameOfTheLetter = None):
  global IS_DEBUGGING_DETAILS, countOfMoreThanMaxThreshold, theCache
  allPoints = PointsCache()
  if(isUndefined(theNameOfTheLetter)):
    theNameOfTheLetter = str(letter)
  if theNameOfTheLetter not in theCache:
    theCache[theNameOfTheLetter] = dict()
  if size not in theCache[theNameOfTheLetter]:
    theCache[theNameOfTheLetter][size] = dict()
    isNew = True
  else:
    isNew = False
  thisCache = theCache[theNameOfTheLetter][size]
  if isinstance(letter, numpy.ndarray):
    points = letter
    rejectImmediatelyIfNotPassed = size
  else:
    points = getLetterPoints(letter, size)  
  if isNew:
    for thisY, values in enumerate(points):
      for thisX, theValue in enumerate(values):
        key = PointsCache.getKey([thisX, thisY])
        thisCache[key] = (theValue > 0)          
  if isinstance(letter, list):
    for thisLetter in letter:
      result = isMatchesByLetter(coordinate, thisLetter, size, rejectImmediatelyIfNotPassed, theNameOfTheLetter = theNameOfTheLetter)
      if isDefined(result):
        result[1].letter = str(letter)
        return result
    return None
  if isinstance(coordinate[1], list):
    if isUndefined(points.measuringsCount):
      points.measuringsCount = getProbableMeasuresCountByLetter(points)
    for y in range(coordinate[1][0], coordinate[1][0] + coordinate[1][1]):
      thisCoordinate = [coordinate[0], y]
      #print("y: {}".format(y))
      result = isMatchesByLetter(thisCoordinate, points, True, theNameOfTheLetter = theNameOfTheLetter)
      #print("After y: {}".format(y))
      if isDefined(result):
        if isUndefined(result[1].coordinate):
          result[1].coordinate = thisCoordinate
        return result
    return None
  if isinstance(coordinate[0], list):
    if isUndefined(points.measuringsCount):
      points.measuringsCount = getProbableMeasuresCountByLetter(points)
    for x in range(coordinate[0][0], coordinate[0][0] + coordinate[0][1]):
      thisCoordinate = [x, coordinate[1]]
      #print("x: {}".format(x))
      result = isMatchesByLetter(thisCoordinate, points, True, theNameOfTheLetter = theNameOfTheLetter)
      if isDefined(result):
        if isUndefined(result[1].coordinate):
          result[1].coordinate = thisCoordinate
        return result
    return None  
  def getMaxmaxThreshold(theCount):
    return math.floor(float(theCount) / 4)
  def outValues(theMax = None):
    for thisIndex, thisElements in enumerate(votesAndColors):
      if (isUndefined(theMax) or (thisIndex != theMax[0])) and (len(thisElements) > 0):
        thisString = ("Undetected" if (thisIndex == 0) else ("black" if (thisIndex == 1) else "white")) + ' are: '
        for indexOfThisElement, element in enumerate(thisElements):
          if indexOfThisElement > 0:
            thisString += ', '
          thisString += '{} - {}'.format(element[1], element[2])
          if isDefined(element[0]):
            thisString += ' ({})'.format(element[0])
        printDebug(thisString)
  maxThreshold = None
  if rejectImmediatelyIfNotPassed:
    maxPoints = points.measuringsCount
    if isUndefined(maxPoints):
      maxPoints = getProbableMeasuresCountByLetter(letter)
    maxThreshold = getMaxmaxThreshold(maxPoints)
  countOfMoreThanMaxThreshold = None if isUndefined(maxThreshold) else 0
  countOfMoreThanMaxThreshold = None
  def isInPoint(coord):
    thisKey = PointsCache.getKey(coord)
    if thisKey in allPoints:
      result = True
    else:
      key = PointsCache.getKey([coord[0] - coordinate[0], coord[1] - coordinate[1]])
      if key in thisCache:
        result = thisCache[key]
      else:
        result = False if (isUndefined(coord) or (coord[0] < coordinate[0]) or (coord[0] >= coordinate[0] + points.shape[1]) or (coord[1] < coordinate[1]) or (coord[1] >= coordinate[1] + points.shape[0])) else points[coord[1] - coordinate[1]][coord[0] - coordinate[0]] > 0
        thisCache[key] = result
      if result:
        allPoints[thisKey] = True
    #if result:
    #  newImg.setColor(coord, [255, 0, 255])
    return result
  votesAndColors = [[], [], []]
  theCoefficients = [[0, 0], [0, 0]]
  undefinedCount = 0
  def addToDetects(point1, point2, undefinedCount = undefinedCount):
    global countOfMoreThanMaxThreshold
    if(img.has(point1) and img.has(point2)):
      watermark = Watermark.detect(img.getColor(point1), img.getColor(point2))
      if isDefined(watermark):
        theElement = theCoefficients[+ watermark.isWhite()]
        theElement[0] += watermark.getAvgCoef()
        theElement[1] += 1  
      else:
        undefinedCount += 1      
      if IS_DEBUGGING_DETAILS:
        printDebug("Detect of {} - {}, watermark is: {}".format(arrayDiff(point1, coordinate), arrayDiff(point2, coordinate), watermark))
      theIndex = 0 if isUndefined(watermark) else (1 + watermark.isWhite())
      votesAndColors[theIndex].append((watermark, clone(point1), clone(point2)))
      """if isDefined(maxThreshold) and len(votesAndColors[theIndex]) == maxThreshold:
        countOfMoreThanMaxThreshold += 1
      """
  #print("330: coordinate: {}".format(coordinate))
  printDebug('Search for matching of letter "{}" in range: [{} - {} (Width: {}), {} - {} (Height: {})]'.format(letter, coordinate[0], coordinate[0] + points.shape[1] - 1, points.shape[1], coordinate[1], coordinate[1] + points.shape[0] - 1, points.shape[0]))
  if IS_DEBUGGING_DETAILS:
    printDebug("Loop x, than y: ")
  for x in range(coordinate[0], coordinate[0] + points.shape[1]):
    oldPoint = [x, coordinate[1] - 1]
    oldIn = isInPoint(oldPoint)
    newPoint = [x, coordinate[1]]
    newIn = isInPoint(newPoint)
    for y in range(coordinate[1], coordinate[1] + points.shape[0]):
      thisPoint = newPoint
      isIn = newIn
      newPoint = [x + 1, y]
      newIn = isInPoint(newPoint)
      if isIn:
        if not oldIn:
          addToDetects(oldPoint, thisPoint)
          if isDefined(countOfMoreThanMaxThreshold) and (countOfMoreThanMaxThreshold > 1):
            outValues()
            return None
        if not newIn:
          addToDetects(newPoint, thisPoint)
          if isDefined(countOfMoreThanMaxThreshold) and (countOfMoreThanMaxThreshold > 1):
            outValues()
            return None
      oldPoint = thisPoint
      oldIn = isIn
  if IS_DEBUGGING_DETAILS:
    printDebug("Loop y, than x: ")
  for y in range(coordinate[1], coordinate[1] + points.shape[0]):
    oldPoint = [coordinate[0] - 1, y]
    oldIn = isInPoint(oldPoint)
    newPoint = [coordinate[0], y]
    newIn = isInPoint(newPoint)
    for x in range(coordinate[0], coordinate[0] + points.shape[1]):
      thisPoint = newPoint
      isIn = newIn
      newPoint = [x + 1, y]
      newIn = isInPoint(newPoint)
      if isIn:
        if not oldIn:
          addToDetects(oldPoint, thisPoint)
          if isDefined(countOfMoreThanMaxThreshold) and (countOfMoreThanMaxThreshold > 1):
            outValues()
            return None
        if not newIn:
          addToDetects(newPoint, thisPoint)
          if isDefined(countOfMoreThanMaxThreshold) and (countOfMoreThanMaxThreshold > 1):
            outValues()
            return None
      oldPoint = thisPoint
      oldIn = isIn
  theMax = [None, 0]
  summ = 0
  for thisIndex, thisElements in enumerate(votesAndColors):
    thisCount = len(thisElements)
    printDebug("count of {}: {}".format("undetected" if (thisIndex == 0) else ("black" if (thisIndex == 1) else "white"), thisCount))
    summ += thisCount
    if(isUndefined(theMax[0]) or (thisCount > theMax[1])):
      theMax[0] = thisIndex
      theMax[1] = thisCount
  if (str(theNameOfTheLetter) == "3") and (coordinate[0] == 420) and (coordinate[1] == 230):
    print("coord: {}, theCoefficients: {}, undefined count: {}".format(coordinate, theCoefficients, undefinedCount))
    #die(coordinate)
  printDebug("Letter = {}".format(theNameOfTheLetter))
  if theMax[0] == 0:
    #outDebug()
    #print("ss")
    #input()
    printDebug("theMax[0] == 0")
    theResult = None
  else:
    if theCoefficients[0][0] > theCoefficients[1][0]:
      theMaxIndex = 0
      theMinIndex = 1
    else:
      theMaxIndex = 1
      theMinIndex = 0
    printDebug("theCoefficients: {}".format(theCoefficients))
    printDebug("(theCoefficients[theMinIndex][1] > (float(theCoefficients[theMaxIndex][1]) / 5)) = {}, (theCoefficients[theMinIndex][0] > (theCoefficients[theMaxIndex][0] / 10)) = {}, (theCoefficients[theMaxIndex][0] / theCoefficients[theMaxIndex][1] <= 0.05) = {}".format((theCoefficients[theMinIndex][1] > (float(theCoefficients[theMaxIndex][1]) / 5)), (theCoefficients[theMinIndex][0] > (theCoefficients[theMaxIndex][0] / 10)), (theCoefficients[theMaxIndex][0] / theCoefficients[theMaxIndex][1] <= 0.05)))
    #input()
    printDebug("theCoefficients: {}, undefined count: {}".format(theCoefficients, undefinedCount))
      
    if (theCoefficients[theMinIndex][1] > (float(theCoefficients[theMaxIndex][1]) / 5)) or (theCoefficients[theMinIndex][0] > (theCoefficients[theMaxIndex][0] / 10)) or (theCoefficients[theMaxIndex][0] / theCoefficients[theMaxIndex][1] <= 0.05):
      theResult = None
    else:
      """
      if isUndefined(maxThreshold):
        maxThreshold = getMaxmaxThreshold(summ)
      #print("maxThreshold = {}, votesAndColors = {}".format(maxThreshold, votesAndColors))
      printDebug("max count of others to pass: {}".format(maxThreshold))  
      outValues(theMax)
      for thisIndex, thisElements in enumerate(votesAndColors):
        if (thisIndex != theMax[0]) and (len(thisElements) > maxThreshold):
          return None
      """
      theResultParams = []
      theResultPoints = MyPointsList([])
      theResultPoints.size = [points.shape[1], points.shape[0]] 
      for element in votesAndColors[theMax[0]]:
        theResultParams.append(element[0])
        theResultPoints.append(element[2])    
      print("theCoefficients: {}, undefined count: {}".format(theCoefficients, undefinedCount))
            
      theResult = [Watermark.getByAvg(theResultParams), theResultPoints, MyPointsList(allPoints.getAll())]
  if(IS_DEBUGGING):
    input()  
  return theResult
MIN_COEFFICIENT_TO_DETECT = 0.05
MIN_COEFFICIENT_TO_DETECT_AS_IMPORTANT_ANTI = 0.05
MAX_COEFICIENT_DIFFERENCE_TO_DETECT_AS_IMPORTANT_ANTI = 0.01
STEP = 2
HEIGHT_TO_SEARCH_INTERVAL = [15, 43]
if SEARCH_ONLY_IN_INTERESTING_RECTANGLE:
  theXRangeCenter = theXRange = range(max([1, interestingRectangle[0][0]]), min([img.getWidth(), interestingRectangle[0][0] + interestingRectangle[1][0]]))
  theYRangeCenter = theYRange = range(max([0, interestingRectangle[0][1]]), min([interestingRectangle[0][1] + interestingRectangle[1][1], img.getHeight()]))
else:
  WIDTH = img.getWidth()
  MARGIN_OF_THE_WIDTH = int(WIDTH / 4)
  HEIGHT = img.getHeight()
  MARGIN_OF_THE_HEIGHT = int((HEIGHT - 60) / 2)  
  theXRangeCenter = range(MARGIN_OF_THE_WIDTH, WIDTH - MARGIN_OF_THE_WIDTH)
  theYRangeCenter = range(MARGIN_OF_THE_HEIGHT, HEIGHT - MARGIN_OF_THE_HEIGHT)
  theXRange = range(1, WIDTH)
  theYRange = range(0, HEIGHT)
  watermarkPartsRemoved = {'logo': False, 'id': False}
  os.system('cls')
  theWatermarks = {}
  interestingRectangle = [[28, 401], [6, 10]]
  interestingRectangle = None
  if isUndefined(interestingRectangle):
    currentXRange = range(0, WIDTH)
    currentYRange = range(0, HEIGHT)
  else:
    currentXRange = range(interestingRectangle[0][0], interestingRectangle[0][0] + interestingRectangle[1][0])
    currentYRange = range(interestingRectangle[0][1], interestingRectangle[0][1] + interestingRectangle[1][1])
  theDetectedBitmask = numpy.zeros((HEIGHT, WIDTH), numpy.bool8)
  for y in currentYRange:
    prevColor = None
    nextColor = img.getColor([0, y])
    #nextColor = {"ss": 3}
    print("y = {} of {}".format(y, currentYRange.stop - 1))
    for x in currentXRange:
      thisColor = nextColor
      if isDefined(prevColor):
        printDebug("Processing [{}, {}] (Color: {}) - [{}, {}] (Color: {})".format(x - 1, y, prevColor, x, y, thisColor))
        currentColorDifference = detectColorDifferenceFast(prevColor, thisColor)
        if isNotEmptyColorDifference(currentColorDifference):
          printDebug("Marking this pixel ([{}, {}])".format(x, y))
          theDetectedBitmask[y][x] = True
          #newImg.setColor([x, y], [255, 0, 0])
        outDebug()
      if x < currentXRange.stop - 1:
        nextColor = img.getColor([x + 1, y])
      prevColor = thisColor
  for x in currentXRange:
    prevColor = None
    nextColor = img.getColor([x, 0])
    #nextColor = {"ss": 3}
    print("x = {} of {}".format(x, currentXRange.stop - 1))
    for y in currentYRange:
      thisColor = nextColor
      if isDefined(prevColor):
        printDebug("Processing [{}, {}] (Color: {}) - [{}, {}] (Color: {})".format(x, y - 1, prevColor, x, y, thisColor))
        currentColorDifference = detectColorDifferenceFast(prevColor, thisColor)
        if isNotEmptyColorDifference(currentColorDifference):
          printDebug("Marking this pixel ([{}, {}])".format(x, y))
          theDetectedBitmask[y][x] = True
          #newImg.setColor([x, y], [255, 0, 0])
        outDebug()
      if y < currentYRange.stop - 1:
        nextColor = img.getColor([x, y + 1])
      prevColor = thisColor
  if False:
    for y in theYRange:
      debugThis = y in range(370, 417)
      currentWatermarks = [None, None]
      thisWatermark = [None, None]    
      theWatermarks[y] = [[], []]
      watermarks = [[], []]
      print("For y = {} of {}".format(y, theYRange.stop - 1))
      for x in theXRange:
        thisWatermark[0] = Watermark.detect(img.getColor([x, y - 1]), img.getColor([x, y])) if y > theYRange.start else None
        thisWatermark[1] = Watermark.detect(img.getColor([x, y + 1]), img.getColor([x, y])) if y < theYRange.stop - 1 else None
        for theIndex in range(2):
          if isUndefined(currentWatermarks[theIndex]):
            currentWatermarks[theIndex] = thisWatermark[theIndex]
            isLike = False
          elif isDefined(thisWatermark[theIndex]):
            isLike = thisWatermark[theIndex].isLike(currentWatermarks[theIndex])
          else:
            isLike = False
          if (x == theXRange.stop - 1) or ((not (isLike)) and (len(watermarks[theIndex]) > 0)):
            theRange = range(x - len(watermarks[theIndex]), x)
            theWatermarks[y][theIndex].append([theRange, clone(currentWatermarks[theIndex])])
            if debugThis and (30 in theRange) and (((theIndex == 0) and (y in range(375, 385))) or ((theIndex == 1) and (y in range(410, 417)))):
              print("Adding for x = {}, theIndex = {}, isLike = {}, range: {} to {}, watermark in this position: {}, current watermark = {}".format(x, theIndex, isLike, x - len(watermarks[theIndex]), x - 1, thisWatermark[theIndex], currentWatermarks[theIndex]))
              input()
            watermarks[theIndex] = []          
          watermarks[theIndex].append(thisWatermark[theIndex])
    stringsForDebug = []
    for theY in theWatermarks:
      stringForDebug = 'For y = {}'.format(theY) + ': '
      debugThis = (thisY == 379)
      theValues = theWatermarks[theY]
      for index, thisValues in enumerate(theValues):
        stringForDebug += '{} watermarks: '.format('open' if (index == 0) else 'close')
        for thisIndex, elements in enumerate(thisValues):
          if thisIndex > 0:
            stringForDebug += ', '
          stringForDebug += '{} - {} ({})'.format(elements[0].start, elements[0].stop - 1, outForUser(elements[1].getAvgCoef()) if isDefined(elements[1]) else None)
      stringsForDebug.append(stringForDebug)
    printDebug(", ".join(stringsForDebug))
def getLength(x, y):
  result = 0
  while 
for x in theXRange:
  xIsInCenter = x in theXRangeCenter
  watermarks = []
  lastWatermark = None
  lastWatermarkLength = 0
  lastWatermarks = []
  allLastWatermarks = []
  YOfOk = {}
    
  for y in theYRange:
    
  """if x >= 19:
    ob.disable()
    sec = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(ob, stream=sec).sort_stats(sortby)
    ps.print_stats()
    print(sec.getvalue())
    die()
   """
  if not IS_DEBUGGING:
    print("x: {}".format(x))
  for y in theYRange:
    isInCenter = xIsInCenter and (y in theYRangeCenter)
    isDebugging = IS_DEBUGGING and ((x >= interestingRectangle[0][0]) and (x < (interestingRectangle[0][0] + interestingRectangle[1][0])) and (y >= interestingRectangle[0][1]) and (y < (interestingRectangle[0][1] + interestingRectangle[1][1])))
    oldCoordinate = [x - 1, y]
    thisCoordinate = [x, y]
    thisWatermarkByY = Watermark.detect(img.getColor([x, y + 1]), thisColor) if (y < theYRange[1] - 1) else None
    oldColor = img.getColor(oldCoordinate)
    thisColor = img.getColor(thisCoordinate)
    thisWatermark = Watermark.detect(oldColor, thisColor)
    printDebug("Pixels: {} ({}) - {} ({}), WM: {}, watermark by Y: {}".format(oldCoordinate, oldColor, thisCoordinate, thisColor, thisWatermark, thisWatermarkByY))
    if isDefined(thisWatermark):
      if thisWatermark.getAvgCoef() < MIN_COEFFICIENT_TO_DETECT:
        printDebug("avg coef = {} < {}, breaking".format(thisWatermark.getAvgCoef(), MIN_COEFFICIENT_TO_DETECT))
        thisWatermark = None
      else:
        minWidth = x + 1
        maxWidth = min(img.getWidth(), x + STEP + 1)
        printDebug("for x from [{} to {}]".format(minWidth, maxWidth))
        hasNonAnti = hasAnti = False
        for thisX in range(minWidth, maxWidth):
          theWatermarks[y][theIndex]
          oldColor = img.getColor([thisX - 1, y])
          thisColor = img.getColor([thisX, y])
          thisWM = Watermark.detect(oldColor, thisColor)
          printDebug("for x: {} ({}) - {} ({}), WM = {}".format(thisX - 1, oldColor, thisX, thisColor, thisWM))
          if isDefined(thisWM) and thisWM.isAnti(thisWatermark) and (thisWM.getAvgCoef() > MIN_COEFFICIENT_TO_DETECT_AS_IMPORTANT_ANTI) and (thisWM.getMaxDifference() < MAX_COEFICIENT_DIFFERENCE_TO_DETECT_AS_IMPORTANT_ANTI):
            hasAnti = True
            printDebug("WM is defined, is anti and zvf coef = {} > {}".format(thisWM.getAvgCoef(), MIN_COEFFICIENT_TO_DETECT_AS_IMPORTANT_ANTI))
          else:
            hasNonAnti = True
            break
        if hasAnti and not(hasNonAnti):
          printDebug("All {} next watermarks detected as anti, thisWatermark to zero".format(STEP))
          thisWatermark = None                    
    printDebug("Current length = {}, last watermark: {}".format(lastWatermarkLength, lastWatermark))
    if isDefined(thisWatermark) and isDefined(lastWatermark) and lastWatermark.isLike(thisWatermark):
      lastWatermarkLength += 1
      lastWatermarks.append(thisWatermark)
      printDebug("This watermark is defined and like last, so setting length to {}".format(lastWatermarkLength))
    else:
      if (lastWatermarkLength >= HEIGHT_TO_SEARCH_INTERVAL[0]) and (lastWatermarkLength <= HEIGHT_TO_SEARCH_INTERVAL[1]):
        if not watermarkPartsRemoved['logo']:
          #print("Checking for logo at [{}, {}] - [{}, {}] (length of the line: {}, watermarks: all lines: {}, prev(2)before: {}, prevbefore: {}, before: {}, this: {})".format(x, y - lastWatermarkLength, x, y - 1, lastWatermarkLength, len(allLastWatermarks), allLastWatermarks[len(allLastWatermarks) - 3], allLastWatermarks[len(allLastWatermarks) - 2], allLastWatermarks[len(allLastWatermarks) - 1], lastWatermarks))
          PROBABLE_SIZE_COFFICIENT = lastWatermarkLength / 37
          PROBABLE_SIZE = int(103 * PROBABLE_SIZE_COFFICIENT)
          PROBABLE_TOP = int(y - lastWatermarkLength - 33 * PROBABLE_SIZE_COFFICIENT)
          print("Searching for big logo ([{}, {}] - [{}, {}])".format(x, PROBABLE_TOP, int(x + 215 * PROBABLE_SIZE_COFFICIENT), PROBABLE_TOP + PROBABLE_SIZE))
          theValue = getMatchesByLine([x, y], lastWatermarkLength, "krisha-logo")
          if isUndefined(theValue):
            print("Big logo not found, looking for small one")
            theValue = getMatchesByLine([x, y], lastWatermarkLength, "krisha.kz")
            if isUndefined(theValue):
              print("Small logo not found too")                          
          if isDefined(theValue):
            theValue[2].unwatermark(watermark = theValue[0])
            watermarkPartsRemoved['logo'] = True
            print("Logo removed")
            #endProfiling()
        if isInCenter and not (watermarkPartsRemoved['id']):
          theValue = isMatchesByLetter([x, y - lastWatermarkLength], "I", lastWatermarkLength)
          print("y = {}, lastWatermarkLength = {} in [{} - {}], result of matching: {}".format(y, lastWatermarkLength, HEIGHT_TO_SEARCH_INTERVAL[0], HEIGHT_TO_SEARCH_INTERVAL[1], theValue))
          #input()
          if isDefined(theValue):
            #for point in theValue[1]:
            #   newImg.setColor(point, [255, 0, 255])
            theDValue = isMatchesByLetter([[x + theValue[1].size[0] + 4, 7], [y - lastWatermarkLength - 1, 2]], "D", lastWatermarkLength)
            if isDefined(theDValue):
              #for point in theDValue[1]:
              #   newImg.setColor(point, [255, 255, 0])
              theResults = getMatchesByLetters([[x + theValue[1].size[0] + 4, theValue[1].size[0] * 43], [y - lastWatermarkLength - 1, 2]], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], lastWatermarkLength)[0]
              the6Value = isMatchesByLetter([[x + theValue[1].size[0] + 4, theValue[1].size[0] * 43], [y - lastWatermarkLength - 1, 2]], "7", lastWatermarkLength)
              if len(theResults) > 0:
                theValue[2].unwatermark(watermark = theValue[0])
                theDValue[2].unwatermark(watermark = theDValue[0])
                for theCurrentValue in theResults:
                  theCurrentValue[2].unwatermark(watermark = theCurrentValue[0])
                  #for point in theCurrentValue[1]:
                  #  if newImg.has(point):
                  #    newImg.setColor(point, [255, 255, 0])
                watermarkPartsRemoved['id'] = True
      lastWatermarkLength = 1
      allLastWatermarks.append(clone(lastWatermarks))
      lastWatermarks = [thisWatermark]
      printDebug("This watermark is {}, so settiung length to {}".format("undefined" if isUndefined(lastWatermark) else "not like last", lastWatermarkLength))
    lastWatermark = thisWatermark
    outDebug()
    if isDebugging:
      input()
#eachPixelsPair(img.getSize(), processThis, coords)



"""def printPix(pix, second = None, third = None):
  Debug.log(repr(pix), second, third)
eachPixelsPair([2, 2], printPix)
#img = Image("images/watermarked/1.jpg")
dd = [2, 3, 4]
"""
#Debug.log(arrayIsLikable(dd, 0.9))
#Debug.log(dd.hasLikableValues())
#img.setColor([0, 0], [0, 0, 0])
#img.save(PATHS_TO_THE_IMAGES[1])