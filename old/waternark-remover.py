from enum import Enum
MIN_DISTANCE_DIVIDER_FOR_CAN_COLLABSE = 0.2
MIN_ANGLE_OF_THE_ENDS_FOR_CAN_COLLABSE - math.pi  / 3
class TypeOfTheFigure(Enum):
  LINE = 0
  ARC = 1
  LEAD = 2
class Figure
  theType = None
  length = None
  points = None
  turnAngle = None
  def getLikableCoefficient(this, other, coefficient = None):
    result = None
    if this.theType == other.theType and isLikableAngle(this.turnAngle, other.turnAngle):
      thisCoefficient = other.length / this.length
      if (coefficient == None) or (isLikableCoefficient(coefficient, thisCoefficient)):
        result = thisCoefficient
    return result
class Shape:
  type = None
  length
  startAngle
  positonInterval
  def getPartData(this, otherShape, coefficient = None, possibleOrder = None) #Считать данные (коэфициент подобия) фигуры, если она включается в другую фигуру (является частью)
    thisCount = this.count()
    otherCount = otherShape.count()
    firstFigure = this[0]
    result = None
    for indexOfTheOtherFigure, otherFigure in enumerate(otherShape):
      coefficient = firstFigure.getLikableCoefficient(otherFigure, coefficient)
      if coefficient != None:
        signs = MyArrayDict()
        if ((possibleOrder == None) or (possibleOrder == 1)) and (indexOfTheOtherFigure + thisCount <= otherCount):
          signs[1] = MyArrayList([otherFigure])
        if ((possibleOrder == None) or (possibleOrder == -1)) and (indexOfTheOtherFigure >= thisCount - 1):
          signs[-1] = MyArrayList([otherFigure])
        if len(signs) > 0:
          for indexOfThisFigure in range(1, thisCount):
            for sign, values in enumerate(signs):
              otherFigure = otherShape[indexOfTheOtherFigure + sign * indexOfThisFigure]
              if this[indexOfThisFigure].getLikableCoefficient(otherFigure, coefficient) == None:
                del signs[sign]
              else
                signs[sign.append(otherFigure)
            if len(signs) == 0:
              break
          if len(signs) > 0:
            result = {"coefficient": coefficient, shape: Shape(enumerate(signs)[0][1], order: signs.getKeyByIndex(0))}
          if result != None:
            break
    return result       
    def processPair(thisFigure, otherFigure, thisIndex, otherIndex):
      if thisIndex >= otherIndex:
        coefficient = thisFigure.getLikableCoefficient(otherFigure)
        if coefficient !== None:
          
      if thisIndex >= otherIndex:
        
    forEachPair(this, otherShape, processPair)              
class Shapes
class oixelsSet:
  
class Lines
  def popSmoothParts(this, accelerationIsInSameSign = None):
    return this.popByPairs(lambda value1, value2: return absDifference(value1.angle, value2.angle) <= MAX_ANGLE_TO_BE_SMOOTH)
    prevLine = None
    signOfTheAcceleration = None
    canPassThis = thisIsPassed = None
    thisIndexes = []
    indexesToRemove = []
    def popByIndexes(indexes):
      result = []
      for index in indexes:
        indexesToRemove.append(index)
        result.append(this[index])
    def hasSameAngleAccelerationSign(this)
      this.getByKey('acceleration').filterSigns().isSame()
    def canCollabse(this)
      return this.hasSameAngleAccelerationSign() and (this.distanceBetweenEnds() < (this.getMaxDistance() / MIN_DISTANCE_DIVIDER_FOR_CAN_COLLABSE)) and (this.angleDifferenceAtTheEnds() > MIN_ANGLE_OF_THE_ENDS_FOR_CAN_COLLABSE)
    def endOfTheSearch():
      if canPassThis:
        result.append(popByIndexes(thisIndexes))
      if accelerationIsInSameSign == False:
        canPassThis = False if (accelerationIsInSameSign == False) else True
      thisIndexes = []
    for indexOfTheLine, line in enumerate(this):
      if prevLine != None:
        if isLikable(prevLine.angle, line.angle, MAX_ANGLE_TO_BE_SMOOTH):
          if signOfTheAcceleration == None:
            signOfTheAcceleration = numpy.sign(prevLine.acceleration)
          elif accelerationIsInSameSign == True:
            if signOfTheAcceleration != numpy.sign(prevLine.acceleration):
              thisIsPassed = False
              canPassThis = False
            else:
              canPassThis = True
          elif accelerationIsInSameSign == False:
            if (signOfTheAcceleration != numpy.sign(prevLine.acceleration))
              canPassThis = True
          else:
            canPassThis = True
        else:
          canPassThis = False
          thisIsPassed = False          
        if thisIsPassed == False:
          endOfTheSearch()
        else:
          thisIndexes.append(indexOfTheLine)
          
          
      prevLine = line
def Shape.detectByLines(lines)
  smoothParts = lines.popSmoothParts(accelerationIsInSameSign = true)
    for smoothPart in smoothParts:
      if smoothPart.canCollabse():
        type = 'leaf';
      else: 
        type = 'arc';
      anglesDistance = smoothPart.getAnglesDistance()
       shapes.append(Shape(type, anglesDistance))
  for line in lines
    shapes.append(new Shape(line))
  cycles = lines.getCycles(minElementsCount = 30, accelerationIsInSameSign = true, accelerationScatter = LIKABLE_ACCELERATION_COEFICIENT, maxEdgesCount = 1)
  for circle in cycles:
    theType = None
    if circle.edgesCount() > 1 and circle.maxTurnInDegrees() > 180 + 70:
      theType = 'loop'
    elif circle.edgesCount() = 0
      theType = 'ellipse'
class ShapeSequenceGetter(string):
  currentIndex = 0
  def has(this, substring):
    lengthOfTheSubstring = len(substring)
    if(string[this.currentIndex:(this.currentIndex + lengthOfTheSubstring)] == substring):
      result = True
      this.currentIndex += lengthOfTheSubstring
    else:
      result = False
    return result
  def get(count):
    result = string[this.currentIndex:(this.currentIndex + count)]
    this.currentIndex += count
    return result
  def isComplete(this):
    return this.this.currentIndex >= len(this)
  def processEach(this, handler):
    this.currentIndex = 0
    before = ShapeSequence()
    result = []
    while(not this.isComplete()):
      newElement = handler(before, this)
      if(newElement != None)
        result.append(newElement)
      before = newElement
    return result
def getSequenceByRegExp(regexp):
  seq = ShapeSequence()
  def forEachElement(beforeResult, string)
    newLineString = "\n"
    if(string.has(newLineString)):
      result = newLineString
    elif(string.has("\d")):
      result = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    elif(string.has('+')):
      beforeResult = ShapeSequence.count = [1, None]
      result = None
    else:
      result = string.get(1)
    if result != None:
      result = ShapeSequence(result)
    return result
  getter = ShapeSequenceGetter(regexp)
  result = getter.processEach(forEachElement)
  return ShapeSequence(result, True)
def getSequences(values):
  result = []
  for value in values:
    result.append(ShapeSequence(value))
  return result
class ShapeSequence:
  operation = None
  count = 1
  subsequences = []
  def __init__(self, value, isSequence = True):
    if isinstance (value, dict):
      self.operation = value.operation
      self.count = value.count
      self.subsequences = value.subsequences
    elif isArray(value):
      self.operation = 'sequence' if isSequence else 'or'
      self.subsequences = getSequences(value)
      self.count = 1
    elif value == "\n":
      self.operation = 'new-line'
      self.count = 1
    else:
      self.operation = 'symbol'
      self.subsequences = [value]
      self.count = 1
  def getMatches(sequence, shapes, rectangle, firstRectangle = None):
    subElements = sequence.subsequences
    firstRectangle = rectangle
    match sequence.operation:
      case "sequence":
        def getResult():
          result = []
          for subSequence in subElements:
            foundMatch = getMatchesOfTheShapeSequence(subSequence, shapes, rectangle, firstRectangle = firstRectangle)
            if(foundMatch == None):
              result = None
              break
            if result == None
              break
            result = result.append(foundMatch)
            rectangle = foundMatch.getNextRectangle()
            if firstRectangle == None:
              firstRectangle = rectangle
            
          return result
      case "or":
        result = None
        def getResult():      
          for subSequence in subElements:
            foundMatch = getMatchesOfTheShapeSequence(subSequence, shapes, rectangle = rectangle, firstRectangle = firstRectangle)
            if(foundMatch != None):
              result = foundMatch
              rectangle = foundMatch.getNextRectangle()
              if firstRectangle == None:
                firstRectangle = rectangle
              break
            if result != None
              break
          return result
      case "symbol":
        def getResult():
          result = Shapes.getByLetter(this.subsequences[0]).getPartData(shapes, rectangle = rectangle)
          rectangle = result.getNextRectangle()
          if firstRectangle == None:
            firstRectangle = rectangle
      case "new-line":
        def getResult():
          if rectangle === None:
            rectangle = firstRectangle
          if (firstRectangle != None) and (not (rectangle[0] <= firstRectangle[0])):
            rectangle[0] = firstRectangle[0]
          rectangle = rectangle.onePositionDown()
          return True if (rectangle[1][1] <= shapes.getSize()[1]) else None
    toContinue = true
    count = 0
    currentResults = []
    result = None
    while toContinue:
      if(inRange(count, this.count)):
        result = clone(currentResults)
      thisResult = getResult()
      if thisResult == None:
        toContinue = false
      else:
        count += 1
        if thisResult != True:
          currentResults.append(thisResult)
    return result                
class Shapes:
  shapesAndPositions = []
  def getPartData(this, other, coefficient = None, possibleOrder = None):
    result = None
    if isinstance(other, Shape):
      for thisShape in this:
        result = other.getPartData(thisShape, coefficient = coefficient, possibleOrder = possibleOrder)
        if(result != None)
          break
    else:
      firstShape = this.getValueByIndex(0)
      for otherShape in other:
        partData = firstShape.getPartData(otherShape, coefficient = coefficient, possibleOrder = possibleOrder)
        def isNotMatched(shape):
          return shape is not otherShape
        if partData != None:
          result = MyListArray([partData])
          for pairIndex in range(1, this.getCount()):
            thisShape = this.getValueByIndex(pairIndex)
            offset = thisShape.getOffsetFrom(firstShape)
            subShapes = other.getByArea(Rectangle(partData.coefficient * offset - SHAPE_MATCH_MAX_ERROR, partData.coefficient * thisShape.getSize() + SHAPE_MATCH_MAX_ERROR)).filter(isNotMatched)
            thisPartData = subShapes.getPartData(thisShape, coefficient = partData.coefficient, possibleOrder = possibleOrder)
            if thisPartData == None:
              result = None
            if result == None:
              break
            result.push(thisPartData)
    return result        
  
class Letter
  shepes = None
  symbol = None
class WaterMarkRemover(object)
  def __init__(this, urlOfTheImage):
    this.image = WaterMarkRemover.getImageByURL(urlOfTheImage)
    this.edges = WaterMarkRemover.getEdges(this.image)
    this.busyEdgeIndexes = []
  def removeMatchesWatermark(this, text):
    matches = WaterMarkRemover.shapesMatches(text)
    if matches != None:
      for match in matches:
        for index in range(MAX_COUNT_OF_INNER_BORDERS):
          border = match.getInnerBorder(1)
          this.decodeByWatermarkCoefficient(this.getWatermarkCoefficientFor(border), border)
        mainArea = match.getInsideInnerBorder(MAX_COUNT_OF_INNER_BORDERS)
        this.decodeByWatermarkCoefficient(this.getWatermarkCoefficientFor(match.getInnerBorder(MAX_COUNT_OF_INNER_BORDERS)), mainArea)
  def shapesMatches(this, text):
    shapeSequence = Matcher.getShapesForText()
    result = None
    while((countour = this.obtainFreeCountour()) != None):
      for offset, shape in shapeSequence:
        if self.isMatchesAsFirst(countour, shape):
          thisIsMatch = None
          for offsetFromThis, otherShape in shapeSequence.getNearest(shape):
            if not (self.isMatchesAsFirst(getCountoursInOffset(countour, offsetFromThis), otherShape)):
              thisIsMatch = False
            If thisIsMatch != None:
              self.breakAllMatches
          if thisIsMatch == None:
            thisIsMatch = True
          if self.hasMatches()
            resukt = self.getMatches()
            break
        if result != None
          break
      if result != None
        break
    return result          