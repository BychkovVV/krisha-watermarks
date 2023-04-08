import math, os, numpy
from functions import isUndefined, isDefined, isLikable, getMultiRange, isBetter, printDebug, outDebug, die
from constants import KRISHA_WATERMARK_AT_CENTER_MAX_SIZE, MIN_WATERMARK_SIZE, MAX_WATERMARK_SIZE, CORNER_SIZE, X_STEP, BLACKCOEF_POSSIBLE_INTERVAL, WHITECOEF_POSSIBLE_INTERVAL, DEBUG_IS_ON
from classes import Debug, Coordinate, CoordinatesSet, Image
FOLDERS = {'WORK': 'C:\\Users\\Administrator\\Desktop\\Работа'}
FOLDERS['IMAGES'] = os.path.join(FOLDERS['WORK'], 'Изображения')
FOLDERS['IMAGE_SOURCES'] = os.path.join(FOLDERS['IMAGES'], 'Исходные данные')
FOLDERS['IMAGE_TARGETS'] = os.path.join(FOLDERS['IMAGES'], 'Результаты')
FOLDERS['IMAGE_PROCESSING'] = os.path.join(FOLDERS['IMAGES'], 'Обработка')
MAX_COEFS_COMPARE_ERROR = 0.05
MAX_COEFS_ERRORS = [0.05, 0.05]
def getColorDifferenceCoefficient(oldColor, newColor, maxCoefsError = MAX_COEFS_ERRORS[0]):
  theMaxColorValue = max(oldColor)
  oldColorAsFloat = float(oldColor[0]), float(oldColor[1]), float(oldColor[2])
  newColorAsFloat = float(newColor[0]), float(newColor[1]), float(newColor[2])  
  printDebug('Comparing colors {} and {}', oldColor, newColor)
  if newColorAsFloat[0] > oldColorAsFloat[0]:
    printDebug('This can be white watermark')
    diff = 255 - theMaxColorValue
    printDebug('Capacity for whiting: {}', diff)
    if diff == 0:
      printDebug('Zero, so not fixing it')
      return None
    coef1 = float((newColorAsFloat[0] - oldColorAsFloat[0]) / diff)
    printDebug('Coefficient1 = ((new red = {}) - (old red = {})) / (diff = {}) = {} / (diff = {}) = {}', newColor[0], oldColor[0], diff, int(newColorAsFloat[0] - oldColorAsFloat[0]), diff, coef1)
    if (coef1 < WHITECOEF_POSSIBLE_INTERVAL[0]):
      printDebug('Is less than possible coefficient for the white watermark aviable ({}), so not fixing it here', WHITECOEF_POSSIBLE_INTERVAL[0])
      return None
    if (coef1 > WHITECOEF_POSSIBLE_INTERVAL[1]):
      printDebug('Is more than possible coefficient for the white watermark aviable ({}), so not fixing it here', WHITECOEF_POSSIBLE_INTERVAL[1])
      return None
    coef2 = float((newColorAsFloat[1] - oldColorAsFloat[1]) / diff)
    printDebug('Coefficient2 = ((new green = {}) - (old green = {})) / (diff = {}) = {} / (diff = {}) = {}', newColor[1], oldColor[1], diff, int(newColorAsFloat[1] - oldColorAsFloat[1]), diff, coef2)
    if (coef2 < WHITECOEF_POSSIBLE_INTERVAL[0]):
      printDebug('Is less than possible coefficient for the white watermark aviable ({}), so not fixing it here', WHITECOEF_POSSIBLE_INTERVAL[0])
      return None
    if (coef2 > WHITECOEF_POSSIBLE_INTERVAL[1]):
      printDebug('Is more than possible coefficient for the white watermark aviable ({}), so not fixing it here', WHITECOEF_POSSIBLE_INTERVAL[1])
      return None
    if ((coef2 - coef1) < - maxCoefsError):
      printDebug('Coefficient for green ({}) is less than coefficient for red ({}) on more, than max possible coefficients difference for differents color ({}), so not fixing this difference as possible watermark', coef2, coef1, maxCoefsError)
      return None
    if ((coef2 - coef1) > maxCoefsError):
      printDebug('Coefficient for green ({}) is more than coefficient for red ({}) on more, than max possible coefficients difference for differents color ({}), so not fixing this difference as possible watermark', coef2, coef1, maxCoefsError)
      return None
    coef3 = float((newColorAsFloat[2] - oldColorAsFloat[2]) / diff)
    printDebug('Coefficient3 = ((new blue = {}) - (old blue = {})) / (diff = {}) = {} / (diff = {}) = {}', newColor[2], oldColor[2], diff, int(newColorAsFloat[2] - oldColorAsFloat[2]), diff, coef3)
    
    if (coef3 < WHITECOEF_POSSIBLE_INTERVAL[0]) or (coef3 > WHITECOEF_POSSIBLE_INTERVAL[1]) or ((coef3 - coef2) < - maxCoefsError) or (coef3 - coef2 > maxCoefsError):
      return None
    if (coef3 < WHITECOEF_POSSIBLE_INTERVAL[0]):
      printDebug('Is less than possible coefficient for the white watermark aviable ({}), so not fixing it here', WHITECOEF_POSSIBLE_INTERVAL[0])
      return None
    if (coef3 > WHITECOEF_POSSIBLE_INTERVAL[1]):
      printDebug('Is more than possible coefficient for the white watermark aviable ({}), so not fixing it here', WHITECOEF_POSSIBLE_INTERVAL[1])
      return None
    if ((coef3 - coef2) < - maxCoefsError):
      printDebug('Coefficient for blue ({}) is less than coefficient for green ({}) on more, than max possible coefficients difference for differents color ({}), so not fixing this difference as possible watermark', coef3, coef2, maxCoefsError)
      return None
    if ((coef3 - coef2) > maxCoefsError):
      printDebug('Coefficient for blue ({}) is more than coefficient for green ({}) on more, than max possible coefficients difference for differents color ({}), so not fixing this difference as possible watermark', coef3, coef2, maxCoefsError)
      return None    
    result = coef1
    printDebug('Possible white watermark detected here with coefficient {}', coef1)
  else:
    printDebug('This can be black watermark')
    diff = theMaxColorValue
    printDebug('Capacity for darking: {}', diff)
    if diff == 0:
      printDebug('Zero, so not fixing it')
      return None
    coef1 = float((oldColorAsFloat[0] - newColorAsFloat[0]) / diff)
    printDebug('Coefficient1 = ((old red = {}) - (new red = {})) / (diff = {}) = {} / (diff = {}) = {}', oldColor[0], newColor[0], diff, int(oldColorAsFloat[0] - newColorAsFloat[0]), diff, coef1)
    if (coef1 < BLACKCOEF_POSSIBLE_INTERVAL[0]):
      printDebug('Is less than possible coefficient for the black watermark aviable ({}), so not fixing it here', BLACKCOEF_POSSIBLE_INTERVAL[0])
      #printDebug('({}, {} (type: {}) < {} (type: {})) Is less than possible coefficient for the black watermark aviable ({}), so not fixing it here', (coef1 < BLACKCOEF_POSSIBLE_INTERVAL[0]), coef1, type(coef1), BLACKCOEF_POSSIBLE_INTERVAL[0], type(BLACKCOEF_POSSIBLE_INTERVAL[0]), BLACKCOEF_POSSIBLE_INTERVAL[0])
      return None
    if (coef1 > BLACKCOEF_POSSIBLE_INTERVAL[1]):
      printDebug('Is more than possible coefficient for the black watermark aviable ({}), so not fixing it here', BLACKCOEF_POSSIBLE_INTERVAL[1])
      return None
    coef2 = float((oldColorAsFloat[1] - newColorAsFloat[1]) / diff)
    printDebug('Coefficient2 = ((old green = {}) - (new green = {})) / (diff = {}) = {} / (diff = {}) = {}', oldColor[1], newColor[1], diff, int(oldColorAsFloat[1] - newColorAsFloat[1]), diff, coef2)
    if (coef2 < BLACKCOEF_POSSIBLE_INTERVAL[0]):
      printDebug('Is less than possible coefficient for the black watermark aviable ({}), so not fixing it here', BLACKCOEF_POSSIBLE_INTERVAL[0])
      return None
    if (coef2 > BLACKCOEF_POSSIBLE_INTERVAL[1]):
      printDebug('Is more than possible coefficient for the black watermark aviable ({}), so not fixing it here', BLACKCOEF_POSSIBLE_INTERVAL[1])
      return None
    if ((coef2 - coef1) < - maxCoefsError):
      printDebug('Coefficient for green ({}) is less than coefficient for red ({}) on more, than max possible coefficients difference for differents color ({}), so not fixing this difference as possible watermark', coef2, coef1, maxCoefsError)
      return None
    if ((coef2 - coef1) > maxCoefsError):
      printDebug('Coefficient for green ({}) is more than coefficient for red ({}) on more, than max possible coefficients difference for differents color ({}), so not fixing this difference as possible watermark', coef2, coef1, maxCoefsError)
      return None
    coef3 = float((oldColorAsFloat[2] - newColorAsFloat[2]) / diff)
    printDebug('Coefficient3 = ((old blue = {}) - (new blue = {})) / (diff = {}) = {} / (diff = {}) = {}', oldColor[2], newColor[2], diff, int(oldColorAsFloat[2] - newColorAsFloat[2]), diff, coef3)
    if (coef3 < BLACKCOEF_POSSIBLE_INTERVAL[0]):
      printDebug('Is less than possible coefficient for the black watermark aviable ({}), so not fixing it here', BLACKCOEF_POSSIBLE_INTERVAL[0])
      return None
    if (coef3 > BLACKCOEF_POSSIBLE_INTERVAL[1]):
      printDebug('Is more than possible coefficient for the black watermark aviable ({}), so not fixing it here', BLACKCOEF_POSSIBLE_INTERVAL[1])
      return None
    if ((coef3 - coef2) < - maxCoefsError):
      printDebug('Coefficient for blue ({}) is less than coefficient for green ({}) on more, than max possible coefficients difference for differents color ({}), so not fixing this difference as possible watermark', coef3, coef2, maxCoefsError)
      return None
    if ((coef3 - coef2) > maxCoefsError):
      printDebug('Coefficient for blue ({}) is more than coefficient for green ({}) on more, than max possible coefficients difference for differents color ({}), so not fixing this difference as possible watermark', coef3, coef2, maxCoefsError)
      return None
    result = - coef1
    printDebug('Possible black watermark detected here with coefficient {}', coef1)
  return result
