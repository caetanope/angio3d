from datetime import datetime 
import time

def printTime(index = False):
    timestamp = time.time()
    dateTime = datetime.fromtimestamp(timestamp)
    strDateTime = dateTime.strftime("%Y/%m/%d %Hh%Mm%Ss")
    if index == False:
        print(strDateTime)
    else:
        print(str(index)+' '+strDateTime)
    