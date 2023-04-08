from threading import Timer
import copy, numpy
import cProfile
import pstats
import io
from pstats import SortKey
from datetime import datetime
def isDefined(value):
  return isNotNone(value)
def isUndefined(value):
  return isNone(value)
def isBoolean(value):
  return isinstance(value, bool)
def isScalar(value):
  return isNumeric(value) or isString(value) or isBoolean(value)
def isArray(value):
  return isinstance(value, list) or isinstance(value, set) or isinstance(value, tuple) or isinstance(value, dict) or isinstance(value, numpy.ndarray)
def isKey(value):
  return isScalar(value) or isArray(value)
def isNumeric(value):
  return isinstance(value, int) or isinstance(value, float) or isinstance(value, complex)
def isString(value):
  return isinstance(value, str)
def die(message = None):
  global theTimer
  if(isDefined(message)):
    print(message)
  #traceback.print_stack()
  #theTimer.cancel()
  quit()
def outStatus():
  global theTimer
  ob.disable()
  outProfile()
  #ps.dump_stats('C:\\Users\\vv\\Desktop\\Работа\\profiles\\status-{}-{}-{}.txt'.format(int(now.hour), int(now.minute), int(now.second)))
  #ob.enable()
  #theTimer = Timer(30, outStatus)
  #theTimer.start()
def startProfile():
  global ob
  ob = cProfile.Profile()
  ob.enable()
def stopProfile():
  global ob
  now = datetime.now()
  path = 'C:\\Users\\vv\\Desktop\\Работа\\profiles\\status-the-time-{}-{}-{}.txt'.format(int(now.hour), int(now.minute), int(now.second))
  with open(path, 'w') as stream:
    sec = io.StringIO()
    sortby = SortKey.TIME;#CUMULATIVE
    ps = pstats.Stats(ob, stream = stream).sort_stats(sortby)
    ps.print_stats()
  """path = 'C:\\Users\\vv\\Desktop\\Работа\\profiles\\status-time-{}-{}-{}.txt'.format(int(now.hour), int(now.minute), int(now.second))
  with open(path, 'w') as stream:
    sec = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(ob, stream = stream).sort_stats(sortby)
    ps.print_stats()
  """
class Debug:
  pass
Debug.startProfiling = startProfile
Debug.stopProfiling = stopProfile
def profilePrint(value, *values):
  if len(values) > 0:
    value = str(value).format(*values)
  print(value)
  input()
def endProfiling():
  ob.disable()
  sec = io.StringIO()
  sortby = SortKey.CUMULATIVE
  ps = pstats.Stats(ob, stream=sec).sort_stats(sortby)
  ps.print_stats()
  print(sec.getvalue())
  die()
#theTimer = Timer(30, outStatus)
#theTimer.start()
def canHaveProperties(value):
  return isinstance(value, list) or isinstance(value, tuple) or isinstance(value, set) or isinstance(value, dict) or isinstance(value, numpy.ndarray)
def clone(value):
  return copy.copy(value)
def isNone(value):
  return value is None
def isNotNone(value):
  return not isNone(value)

class MyCommonObject(object):
  theId = None
  values = None
  def __init__(this, value1 = None, value2 = None, value3 = None):
    this.theId = MyCommonObject.id
    MyCommonObject.id += 1
    if(canHaveProperties(value1)):
      this.values = value1
    else:
      this.values = []
      if(value1 != None):
        this.values.append(value1)
      if(value2 != None):
        this.values.append(value2)
      if(value3 != None):
        this.values.append(value3)