def processImageSide(img, side, whiteCoefficients, blackCoefficients):
  theXStart = side[0][0]
  theYStart = side[1][0]
  theXRange = range(theXStart, theXStart + side[0][1])
  theYRange = range(theYStart, theYStart + side[1][1])
  openedCoefficients = []
  theQuantity = 0
  for y in theYRange:
    x = theXRange.start
    x2 = theXRange.start + X_STEP
    while(x2 < theXRange.stop):
      color1 = img.getColorFast((x, y))
      for otherX in range(x + 1, x2 + 1):
        color2 = img.getColorFast((otherX, y))
        openCoef = getColorDifferenceCoefficient(color1, color2, 0)
        closeCoef = getColorDifferenceCoefficient(color2, color1, 0)
        if isDefined(openCoef) or isDefined(closeCoef):
          img.setColorFast((x, y), (0, 0, 255))
          theQuantity += 1
          break
      currentXStep = 1
      x += currentXStep
      x2 += currentXStep
      continue
      color1 = img.getColorFast((x, y))
      color2 = img.getColorFast((x2, y))
      printDebug('Compareing {} (Color: {}) and {} (Color: {})', (x, y), color1, (x2, y), color2)
      printDebug('Possible watermark start possitions: {}', list(map(lambda value: ((value[1], y), value[0]), filter(lambda value: x - value[1] <= MAX_WATERMARK_SIZE[0], openedCoefficients))))
      openCoef = getColorDifferenceCoefficient(color1, color2, MAX_COEFS_ERRORS[0])
      closeCoef = getColorDifferenceCoefficient(color2, color1, MAX_COEFS_ERRORS[1])
      printDebug('Open coef: {}, close coef: {}', openCoef, closeCoef)
      currentXStep = None
      if openCoef != None:
        openedCoefficients.insert(0, [openCoef, x])
        printDebug('Adding possible watermark start point ({}), new possible start points: {}', (x, y), openedCoefficients)
        currentXStep = X_STEP
      if closeCoef != None:
        theMinX = max(0, x - MAX_WATERMARK_SIZE[0])
        theMaxX = max(0, x - MIN_WATERMARK_SIZE[0])            
        printDebug('Looking for close for this opening coefficient, in interval {} - {}', (theMinX, y), (theMaxX, y))
        firstIndexToRemove = None
        chosenOpenedIndex = None
        for openedIndex, theOpened in enumerate(openedCoefficients):
          printDebug('Is coefficient {} at {} is opening for current close?', (theOpened[1], y), theOpened[0])
          if theOpened[1] < theMinX:
            printDebug('This coefficient is out of possible limits, exiting searching for start loop and removing this and all next starts (Thay are out of max width)')
            firstIndexToRemove = openedIndex
            break
          if isLikable(theOpened[0], closeCoef, MAX_COEFS_COMPARE_ERROR):
            printDebug('This is possible start, we found possible start coefficient, existing the loop')
            chosenOpenedIndex = openedIndex
            break
        if chosenOpenedIndex != None:
          openedCoefficient = openedCoefficients[chosenOpenedIndex]
          xStart = openedCoefficient[1] 
          if xStart <= theMaxX:
            printDebug('The start point is not thinner than minimum watermark width ({})', MIN_WATERMARK_SIZE[0])
            if closeCoef > 0:
              whiteCoefficients[xStart][y] = closeCoef
              whiteCoefficients[x2][y] = - closeCoef
              img.setColorFast((xStart, y), (0, 0, 255))
              printDebug('Point {} is added as start for this white watermark (coefficient: {})', (xStart, y), closeCoef)
              img.setColorFast((x2, y), (0, 255, 0))
              printDebug('Point {} is added as end', (x2, y))
            else:
              blackCoefficients[openedCoefficients[chosenOpenedIndex][1]][y] = - closeCoef 
              blackCoefficients[x2][y] = closeCoef
              img.setColorFast((xStart, y), (120, 120, 255))
              printDebug('Point {} is added as start for this black watermark (coefficient: {})', (xStart, y), - closeCoef)
              img.setColorFast((x2, y), (255, 0, 0))
              printDebug('Point {} is added as end for this black watermark', (x2, y))
            currentXStep = X_STEP
            theQuantity += 1
          else:
            printDebug('Point {} is opens watermark, that is too thin, not adding this', (xStart, y))
          printDebug('Removing all possible start points, that is not after chosen one (thay are: {})', list(map(lambda element: ((element[1], y), element[0]), openedCoefficients[0:chosenOpenedIndex + 1])))
          openedCoefficients = openedCoefficients[chosenOpenedIndex + 1:]
          printDebug('New open points: {}', list(map(lambda element: ((element[1], y), element[0]), openedCoefficients)))
        elif firstIndexToRemove != None:
          printDebug('Removing all possible start points, that is too far away: {}', list(map(lambda element: ((element[1], y), element[0]), openedCoefficients[firstIndexToRemove:])))
          openedCoefficients = openedCoefficients[0:firstIndexToRemove]
          printDebug('New open points: {}', list(map(lambda element: ((element[1], y), element[0]), openedCoefficients)))
      if isUndefined(currentXStep):
        currentXStep = 1
      x += currentXStep
      x2 += currentXStep
      outDebug()
  return theQuantity  
