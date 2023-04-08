import math, copy, numpy
from common import die, canHaveProperties, MyCommonObject, MyArray
from functions import die, clone, isNone, isNotNone, isDefined, toMyArray, toNumericValueIfItIs, isNumericValue, toIntegerValueIfItIs, isIntegerValue, toNaturalIntegerIfItIs, isNaturalInteger, isLikable, isNumeric, isString, isArray, isScalar, isKey, arrayIsLikable, profilePrint
class ArrayWithNaturalKeys(MyArray):
  def processKey(this, key):
    return toNaturalIntegerIfItIs(key)
  def getNewIndex(this):
    return len(this)
  def push(this, value):
    result = this.getNewIndex()
    this.setValueSimple(result, value)
    return result
  def theExtend(this, values):
    values = type(this)(clone(values))
    for index, value in values:
      this.push(value)    
  def repeat(this, count = 1):
    result = type(this)()
    theRange = range(count)
    for index in theRange:
      result.theExtend(this)
    return result
  def indexOf(value):
    pass    
  def getKeys(this):
    return range(0, this.getNewIndex())
  def __getDefaultValueToFill(this):
    return type(this).DEFAULT_VALUE_TO_FILL
  def onBeforeSettingValue(this, key, value):
    #print("Count: " + str(this.count()));
    #print(this.__getDefaultValueToFill())
    while this.count() <= key:
      this.localPush(this.__getDefaultValueToFill())      
  def __unsetValueSimple(this, key):
    this.pop(key)
ArrayWithNaturalKeys.DEFAULT_VALUE_TO_FILL = None    
class MyArrayList(ArrayWithNaturalKeys, list):
  def localPush(this, value):
    return this.append(value)
  def indexOf(value):
    try:
      result = this.index(value)
    except:
      result = None
    return result
class MyArrayListNumeric(MyArrayList):
  def __eq__(this, other):
    if(isString(other)):
      result = (repr(this) == other)
    elif(isKey(other)):
      type(this).compareCheck(this, other)
      for index, element in this:
        if(element != MyArrayListNumeric.getByIndex(other, index)):
          return False
      return True  
  def __ne__(this, other):
    return not (this == other)
  def __copy__(this):
    return type(this)(list(this))
  def length(this):
    result = 0
    for index, value in this:
      result += value ** 2
    return result ** 0.5
  def __round__(this, *parameters):
    return this.round(*parameters)
  def round(this, *parameters):
    return this.mapByValues(lambda value: round(value, *parameters))
  def ceil(this):
    return this.mapByValues(lambda value: math.ceil(value))
  def floor(this):
    return this.mapByValues(lambda value: math.floor(value))
  def __pos__(this):
    return this.mapByValues(lambda value: + value)
  def __neg__(this):
    return this.mapByValues(lambda value: - value)
  def __abs__(this):
    return this.mapByValues(abs)
  def __add__(this, other):
    if(isString(other)):
      result = repr(this) + other
    elif(isKey(other)):
      result = []
      type(this).compareCheck(this, other)
      for index, element in this:
        result.append(element + MyArrayListNumeric.getByIndex(other, index))
      result = type(this)(result)
    return result
  def __iadd__(this, other):
    if(isKey(other)):
      for index, element in this:
        this[index] += MyArrayListNumeric.getByIndex(other, index)
    return this
  def __radd__(this, other):
    if(isString(other)):
      result = other + repr(this)    
    elif(isNumeric(other)):
      result = this.mapByValues(lambda value: other + value)    
    return result
  def __sub__(this, other):
    if(isKey(other)):
      result = []
      type(this).compareCheck(this, other)
      for index, element in this:
        result.append(element - MyArrayListNumeric.getByIndex(other, index))
      result = type(this)(result)
    return result
  def __isub__(this, other):
    if(isKey(other)):
      for index, element in this:
        this[index] -= MyArrayListNumeric.getByIndex(other, index)
    return this
  def __rsub__(this, other):
    if(isNumeric(other)):
      result = this.mapByValues(lambda value: other - value)    
    return result
  def __mul__(this, other):
    if(isNumeric(other)):
      result = []
      type(this).compareCheck(this, other)
      for index, element in this:
        result.append(element * MyArrayListNumeric.getByIndex(other, index))
      result = type(this)(result)
    return result
  def __imul__(this, other):
    if(isNumeric(other)):
      for index, element in this:
        this[index] *= MyArrayListNumeric.getByIndex(other, index)
    return this
  def __rmul__(this, other):
    if(isNumeric(other)):
      result = this.mapByValues(lambda value: other * value)    
    return result
  def __truediv__(this, other):
    if(isNumeric(other)):
      result = []
      type(this).compareCheck(this, other)
      for index, element in this:
        result.append(element / MyArrayListNumeric.getByIndex(other, index))
      result = type(this)(result)
    return result
  def __itruediv__(this, other):
    if(isNumeric(other)):
      for index, element in this:
        this[index] /= MyArrayListNumeric.getByIndex(other, index)
    return this
  def __rtruediv__(this, other):
    if(isNumeric(other)):
      result = this.mapByValues(lambda value: other / value)    
    return result
  def getSum(this):
    result = 0
    for value in this.getValues():
      result += value
    return result
  def getAverage(this):
    return this.getSum() / len(this)
  def hasLikableValues(this, maxError = None):
    averageValue = this.getAverage()
    return this.any(lambda value: isLikable(valueaverageValue, maxError))
