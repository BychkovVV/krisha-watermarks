import math, copy, numpy, cv2, os, sys
from constants import IS_DEBUGGING, MAX_WATERMARK_VALUE, MIN_COEFICIENT_DIFFERENCE_WITH_ONE_TO_DETECT, MIN_WATERMARK_VALUE_FOR_DETECTION, MIN_WATERMARK_VALUE_FOR_DETECTION_GETTER, MAX_COUNT_OF_PIXELS_FOR_DETECT, MIN_WATERMARK_SIZE, MAX_WATERMARK_SIZE, MIN_LETTER_SIZE, CORNER_SIZE, STEP_FOR_DETECTING_LOGO_WATERMARKS_OF_KRISHA_KZ_AT_CORNERS
from classes import Coordinate, CoordinatesSet, CoordinatesSequence, Pixel, Color, Image, Watermark, Debug, Area, PointsCache, LineIterator
from functions import die, isLikable, arrayIsLikable, haveOneSign, divMaybeOnZero, eachPixelsPair, isUndefined, isDefined, arrayGetAvg, getArrayReprValue, allNoLessThan, clone, arrayDiff, getPointSurrounding, isBetter, purgeFolder, printDebug, outDebug, logThis, haveAlmostOneSign, outForUser, detectColorDifferenceFast, isNotEmptyColorDifference, endProfiling, setFilePathToLog
from arrays import MyArrayListNumeric
from main import processImages
import cv2, traceback, threading
FOLDERS_PATH = 'C:\\Работа\\Александр Болтенков\\Водяные знаки\\Изображения\\krisha.kz'
SOURCES_FOLDER = os.path.join(FOLDERS_PATH, 'Исходные данные')
RESULTS_FOLDER = os.path.join(FOLDERS_PATH, 'Тестирование')
    
try:
  def main():
    processImages(SOURCES_FOLDER, RESULTS_FOLDER)
    HEIGHT = img.getHeight()
    theRange = range(HEIGHT - CORNER_SIZE[1], HEIGHT, STEP_FOR_DETECTING_LOGO_WATERMARKS_OF_KRISHA_KZ_AT_CORNERS)

    FILE_NAME = '1'
    FILE_EXTENSION = 'jpg'
    FILE = '.'.join([FILE_NAME, FILE_EXTENSION])
    img = Image(os.path.join(SOURCES_FOLDER, FILE))
    print('16 - initing')
    dd = CoordinatesSequence([[0, 0]])
    img.setColor(CoordinatesSequence([[0, 0]]), [255, 0, 0])
    img.save(os.path.join(RESULTS_FOLDER, FILE))
  theThread = threading.Thread(target=main)
  theThread.start()
  theThread.join()
  die()
except BaseException as error:
  print (error)
  print(''.join(traceback.format_tb(error.__traceback__)))
  die()

