INSTRUMENTS = [
    ('violin', 'violin'),
    ('double bass', 'double bass'),
    ('cello', 'cello'),
]

DURATIONS = [
    ('30', '30'),
    ('45', '45'),
    ('60', '60'),
]

DURATION_TO_PRICES = {
    '30' : 20,
    '45' : 30,
    '60' : 40
}

DAYS_IN_WEEK = [
    ('Monday' ,'Monday'),
    ('Tuesday' , 'Tuesday'),
    ('Wednesday' , 'Wednesday'),
    ('Thursday' , 'Thursday'),
    ('Friday' , 'Friday')   
]

INTERVAL_BETWEEN_LESSONS = [
    ('1', 1),
    ('2', 2)
]



def getInstruments():
    return INSTRUMENTS

def getDurations():
    return DURATIONS

def getDaysInWeek():
    return DAYS_IN_WEEK

def getIntervalsBetweenLessons():
    return INTERVAL_BETWEEN_LESSONS

def getDurationsToPrices(duration):
    return DURATION_TO_PRICES[duration]