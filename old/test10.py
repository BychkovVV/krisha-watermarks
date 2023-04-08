import math, copy, numpy, cv2, os, sys
from constants import IS_DEBUGGING, MAX_WATERMARK_VALUE, MIN_COEFICIENT_DIFFERENCE_WITH_ONE_TO_DETECT, MIN_WATERMARK_VALUE_FOR_DETECTION, MIN_WATERMARK_VALUE_FOR_DETECTION_GETTER, MAX_COUNT_OF_PIXELS_FOR_DETECT, MIN_WATERMARK_SIZE, MAX_WATERMARK_SIZE, MIN_LETTER_SIZE
from classes import Coordinate, Pixel, Color, Image, Watermark, Debug, Area, PointsCache
from functions import die, isLikable, arrayIsLikable, haveOneSign, divMaybeOnZero, eachPixelsPair, isUndefined, isDefined, arrayGetAvg, getArrayReprValue, allNoLessThan, clone, arrayDiff, getPointSurrounding, isBetter, purgeFolder, printDebug, outDebug, logThis, haveAlmostOneSign, outForUser, detectColorDifferenceFast, isNotEmptyColorDifference, endProfiling, setFilePathToLog
from arrays import MyArrayListNumeric
import cv2, traceback, atexit, threading
try:
  def main():
    class Derrived(list):
      def __init__(this, value):
        print("Value", value)
    class Derrived2(Derrived):
      def __init__(this, value):
        print("Value2", value)
    d = Derrived2([2])
    print(d)
  theThread = threading.Thread(target=main)
  theThread.start()
  theThread.join()
  die()
except BaseException as error:
  print (error)
  print(''.join(traceback.format_tb(error.__traceback__)))
  die()