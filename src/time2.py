from datetime import datetime 
import time

def printTime():
    timestamp = time.time()
    dateTime = datetime.fromtimestamp(timestamp)
    strDateTime = dateTime.strftime("%Y-%m-%d_%H-%M-%S")
    print(strDateTime)
    