#Take in Image input
import pytesseract
#import easyocr
import cv2
import numpy as np
#from PIL import Image


img = cv2.imread('data/workschedule1.jpeg')
cv2.imshow('Window1', img)
#img_file = "data/workschedule2.png"
#img_file = "data/workschedule3.png"

ocr_results = pytesseract.image_to_string(img)
print(ocr_results)