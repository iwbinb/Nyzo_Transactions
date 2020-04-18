import datetime

def getTimestampSeconds():
    return int(datetime.datetime.timestamp(datetime.datetime.now()))

