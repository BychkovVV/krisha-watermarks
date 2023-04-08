import copy, numpy, cv2
from functions import die, clone, isNone, isNotNone, isDefined, canHaveProperties, toMyArray, toNumericValueIfItIs, isNumericValue, toIntegerValueIfItIs, isIntegerValue, toNaturalIntegerIfItIs, isNaturalInteger
from common import MyCommonObject
from classes import Color, Coordinate, Area
from arrays import MyArray, ArrayWithNaturalKeys, MyArrayList, MyNumericArray, MyArrayDictionary, MyArraySet
ss = Area()
coordinate1 = Coordinate([0, 0])
ss.push(coordinate1)
print(ss)