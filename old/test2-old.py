import copy, numpy, cv2
from functions import die, clone, isNone, isNotNone, isDefined, canHaveProperties, toMyArray, toNumericValueIfItIs, isNumericValue, toIntegerValueIfItIs, isIntegerValue, toNaturalIntegerIfItIs, isNaturalInteger
from arrays import MyArray, ArrayWithNaturalKeys, MyArrayList, MyNumericArray, MyArrayDictionary, MyArraySet
from matplotlib import pyplot as plt
def processImage(url):
  image = Image(url)
  die(image)
  patterns = []
  shapes = Shapes.getByImage(image)
  match(getBaseUrl(url)):
    case "krisha.kz":
      patterns = patterns.append("   ^\nКрыша")
      patterns = patterns.append("ID\d+")
      
      Shapes.getByLetters()
  for pattern in patterns:
    matches = getSequenceByRegExp(pattern).getMatches(shapes)
    if matches != None:
      image.removeWatermark(matches.getArea(), 1)
  path = getWaterMarksFolder()
  id = getMaxFile(path, "jpg", 0) + 1
  path += "/" + id + ".jpg"
  image.saveTo(path)
  return path
class Image(object):
  pixels = None
  def __init__(this, url):
    this.original = cv2.imread(url, cv2.IMREAD_UNCHANGED)
    this.byValueInHSV = cv2.cvtColor(this.original, cv2.COLOR_RGB2HSV)[:, :, 2]
    def getByParam(index, maxOffset = 81):
      return cv2.Canny(cv2.cvtColor(numpy.stack(((cv2.cvtColor(this.original, cv2.COLOR_RGB2HSV)[:, :, index]), ) * 3, axis=-1), cv2.COLOR_BGR2GRAY), 12, 12 + maxOffset).astype(numpy.int32)
    def printEdges(edges):
      plt.subplot(1, 1, printEdges.plotIndex), plt.imshow(edges)
      printEdges.plotIndex += 1
    printEdges.plotIndex = 1
    toBoolean = numpy.vectorize(lambda value1: value1 != 0)
    byValueInHSV = getByParam(2)
    #print(byValueInHSV)
    
    cnts = cv2.findContours(this.byValueInHSV, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    print(cnts)
    #cv2.drawContours(this.original, cnts, -1, (255,255,255))
    for c in cnts:
      cv2.drawContours(byValueInHSV, [c], -1, (255,255,255))    
    printEdges(byValueInHSV)
    plt.show()
    return
    this.contours, this.hierarchy = cv2.findContours(this.byValueInHSV, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(this.original, this.contours, -1, (0, 0, 255))
    plt.subplot(111), plt.imshow(this.original)
    plt.show()
  def removeWatermark(this, area, depth = 1):
    borderPoints = area.getBorder(range((- 1) * (depth + 1), 2))
    watermarks = MyArrayList()
    myDictionary = MyArrayDict()
    for index in range(depth + 1):
      watermarks.push(WaterMark())
    for borderPoint in borderPoints:
      if(borderPoint.theType == 0):      
        thePoint = borderPoint
        typeIndex = None
      else:
        thePoint = borderPoint.parents[0]
        typeIndex = 0 if borderPoint.theType == -1 else 1
      if not myDictionary.hasKey(thePoint):
        myDictionary[thePoint] = MyArrayList([MyArrayList(), MyArrayList()])
      if typeIndex != None:
        myDictionary[thePoint][typeIndex].push(borderPoint)
    for points in myDictionary:
      forEachPair(points[0], points[1], lambda point1, point2: watermarks[borderPoint.parents.count() - 1].takeIntoConsideration(this.getColor(point1), this.getColor(point2)))
    for pixel in area:
      color = this.getColor(pixel)
      if(borderPoints.hasKey(pixel)):
        this.setColor(pixel, watermarks[borderPoints[pixel].parents.length - 1].decode(color))
      else:
        this.setColor(pixel, watermarks[(borderPoints[pixel].parents.length - 1) if borderPoints.hasKey(pixel) else depth].decode(color))
  def getLinesInArea(lines):
    pass
  def getShapesInArea(lines):
    pass
def getRecursive(set, processor, isRestricted = None, levelsNeeded = None, withParents = False):
  getEmpty = lambda: getSameTypeArray(set)
  processedElements = getEmpty()
  result = getEmpty()
  currentNextElements = getEmpty()
  currentLevel = 0
  if isRestricted == None:
    isRestricted = lambda: False
  thisSet = clone(set)
  toContinue = True
  if levelsNeeded == None:
    levelsNeeded = True
    maxLevelNeeded = None
  elif(isinstance(levelsNeeded, int)):
    levelsNeeded = MyNumericArray(range(levelsNeeded, levelsNeeded + 1))
    maxLevelNeeded = levelsNeeded.getMaximum()
  while toContinue:
    for element in thisSet:
      if withParents:
        if element.parents == None:
          element.parents = MyArrayList()
        parents = element.parents.mergeWith([element])
      subElements = processor(element, currentLevel)
      for subElement in subElements:
        if withParents:
          subElement.parents = parents
        if (not (processedElements.has(subElement))) and (not (isRestricted(subElement, currentLevel))):
          currentNextElements.push(subElement)
    processedElements = processedElements.mergeWith(currentNextElements)
    if levelsNeeded == True or levelsNeeded.has(currentLevel):
      result = result.mergeWith(currentNextElements)
    if maxLevelNeeded == None:
      if currentNextElements.isEmpty():
        toContinue = False
    elif currentLevel == maxLevelNeeded:
      toContinue = False
    currentLevel += 1    
    thisSet = currentNextElements
  return result
def getCombinationsAndIndexes(values, dimension, filter = None):
  for index, value in enumerate(values):
    otherCombinations = getCombinationsAndIndexes(values, dimension - 1) if dimension > 1 else numpy.ndarray([])
    result = MyArrayList()
    for otherCombinationAndIndex in otherCombinations:
      otherCombinationAndIndex[0] = numpy.insert(otherCombinationAndIndex[0], 0, index)
      otherCombinationAndIndex[1] = numpy.insert(otherCombinationAndIndex[1], 0, value)
      if filter == None or filter(otherCombinationAndIndex[1], otherCombinationAndIndex[0]):
        result.push(otherCombinationAndIndex)
  return result
def getCombinations(values, dimension, filter = None):
  return getCombinationsAndIndexes(values, dimension, None if filter == None else lambda x: filter(x))
def forEachPixels(rectangle, checker, processor):
  isIn = False
  beforePixel = None
  def thisProcessor(x, y, isContinue):
    if not(isContinue):
      isIn = False
      beforePixel = None
    newIsIn = checker(x, y)
    thisCoordinate = [x, y]
    if newIsIn != isIn:
      coordinate = thisCoordinate if isIn else beforePixel
      processor(coordinate[0], coordinate[1])
    beforePixel = thisCoordinate
  for combin in getCombinations([False, True], 2):
    rectangle.forEachPixel(combin[0], combin[1], thisProcessor)
class Coordinate(object):
  dimension = None
  value = None
  def getNearest(this):
    getCombinationsAndIndexes([-1, 0, 1], this.dimension, lambda x: not x.isSameAs(0))
class Area(MyNumericArray):
  def getBorder(distance = 0):
    isInArea = lambda pixel: this.has(pixel)
    border = Area()
    result = Area()
    range = getRangeIntervalBy(distance)
    ranges = range.split(0, true)
    forEachPixels(this.getSizeRectangle(), isInArea, lambda pixel: border.push(pixel))
    for indexOfTheRange, thisRange in enumerate(ranges):
      if indexOfTheRange == 1:
        currentResult = border
        result = result.mergeWith(border)
      else:
        comparer = isInArea if indexOfTheRange == 0 else (lambda pixel: not isInArea(pixel))
      if indexOfTheRange == 1:
        comparer = lambda pixel: not isInArea(pixel)
        currentResult = Area(getRecursive(border, lambda pixel: pixel.getNearPoints(), comparer, thisRange - 1))
      theType = indexOfTheRange - 1
      for point in currentResult:
        point.theType = theType
      result = result.mergeWith(currentResult)
    return result
  def getPoints():
    pass
  def intersectsWith(area):
    pass
class Rectangle(Area):
  intervals = [[], []]
class Shapes(MyArrayList):
  def getArea(this):
    border = this.getBorder()
    oldX = isIn = None
    result = Area()
    def process(x, y):
      if x != oldX:
        isIn = False
        oldX = x
        if(border.has(x, y)):
          isIn = not isIn
        if isIn:
          result.push(x, y)
    this.eachPixel(process)
    return result
  def getByArea(this, area):
    return this.filter(lambda shape: shape.getArea().intersectsWith(area))  
  #def getIncludePart(otherShapes):
Shapes.getPathToTheLetter = lambda letter: "letters/" + letter + ".png"
def getShapesByLetter(letter):
  return Shapes.getByImage(Shapes.getPathToTheLetter(letter))
def getShapesByLetters(letters):
  lines = letters.splitToLines()
  offset = [0, 0]
  result = Shapes()
  for line in lines:
    offset[0] = 0
    maxHeight = None
    for letter in line:
      thisShape = Shapes.getByLetter(letter)
      result = result.mergeWith(thisShape, offset = offset)
      offset[0] += thisShape.getWidth() + Shapes.CONSTANTS.LETTERS_MARGIN[0]
      thisHeight = thisShape.getHeight()
      if (maxHeight == None) or (thisHeight > maxHeight):
        maxHeight = thisHeight
    offset[1] += maxHeight + Shapes.CONSTANTS.LETTERS_MARGIN[1]
  return result
Shapes.getByLetters = getShapesByLetters
def getShapesByLines(lines):
  pass
def getLinesByImage(image):
  byValueInHSV = cv.cvtColor(image.image, cv.COLOR_RGB2HSV)[:, :, 2]
  image, contours, hierarchy = cv.findContours(byValueInHSV, cv.RETR_FLOODFILL, cv.CHAIN_APPROX_NONE)
  gotElements = MyArraySet(range(0, len(contours)))
  def getPoint(index):
    if index in gotElements:
      result = contours[index]
      gotElements.remove(index)
    else:
      result = None
    return result
  lines = MyArrayList()
  for index, element in enumerate(hierarchy):
    if (element[0] == -1):
      point = getPoint(index)
      line = MyArrayList()
      while(isNotNone(point)):
        line.append(point)
        if element[1] >= 0:
          point = getPoint(element[1])
          element = hierarchy[element[1]]
        else:
          point = None
      shapesDetector = ShapesDetector()
      shapesDetector.processPoints(line, True)
      lines = lines.mergeWith(shapesDetector.lines)
  return Lines(lines) 
def getShapesByImage(image):
  return getShapesByLines(getLinesByImage(image))
Shapes.getByLines = getShapesByLines
Shapes.getByImage = getShapesByImage
Shapes.getByLetter = getShapesByLetter

class Shape(object):
  def getIncludePart(this, rectangle):
    for shape in this:
      if rectangle.includes('shape'):
        pass
#  Lines
class Lines(object):
  def toShape():
    pass
Lines.getByImage = getLinesByImage
class Line(object):
  pass
class PixelsSet(object):
  def getLinesInArea():
    pass
  def getBorder(distance):
    pass
  def unwatermark(border):
    pass
processImage("C:/Users/Administrator/Pictures/10-full.jpg")