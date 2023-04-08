try:
  import os, sys
  sys.path.insert(1, 'old')
  from classes import Debug
  from main import main
  from functions import die
  from old.arrays import MyArray
  import cv2, traceback, atexit, threading
  print('Starting profiling')
  Debug.startProfiling()
  os.system('cls')
  main()
  print('Stopping profiling')
  #Debug.stopProfiling()
  #theThread = threading.Thread(target=main)
  #theThread.start()
  #theThread.join()
  #die()
except BaseException as error:
  print(error)
  print(''.join(traceback.format_tb(error.__traceback__)))
  die()