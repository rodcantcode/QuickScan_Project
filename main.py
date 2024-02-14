#Take in Image input
import pytesseract
import re
import cv2
import numpy as np
from pytesseract import Output

img = cv2.imread('data/workschedule1.jpeg')
d = pytesseract.image_to_data(img, output_type=Output.DICT)
keys = list(d.keys())
print(d.keys())

#date_pattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'


n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 10:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


#img_file = "data/workschedule2.png"
#img_file = "data/workschedule3.png"
cv2.imshow('img', img)
cv2.waitKey(0)
#ocr_results = pytesseract.image_to_string(img)
#print(ocr_results)