MyCommonObject.id = 0
class MyArray(MyCommonObject):
  current_index = 0
  def processKey(this, key):
    return key
  def getCount(this):
    return super(MyCommonObject, this).__len__()
  def count(this):
    return this.getCount()
  def __init__(this, values = None):
    #if this.theId == 333:
      #print('Constructor launched, type of this: {}, values: {}'.format(type(this), values))
    this.current_index = 0
    this.values = values
    superMethod = MyArray.getSuperMethod(this)
    #if this.theId == 333:
      #print('Super method: {}'.format(superMethod))
    if values is None:
      superMethod(this, [])
    elif not(isinstance(this, numpy.ndarray)):
      #print(superMethod)
      if this.theId == 333:
        pass
        #print('Super method: {}, values: {}'.format(superMethod, arrayGetValues(values)))
      superMethod(this, arrayGetValues(values))
    #print(len(this))
    if this.theId == 333:
      pass
      #print('this - {}, values: {}'.format(this, arrayGetValues(values)))
  def getKeyIndex(this, key):
    key = this.processKey(key)
    return this.getKeys().indexOf(key) if isDefined(key) else None
  def getValueIndex(this, value):
    return this.getValues().indexOf(value)
  def hasKey(this, key):
    return isDefined(this.getKeyIndex(key))
  def hasValue(this, value):
    return isDefined(this.getValueIndex(value))
  def issetValueSimple(this, key):
    return this.hasKey(key)
  def __unsetValueSimple(this, key):
    del this[key]
  def unsetValueSimple(this, key):
    if this.issetValueSimple(key):
      this.__unsetValueSimple(this.processKey(key))
      result = True
    else:
      result = False
    return result    
  def getValueSimple(this, key, defaultValue = None):
    if this.issetValueSimple(key):
      result = this[this.processKey(key)]
    else:
      result = defaultValue
    return result
  def onBeforeSettingValue(this, key, value):
    #print(type(this))
    pass
  def setTheValue(this, key, value):
    this[key] = value
  def onAfterSettingValue(this, key, value):
    pass
  def setValueSimple(this, key, value):
    key = this.processKey(key)
    if isDefined(key):
      this.onBeforeSettingValue(key, value)
      this.setTheValue(key, value)
      this.onAfterSettingValue(key, value)
      result = True
    else:
      result = False
    return result
  def mergeWith(this, element):
    result = clone(this)
    element = toMyArray(element)
    for key, value in element:
      result.setVarSimple(key, value)
    return result
  def __iter__(this):
    this.current_index = 0
    return this
  def __next__(this):
    #print(this.current_index, this.getCount(), this.current_index >= this.getCount())
    #print('this.current_index - {}'.format(this.current_index))
    if this.current_index >= this.getCount():
      
      raise StopIteration
      result = None
    else:
      result = (this.getKeys()[this.current_index], this.getValues()[this.current_index])
      this.current_index += 1
    return result
  def getKeys(this):
    result = []
    for index, value in enumerate(this):
      result.append(index)
    return result
  def getValues(this):
    keys = this.getKeys()
    theRange = range(len(keys))
    result = []
    for index in theRange:
      result.append(this[keys[index]])
    return result
  def removeByIndexes(this, indexes):
    indexes = toNumericArray(indexes)
    indexes.sort().flip()
    for index in indexes:
      if(len(this) > index):
        this.removeByIndex(index)
    return this
  def removeByIndex(index):
    pass
  def isSame(this):
    result = None
    valueToCompare = None
    for key, value in this:
      if valueToCompare == None:
        valueToCompare = element
      elif value != valueToCompare:
        result = False
      if result != None:
        break
    return ifNone(result, True)
  def any(this, handler):
    result = None
    for key, value in this:
      if(handler(value, key)):
        result = True
      if result != None:
        break
    return ifNone(result, False)
  def filterNonZeroValues():
    return this.filter(bindFunctionTo(isNotZero, 1)).map(bindFunctionTo(getSign, 1))
  def all(this, handler):
    result = None
    for index, element in enumerate(this):
      if not (handler(element, index)):
        result = False
      if result != None:
        break
    if result == None:
      result = True
    return result
  def mapByValues(this, handler):
    return this.map(lambda value, index: handler(value))
  def map(this, handler):
    result = type(this)()
    for index, element in this:
      result.push(handler(element, index))
    return result
  def any(this, handler):
    result = None
    for index, element in enumerate(this):
      if(handler(element, index)):
        result = True
      if result != None:
        break
    if result == None:
      result = True
    return result
  def all(this, handler):
    result = None
    for element in this:
      if(not handler(element)):
        result = False
      if result != None:
        break
    if result == None:
      result = True
    return result
  def filter(this, handler):
    result = getSameTypeArray(this)
    for index, element in enumerate(this):
      if(handler(element, index)):
        result.push(element)    
    return result
def myArrayGetSuperValue(element):
  if(isinstance(element, tuple)):
    result = tuple
  elif(isinstance(element, set)):
    result = set
  elif(isinstance(element, list)):
    result = list
  elif(isinstance(element, dict)):
    result = dict
  elif(isinstance(element, numpy.ndarray)):
    result = numpy.ndarray
  else:
    result = None
  return result  
MyArray.getSuperValue = myArrayGetSuperValue
def compareCheckListsForCoordinate(value1, value2):
  if(isArray(value1) and isArray(value2) and (len(value1) != len(value2))):
    raise ArrayProcessingException("No match")
MyArray.compareCheck = compareCheckListsForCoordinate
def myArrayGetSuperMethod(element):
  if isinstance(element, numpy.ndarray):
    result = numpy.array
  else:
    result = MyArray.getSuperValue(element).__init__
  return result  
MyArray.getSuperMethod = myArrayGetSuperMethod
def getEnumerated(value):
  if(isinstance(value, set)):
    _index = 0
    result = []
    #profilePrint('For each')
    print('For each start')
    for _value in value:
      #profilePrint('For each, _value: {}', _value)
      print('Got _value = {}, _index = {}'.format(_value, _index))
      element = [_index, _value]
      result.append([_index, _value])
      _index += 1
  elif(isinstance(value, MyArray)):
    result = value
  else:
    result = enumerate(value)
  return result
def arrayGetKeys(value):
  values = getEnumerated(value)
  result = []
  for _index, _value in values:
    result.append(_index)
  return result
def arrayGetValues(value):
  values = getEnumerated(value)
  result = []
  for _index, _value in values:
    result.append(_value)
  return result
