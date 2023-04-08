import math, copy, numpy, cv2, os, sys
from constants import IS_DEBUGGING, MAX_WATERMARK_VALUE, MIN_COEFICIENT_DIFFERENCE_WITH_ONE_TO_DETECT, MIN_WATERMARK_VALUE_FOR_DETECTION, MIN_WATERMARK_VALUE_FOR_DETECTION_GETTER, MAX_COUNT_OF_PIXELS_FOR_DETECT, MIN_WATERMARK_SIZE, MAX_WATERMARK_SIZE, MIN_LETTER_SIZE, CORNER_SIZE, STEP_FOR_DETECTING_LOGO_WATERMARKS_OF_KRISHA_KZ_AT_CORNERS
from classes import Coordinate, CoordinatesSet, CoordinatesSequence, Pixel, Color, Image, Watermark, Debug, Area, PointsCache, LineIterator
from functions import die, isLikable, arrayIsLikable, haveOneSign, divMaybeOnZero, eachPixelsPair, isUndefined, isDefined, arrayGetAvg, getArrayReprValue, allNoLessThan, clone, arrayDiff, getPointSurrounding, isBetter, purgeFolder, printDebug, outDebug, logThis, haveAlmostOneSign, outForUser, detectColorDifferenceFast, isNotEmptyColorDifference, endProfiling, setFilePathToLog
from arrays import MyArrayListNumeric
import cv2, traceback, threading
def processImages(source, distination):
  files = os.listdir(source)
  for file in files:
    image = Image(os.path.join(source, file))
    result = Image(os.path.join(source, file))
    pathToTheResult = os.path.join(distination, file)
    HEIGHT = image.getHeight()
    xCornersRange = range(1, -1, -1)
    yCornersRange = range(1, -1, -1)
    for xIndex in xCornersRange:
      xStart = (WIDTH - 1) * xIndex
      angle = xIndex * math.pi
        
      for yIndex in yCornersRange:
        yStart = (HEIGHT - CORNER_SIZE[1]) * yIndex
        theRange = range(yStart, yStart + CORNER_SIZE[1],   STEP_FOR_DETECTING_LOGO_WATERMARKS_OF_KRISHA_KZ_AT_CORNERS)
        for theY in theRange:
          theLineIterator LineIterator(Coordinate([xStart, theY]), angle, CORNER_SIZE[0])
          
        theStartPoint = Coordinate([RIGHTX, ])
        theLine = LineIterator(start, coef)
    FILE_NAME = '1'
    FILE_EXTENSION = 'jpg'
    FILE = '.'.join([FILE_NAME, FILE_EXTENSION])
    FOLDERS_PATH = 'C:\\Работа\\Александр Болтенков\\Водяные знаки\\Изображения\\krisha.kz'
    SOURCES_FOLDER = os.path.join(FOLDERS_PATH, 'Исходные данные')
    RESULTS_FOLDER = os.path.join(FOLDERS_PATH, 'Тестирование')
    img = Image(os.path.join(SOURCES_FOLDER, FILE))
    print('16 - initing')
    dd = CoordinatesSequence([[0, 0]])
    img.setColor(CoordinatesSequence([[0, 0]]), [255, 0, 0])
    img.save(os.path.join(RESULTS_FOLDER, FILE))

