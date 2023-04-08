import math, copy, numpy, cv2, os, sys
from constants import IS_DEBUGGING, MAX_WATERMARK_VALUE, MIN_COEFICIENT_DIFFERENCE_WITH_ONE_TO_DETECT, MIN_WATERMARK_VALUE_FOR_DETECTION, MIN_WATERMARK_VALUE_FOR_DETECTION_GETTER, MAX_COUNT_OF_PIXELS_FOR_DETECT, MIN_WATERMARK_SIZE, MAX_WATERMARK_SIZE, MIN_LETTER_SIZE
from classes import Coordinate, CoordinatesSet, CoordinatesSequence, Pixel, Color, Image, Watermark, Debug, Area, PointsCache
from functions import die, isLikable, arrayIsLikable, haveOneSign, divMaybeOnZero, eachPixelsPair, isUndefined, isDefined, arrayGetAvg, getArrayReprValue, allNoLessThan, clone, arrayDiff, getPointSurrounding, isBetter, purgeFolder, printDebug, outDebug, logThis, haveAlmostOneSign, outForUser, detectColorDifferenceFast, isNotEmptyColorDifference, endProfiling, setFilePathToLog
from arrays import MyArrayListNumeric
import cv2, traceback
try:
  def main():
    FILE_NAME = '1'
    FILE_EXTENSION = 'jpg'
    FILE = '.'.join(FILE_NAME, FILE_EXTENSION)
    FOLDERS_PATH = 'C:\\Работа\\Александр Болтенков\\Водяные знаки\\Изображения\\krisha.kz'
    SOURCES_FOLDER = os.path.join(FOLDERS_PATH, 'Исходные данные')
    RESULTS_FOLDER = os.path.join(FOLDERS_PATH, 'Тестирование')
    img = Image(os.path.join(SOURCES_FOLDER, FILE))
    img.save(os.path.join(RESULTS_FOLDER, FILE))
  theThread = threading.Thread(target=main)
  theThread.start()
  theThread.join()
  die()
except BaseException as error:
  print (error)
  print(''.join(traceback.format_tb(error.__traceback__)))
  die()
try:
  #die(list.__new__([2, 3]))
  try:
    c = Coordinate([2, 3])
    coordinates = [Coordinate([2, 3, 3]), Coordinate([9, 3, 2])]
    theSum = coordinates[0] + coordinates[1]
    def process(*values):
      print(values)
      return values[0] + 1
    die(3 + theSum)
  except IndexError as error:
    print (error)
    print(''.join(traceback.format_tb(error.__traceback__)))
  except BaseException as error:
    print (error)
    print(''.join(traceback.format_tb(error.__traceback__)))
except BaseException as error:
  print (error)
  print(''.join(traceback.format_tb(error.__traceback__)))
die()

