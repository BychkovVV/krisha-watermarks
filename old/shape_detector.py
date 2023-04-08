import os
import math
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
PATH_TO_THE_LOG_FILE = "log.txt"
CURRENT_LOG_IMPORTANCE_LEVEL = 1
logString = ''
def logThis(value, importanceLevel = 0)
  if importanceLevel <= CURRENT_LOG_IMPORTANCE_LEVEL:
    if len(logString) > 0:
      logString += ", "
    logString += value
def pushLog()
  prefix = "\n" if os.path.exists(PATH_TO_THE_LOG_FILE) and os.path.isfile(PATH_TO_THE_LOG_FILE) and (os.path.getsize(PATH_TO_THE_LOG_FILE) > 0) else ""
  with fopen(PATH_TO_THE_LOG_FILE, "a") as variableOfTheFile:
    fwrite(variableOfTheFile, prefix + logString)
def getPoint(x = 0, y = 0):
  return np.array([x, y])
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
def getLineParameters(point1 = None, point2 = None, length = None):
  distance = math.dist(point2, point1) if (point1 != None and point2 != None) else 0
  result = dict([("length", distance), ("angle", getAngle(point2, point1)), ("acceleration", None)] if distance > 0 else [("length", 0), ("angle", None), ("acceleration", None)])
  result.points = [point1, point2]
  result.length = length
  return result
OFFSET_MAX_ERROR = 3
def isLikable(value1, valur2, maxError)
  return abs(value2 - value1) <= maxError
def isLikableOffset(offset1, offset2)
  return isLikable(offset1, offset2, OFFSET_MAX_ERROR)