def getByIndexInArray(value, index):
  return value[index] if isArray(value) else value
MyArrayListNumeric.getByIndex = getByIndexInArray
class MyNumericArray(ArrayWithNaturalKeys, numpy.ndarray):
  def __new__(classes, value = None):
    return numpy.asarray(value).view(classes)
  def localPush(this, value):
    #print("Before", this, value)
    result = len(this)
    this.put(result, value, mode = "clip")
    #print("After", result, this)
    return result
  def __getDefaultValueToFill(this):
    if this.shape[0] == 0:
      result = 0
    elif len(this.shape) == 1:
      result = this[0]
    else:
      result = numpy.zeros_like(this[0])
    return result
  def indexOf(value):
    result = numpy.argwhere(this==value)
    if len(result) == 0:
      result = None
    else:
      result = result[0]
    if len(result) == 0:
      result = None
    else:
      result = result[0]
    return result
MyNumericArray.DEFAULT_VALUE_TO_FILL = 0
class MyArrayTuple(ArrayWithNaturalKeys, tuple):
  pass
class MyArrayDictionary(MyArray, dict):
  def getKeys(this):
    return MyArrayList(this.list()) 
class MyArraySet(MyArray, set):
  def __iter__(this, *values, **theValues):
    return super(MyCommonObject, this).__iter__(*values, **theValues)
  def __next__(this):
    #print('Suer next: {}'.format(super(type(this), MyArraySet).__next__))
    #die(list(super(set, this)))
    theNextValue = super(MyCommonObject, this).__next()
    print('this.current_index - {}, c: {}'.format(this.current_index, this.getCount()))
    if this.current_index >= this.getCount():
      print('raised in set')
      raise StopIteration
      #profilePrint('It')
      return None
    return theNextValue
  def push(this, value):
    return this.setTheValue(value, True)
  def getKeys(this):
    return list(set(this))
    result = MyArrayList()
    for key in set(this):
      result.append(key)
    return result
  def getValues(this):
    theCount = this.getCount()
    if theCount not in MyArraySet.valuesForCounts:
      MyArraySet.valuesForCounts[theCount] = MyArrayList([True]).repeat(this.getCount())
    return MyArraySet.valuesForCounts[theCount] 
  def __unsetValueSimple(this, key):
    this.remove(key)
  def getValueSimple(this, key, defaultValue = None):
    return True if this.issetValueSimple(key) else defaultValue
  def setTheValue(this, key, value):
    this.add(key)
MyArraySet.valuesForCounts = dict()
#elements = MyNumericArray([3, 4])
#elements.setValueSimple(12, 3)
#print(elements + 3)