def logCurrent(value, *elements):
  if len(elements) > 0:
    value = value.format(*elements)
  print(value)
def main():
  files = os.listdir(FOLDERS['IMAGE_SOURCES'])
  SIDES = ((1, 1), (0, 1), (1, 0), (0, 0))
  for file in files:
    logCurrent('Processing {}', file)
    img = Image(os.path.join(FOLDERS['IMAGE_SOURCES'], file))
    SIZE = list(img.inColor.shape)[1::-1]
    STEPS = (SIZE[0] - CORNER_SIZE[0], SIZE[1] - CORNER_SIZE[1])
    whiteCoefficients = numpy.zeros(SIZE, numpy.float64)
    blackCoefficients = numpy.zeros(SIZE, numpy.float64)
    chosenSideAndCount = [None, None]
    for element in SIDES:
      logCurrent('Processing side {}', element)
      theXStart = element[0] * STEPS[0]
      theYStart = element[1] * STEPS[1]
      theXRange = range(theXStart, theXStart + CORNER_SIZE[0])
      theYRange = range(theYStart, theYStart + CORNER_SIZE[1])
      theCount = processImageSide(img, [[theXStart, CORNER_SIZE[0]], [theYStart, CORNER_SIZE[1]]], whiteCoefficients, blackCoefficients)
      logCurrent('Processed, count: {}', theCount)
      if isBetter(theCount, chosenSideAndCount[1], True):
        chosenSideAndCount = [element, theCount]
      if DEBUG_IS_ON:
        break
    if not DEBUG_IS_ON:
      startPosition = math.floor((SIZE[0] - KRISHA_WATERMARK_AT_CENTER_MAX_SIZE[0]) / 2), math.floor((SIZE[1] - KRISHA_WATERMARK_AT_CENTER_MAX_SIZE[1]) / 2)
      logCurrent('Processing center')
      theCount = processImageSide(img, [[startPosition[0], KRISHA_WATERMARK_AT_CENTER_MAX_SIZE[0]], [startPosition[1], KRISHA_WATERMARK_AT_CENTER_MAX_SIZE[1]]], whiteCoefficients, blackCoefficients)
      logCurrent('Processed, count: {}', theCount)    
    img.save(os.path.join(FOLDERS['IMAGE_PROCESSING'], file + '.png'))
    if DEBUG_IS_ON:
      break
    
    #die(img.inColor)
    print('Processing {}'.format(file))
    Image.drawCountours(os.path.join(FOLDERS['IMAGE_SOURCES'], file), os.path.join(FOLDERS['IMAGE_TARGETS'], file))
    print('Processed {}'.format(file))
    Debug.stopProfiling()
    break
  """os.path.processImages('')
  Image.drawCountours
  Image.drawCountours('../test.png', '../test-result.png')
  ind = [None]
  dd = [2, 3]
  for ind[0] in dd:
    print(ind)
  print('START')
  img = Image('test.png')
  contours = img.getCountours()
  img.setColor(contours, [255, 0, 0])
  img.save('test-result.png')
  """