class ShapeDetector(object)
  lineOffset = None
  startPoint = None
  offsetFromBegin = None
  fixedChangeOfCoordinates = [False, False]
  currentOffset = None #Текущее ождаемое приращение (количество пикселей), в коорднате, которая увеличивается с меньшей скоростью (для измерения линии)
  currentMeasuredLength = 0 #Длина линии до проверки на "прямую"
  lastDifference = [0, 0] #Смещение при проверки на прямую
  currentMeasuredLengthFromBegin = None #Длина интервала с начала "отсчёта"
  coordinatesIncrementFromTheLastCoordinatesChange = None #Разница с начала фиксации
  previousPoint = None #Последняя, зафиксированная точка
  currentChangeIndexAndCount = None #Массив, 0-й элемент - индекс (0 - для абсциссы, 1 - для ординаты) оси, которая приращается с меньшей скоростью, 1 - во сколько эта скороть меньше
  currentOffsetIndex = None #Индекс
  currentLineCoefficientsIsFixedOnlyBecauseOfTheOverflow = False
  lastNonStrangePoint = None #Последняя точка текущей, анализируемой линии, которая точно зафиксирована на её часть (не "подозритальная", что это - часть другой линии)
  strangePoints = None
  currentProcessingPoint = None #Текущая, обрабатываемая точка
  _thisIsEndingPoint = None #Текущая, анализируемая точка - последняя в анализируемом контиуре?
  strageStartIndexesCount = 0 #Количество итераций с того момента, когда начались отклония реальной линии от ожидаемой
  points = []
  lines = []
  isNewLine = True
  firstPointValue = None #1-я точка текущей, анализируемой линии
  currentLengthOfTheLine = 0
  currentLengthOfStrangePointsParts = 0
  def fixThisIncrementOfTheCoordinatesAsStandardForThisLineIfItIsDidNotFixedYet(self, increment): #Фиксирует параметры линии, если они не установлены, если установлены, то сравивает их с существующими, возвращает True, если не соотвттвтуют, None, если соответствуют, но не полностью и False - если полностью соотвутствуют
    if self.currentChangeIndexAndCount == None:
      logThis("Коэффициенты текущей линии ещё не зафиксировны")
      self.fixThisIncrementOfTheCoordinatesAsStandardForThisLine(increment)
      result = False
    else
      thisOffset = increment[getAntiIndex(self.currentChangeIndexAndCount[0])] / self.currentChangeIndexAndCount[1]
      logThis("Ожидаемое приращение по " + ("абсциссе" if (self.currentChangeIndexAndCount[0] == 0) else "ординате") + " = инкремент по другой оси / параметр = " + str(increment[getAntiIndex(self.currentChangeIndexAndCount[0])]) + " / " + str(self.currentChangeIndexAndCount[1]) + " = " + thisOffset)
      self.currentOffset += thisOffset
      estimatedOffset = math.floor(self.currentOffset)
      currentIncrement = increment[self.currentChangeIndexAndCount[0]]
      self.currentOffset -= currentIncrement
      if estimatedOffset == currentIncrement:
        logThis("estimatedOffset == currentIncrement (" + estimatedOffset + " == " + currentIncrement + ")")
        result = False
      elif isLikableOffset(estimatedOffset, currentIncrement):
        logThis("estimatedOffset is likable currentIncrement (" + estimatedOffset + " is likable " + currentIncrement + ")")
        result = None        
      else:
        result = True
    return result
  def fixThisIncrementOfTheCoordinatesAsStandardForThisLine(self, increment): #Фиксирует параметры линии, устанавливает текущее ожидание приращения координаты, которой свойственно приращение в меньшей степени в 0
    if abs(increment[0]) > abs(increment[1]):
      self.currentChangeIndexAndCount = [1, increment[0] / increment[1]]
      result = True
    else
      self.currentChangeIndexAndCount = [0, increment[1] / increment[0]]
      result = False
    logThis("Фиксируем параметры линии, стандартное приращение: " + str(increment) + ", параметр приращения: " + str(self.currentChangeIndexAndCount) + ", усанавливает текущее ожидание приращения координаты в 0")
    self.currentOffset = 0
    return result
  def resetForNewLineDetection(self):
    self.firstPointValue = None
    self.offsetFromBegin = None
    self.fixedChangeOfCoordinates = [False, False]
    self.strangePoints = []
    self.previousPoint = None
    self.lastNonStrangePoint = None
    self.currentLengthOfTheLine = self.currentLengthOfStrangePointsParts = 0
    self.currentMeasuredLength = 0
  """def resetForNewDetection(self):
    self.coordinatesIncrementFromTheLastCoordinatesChange = None
    self.currentLineCoefficientsIsFixedOnlyBecauseOfTheOverflow = False
    self.strageStartIndexesCount = 0
    self.lastNonStrangePoint = None
    self.strangePoints = []
    self.firstPointValue = None
    self.reset()
  def reset(self):
    self.currentMeasuredLength = 0
    self.previousPoint = self.coordinatesIncrementFromTheLastCoordinatesChange = None
    self.lastDifference = [0, 0]
    if self.coordinatesIncrementFromTheLastCoordinatesChange == None:
      self.coordinatesIncrementFromTheLastCoordinatesChange = self.lastDifference
      self.currentMeasuredLengthFromBegin = self.currentMeasuredLength
  """
  def applyFigure(self, isNewLine = False): #Метод, который устанавливает длину и направления текущей, анализируемой линии, если isNewLine - о фиксирует ё окончательно и создаёт новую
    if isNewLine: #
      if len(self.lines) > 0:
        self.lines[len(self.lines) - 1] = getLineParameters(self.firstPointValue, self.lastNonStrangePoint, self.currentLengthOfTheLine)
        self.lines[len(self.lines) - 1].points = self.points
        self.points = []
        if len(self.lines) > 1:
          self.lines[len(self.lines) - 2].acceleration = (self.lines[len(self.lines) - 2].angle - self.lines[len(self.lines) - 1].angle) / self.lines[len(self.lines) - 2].length
      if (self.strangePoints != None) and (len(self.strangePoints) > 0): #Если есть точки, которые считаются возможной частью следующей линии (из-за отклонений их координат от тех, которые ожидаемы для текущей линии), то обрабатываем их заново "непредвзято" (генерируем новый коэффицинень)
        pointsToProcess = np.copy(self.strangePoints)
      else
        pointsToProcess = []
      self.resetForNewLineDetection()
      self.processPoints(pointsToProcess, self.thisIsEndingPoint())
      self.lastDifference = self.coordinatesIncrementFromTheLastCoordinatesChange = None
      self.currentLineCoefficientsIsFixedOnlyBecauseOfTheOverflow = False
    else:
      self.lines[len(self.lines) - 1] = getLineParameters(self.firstPointValue, self.currentPoint(), self.currentLengthOfTheLine + self.currentLengthOfStrangePointsParts)
      self.lastDifference = getPoint(0, 0)
      self.coordinatesIncrementFromTheLastCoordinatesChange = getPoint(0, 0)
      self.currentMeasuredLengthFromBegin = 0
      self.currentMeasuredLength = 0
    self.previousPoint = None
  def thisIsEndingPoint(self, theValue = None):
    if value != None:
      self._thisIsEndingPoint = theValue
    return value
  def currentPoint(self, value = None):
    if value != None:
      if self.firstPointValue == None:
        self.firstPointValue = value
        self.lines.append(getLineParameters(firstPointValue))
        logThis("Начало обработки, обработка точки " + str(value))        
      else
        logThis("Обработка точки " + str(value))
      self.currentProcessingPoint = value
      self.points.append(value)
    return self.currentProcessingPoint
  def processNewInterval(self, difference, length):
    logThis("Обработка нового приращения: " + str(difference) + " на коэффициенты (длина: " + str(length) + ")")
    isNewLine = self.fixThisIncrementOfTheCoordinatesAsStandardForThisLineIfItIsDidNotFixedYet(difference)
    thisPointIsFixedAsStrange = False
    if isNewLine == None:
      if self.strangePoints != None:
        if len(self.strangePoints) >= ShapeDetector.STRANGE_INDEXES_COUNT_FOR_THE_TOLERATION - 1:
          self.strangePoints = None
          self.currentLengthOfTheLine += self.currentLengthOfStrangePointsParts
          self.currentLengthOfStrangePointsParts = 0
        else
          self.strangePoints.append(self.currentPoint())
          self.currentLengthOfStrangePointsParts += self.currentMeasuredLength          
          thisPointIsFixedAsStrange = True
      isNewLine = False
    elif not(isNewLine):
      self.currentLengthOfTheLine += self.currentLengthOfStrangePointsParts
      self.currentLengthOfStrangePointsParts = 0
      self.strangePoints = []
    if not thisPointIsFixedAsStrange:
      self.currentLengthOfTheLine += self.currentMeasuredLength
      self.lastNonStrangePoint = self.currentPoint()
    self.applyFigure(isNewLine)
    """
    
    if self.currentOffset != None:
      thisOffset = difference[getAntiIndex(self.currentChangeIndexAndCount[0])] / self.currentChangeIndexAndCount[1]
      self.currentOffset += thisOffset
      estimatedOffset = math.floor(self.currentOffset)
      isNewLine = False
      if (estimatedOffset == difference[self.currentChangeIndexAndCount[0]]):
        self.strangePoints = []
        self.lastNonStrangePoint = self.currentPoint()
      elif(isLikableOffset(estimatedOffset, difference[self.currentChangeIndexAndCount[0]])):
        if self.strangePoints == None:
          self.lastNonStrangePoint = self.currentPoint()
        else:
          self.strangePoints.append(self.currentPoint())
          if len(self.strangePoints) >= ShapeDetector.STRANGE_INDEXES_COUNT_FOR_THE_TOLERATION:
            self.strangePoints = None
      else:
        isNewLine = True      
      self.applyFigure(isNewLine)
      self.currentOffset -= difference[self.currentChangeIndexAndCount[0]]
      difference[self.currentChangeIndexAndCount[0]] - thisOffset      
    self.currentOffset = 0
    currentAngle = self.getCurrentAngle()
    angle = getAngle(difference)
    if currentAngle == None:
      self.pushLine(angle, length)
    elif angleIsNear(angle, self.getCurrentAngle()):
      self.continueLine(length)
    else:
    """
  def processPoints(self, points, isEnding = False):
    for index, point in enumerate(points):
      self.processPoint(self, point, isEnding and (index == (len(points) - 1)))
  def processPoint(self, point, isEnding = False):
    self.currentPoint(point)
    self.thisIsEndingPoint(isEnding) #Запись текущий данных (обрабатываемой точки и последняя ли она)
    if self.previousPoint == None: #Если эта точка - новая в фиксации, то фиксируем длину измеряемой линии как 0
      self.lastDifference = getPoint(0, 0)
      self.currentMeasuredLength = 0 #
    else
      self.currentDistance = math.dist(self.previousPoint, point) #Измеряем дистанцию меду текущей и предыдущей точками
      self.currentMeasuredLength += self.currentDistance #Добавляем эту длину к измерямой (общей) длине
      logThis("Измеряемая длина: " + self.currentMeasuredLength)
      difference = point - self.previousPoint #difference - текущее приращение координат точки
      logThis("Текущее приращение: " + str(difference), 1)
      if (difference[0] != 0) and (not self.fixedChangeOfCoordinates[0]):
        logThis("Зафиксировано изменение координаты по \"x\"", 1)
        self.fixedChangeOfCoordinates[0] = True
      if (difference[1] != 0) and (not self.fixedChangeOfCoordinates[1]):
        logThis("Зафиксировано изменение координаты по \"y\"", 1)
        self.fixedChangeOfCoordinates[1] = True       
      currentFixedChangeOfCoordinates = np.copy(self.fixedChangeOfCoordinates)
      self.lastDifference += difference
      logThis("Общее, последнее приращение: " + str(self.lastDifference), 1)
      if self.offsetFromBegin != None:
        self.offsetFromBegin += difference #Добавляем это приращение к общему, если оно есть
        logThis("Увеличивает отступ с начала: " + str(self.offsetFromBegin), 2)
      if (currentFixedChangeOfCoordinates[0] and currentFixedChangeOfCoordinates[1]): #Если зафиксировано изменение обоих координат линии ("x" и "y")
        logThis("Зафиксировано измнение обоих координат", 2)
        if self.offsetFromBegin == None:
          self.offsetFromBegin = getPoint(0, 0)
          self.fixedChangeOfCoordinates = [False, False]
          logThis("Фиксируем эту точку как возможное начало отсчёта для измерения параметров линии", 2)
        elif(self.currentLineCoefficientsIsFixedOnlyBecauseOfTheOverflow)
          logThis("Фиксируем более чётко параметры линии (ранее не удалось их зафиксировать из-за того, что линия не меняла свою абсциссу или ординату слишком долго)", 2)
          self.fixThisIncrementOfTheCoordinatesAsStandardForThisLine(self.offsetFromBegin)
          self.currentLineCoefficientsIsFixedOnlyBecauseOfTheOverflow = False
      if self.coordinatesIncrementFromTheLastCoordinatesChange == None:
        if (currentFixedChangeOfCoordinates[0] and currentFixedChangeOfCoordinates[1]):
          logThis("Начинает отсчитывать приращение с текущей точки", 1)
          self.coordinatesIncrementFromTheLastCoordinatesChange = [0, 0]
          self.currentMeasuredLengthFromBegin = 0
      else
        self.coordinatesIncrementFromTheLastCoordinatesChange += difference
        self.currentMeasuredLengthFromBegin += self.currentDistance
        logThis("Увеличивает приращение с последней точки фиксации на " + str(difference) + ", теперь оно равно: " + str(self.coordinatesIncrementFromTheLastCoordinatesChange) + ", а длина линии увеличивается на " + str(self.currentDistance) + ", и, теперь, она равна " + str(self.currentMeasuredLengthFromBegin), 1)
      if (not (isEnding)) and (self.currentMeasuredLength <= ShapeDetector.INTERVAL[1]):
        logThis("Эта точка - не конечная и длина последней части линии меньше максимальной")
        if self.currentMeasuredLength >= ShapeDetector.INTERVAL[0]:
          logThis("Длина последней части отпезка не меньше минимальной - можем проверить, уи, уже, возмжно сейчас зафиксировать параметры")
          if (self.coordinatesIncrementFromTheLastCoordinatesChange != None) and self.fixedChangeOfCoordinates[0] and self.fixedChangeOfCoordinates[1]:
            logThis("Сравнивем с началом отсчёта, можно зафиксировать часть линии")
            differenceForCompareIsFromBegin = True
          else:
            logThis("Пока рано фиксировать, ждём точки фиксайии или когда длина будет больше максимальной")
            differenceForCompareIsFromBegin = None
        else:
          logThis("Длина последней части линии меньше минимальной - пока рано проводить проверку")
          differenceForCompareIsFromBegin = None
      else:
        logThis("Нужно обазательно зафиксировать параметры, " + ("длина линии боьше максимальной" if (self.currentMeasuredLength <= ShapeDetector.INTERVAL[1]) else "эта точка - конечная в контуре"))
        differenceForCompareIsFromBegin = False
        if not isEnding:
          self.currentLineCoefficientsIsFixedOnlyBecauseOfTheOverflow = True
      if differenceForCompareIsFromBegin != None:
        logThis("Фиксируем эту часть пути для анализа приращения")
        if differenceForCompareIsFromBegin:
          difference = self.coordinatesIncrementFromTheLastCoordinatesChange
          length = self.currentMeasuredLengthFromBegin
        else:
          difference = self.lastDifference
          length = self.currentMeasuredLength
        self.processNewInterval(difference, length)
    self.previousPoint = point
    pushLog()
ShapeDetector.INTERVAL = [3, 7] #Интервал, минимальное и максимальное значение длины для фиксации прямой
ShapeDetector.STRANGE_INDEXES_COUNT_FOR_THE_TOLERATION = 21
print(math.pi + math.pi / 2 + math.pi / 4, [getAngle([2, -2])])