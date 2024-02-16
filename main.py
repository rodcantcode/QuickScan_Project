import pytesseract
import re
import cv2
import numpy as np
from pytesseract import Output

#Image input
image_path = 'data/workschedule.jpg'
img = cv2.imread(image_path)
d = pytesseract.image_to_data(img, output_type=Output.DICT)

#List for all text results 
textResults = []

shifts_dict = {}

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Use pytesseract to perform OCR on the grayscale image
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(gray, config=custom_config)

# Split the OCR output into words
words = text.split()

# Initialize variables to track the current date, start time, and end time
current_date = None
current_start_time = None
current_end_time = None

# Combine relevant components
combined_times = []
current_time = ""
for word in words:
    print(word)
    if any(char.isdigit() for char in word) or word.lower() in ["a.m.", "p.m."] and not re.match(r'\d{1,2}/\d{1,2}', word):
        current_time += " " + word
    else:
        if current_time:
            combined_times.append(current_time.strip())
            current_time = ""
print(combined_times)


for time in combined_times:
    if (any(char.isdigit() for char in time) or time.lower() in ["a.m.", "p.m."]) and not re.match(r'\d{1,2}/\d{1,2}', time):
        #print(time)
        if not current_start_time:
            current_start_time = time
   
        

'''
#Draws Boxes on Image where text is detected
n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 0:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        textResults.append(d['text'][i])
print(textResults)
#cv2.imshow('img', img)
#cv2.waitKey(0)

if current_start_time == None:
        current_start_time = word
        print(current_start_time)
        current_start_time = None
'''