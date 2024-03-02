import re

def convert_time(time):
    if time == None:
        pass
    else:
        if re.search('a.m.', time): #Checks if the meridiem a.m. is within the string
            convertedTime = re.sub('a.m.', '', time) #removes the meridiem so now left with just time value

            #Checking if time is in format HH:MM, if so, return the time value
            if re.search('(1[0-2]):[0-5][0-9]', convertedTime):
                return convertedTime 
           
            #Checking if time is in format H:MM, if so, add 0 before the H
            if re.search('[1-9]:[0-5][0-9]', convertedTime):
                return '0' + convertedTime
            
            #Checking if time is in format HH, if so, add trailing :00
            if re.search('(1[0-2])', convertedTime):
                return convertedTime + ':00' 
            
            #Checking if time is in format H, if so, add trailing :00
            if re.search('[1-9]', convertedTime):
                return '0' + convertedTime + ':00' 
        #The code below is now formatting like above, but for p.m. times instead
        if re.search('p.m.', time): #Checks if the meridiem p.m. is within the string
                convertedTime = re.sub('p.m.', '', time) #removes the meridiem so now left with just time value
                
                if re.search('[1-9]:[0-5][0-9]', convertedTime): #If format in H:MM
                    x = convertedTime.split(':') #Split string at colon : so that way 12 can be added to the hours alone
                    hoursMins = str(int(x[0]) + 12)
                    convertedTime = hoursMins + ":" + x[1]
                    return convertedTime
                
                if re.search('[1-9]', convertedTime): #If format in H alone, 3pm is 3 for example. 
                    hoursMins = str(int(convertedTime) + 12)
                    convertedTime = hoursMins + ":00"
                    return convertedTime
                if re.search('(1[0-2]):[0-5][0-9]', convertedTime): #If format in HH:MM
                    if '12' in convertedTime: #If HH:MM hour value is 12, then return converted time
                        return convertedTime
                    x = convertedTime.split(':')
                    hoursMins = str(int(x[0]) + 12)
                    convertedTime = hoursMins + ":" + x[1]
                    return convertedTime
                if re.search('(1[0-2])', convertedTime): #If format is in HH alone
                    if '12' in convertedTime: # If HH value is 12
                        return convertedTime + ':00'
                    hoursMins = str(int(convertedTime) + 12)
                    convertedTime = hoursMins + ':00'
                    return convertedTime 
                

def convert_date(date):
    x = date.split('/')
    m = x[0]
    d = x[1]
    y = x[2]
    
    if not re.search('(0[1-9]|1[012])', m):
        m = '0' + m
    if not re.search('(0[1-9]|[12][0-9]|3[01])', d):
        d = '0' + d 
    convertedDate = y + '-' + m + '-' + d
    return convertedDate