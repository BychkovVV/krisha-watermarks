from PIL import Image
import pytesseract as pyTesseract
import numpy
import cv2
filename = "C:/Users/Administrator/Pictures/10-full.jpg"
img = numpy.array(Image.open(filename))
norm_img = numpy.zeros((img.shape[0], img.shape[1]))
img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
img = cv2.GaussianBlur(img, (1, 1), 0)
text = pyTesseract.image_to_string(img)