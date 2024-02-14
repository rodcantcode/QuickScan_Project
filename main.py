import pytesseract
import re
import cv2
import numpy as np
from pytesseract import Output

#Image input
img = cv2.imread('data/workschedule2.png')
d = pytesseract.image_to_data(img, output_type=Output.DICT)

#List for all text results 
textResults = []

#Draws Boxes on Image where text is detected
n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 0:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        textResults.append(d['text'][i])

print(textResults)
cv2.imshow('img', img)
cv2.waitKey(0)