import pytesseract
import re
import cv2

#Image input
image_path = 'data/workschedule.jpg'
img = cv2.imread(image_path)

#Dictionary to store all 
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
    if not re.match(r'\d{1,2}/\d{1,2}', word) and any(char.isdigit() for char in word) or word.lower() in ["a.m.", "p.m."]:
        current_time += word
    else:
        if current_time:
            combined_times.append(current_time.strip())
            current_time = ""
    if re.match(r'\d{1,2}/\d{1,2}', word):
        combined_times.append(word)

#print(combined_times)

for time in combined_times:
    if not re.match(r'\d{1,2}/\d{1,2}', time):
        if not current_start_time:
            current_start_time = time
        else:
            current_end_time = time
    else:
        current_date = time
        shifts_dict[current_date] = {'start_time': current_start_time, 'end_time': current_end_time}

        current_start_time = None
        current_end_time = None
   
print(shifts_dict)
