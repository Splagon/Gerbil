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



INTERVALS_BETWEEN_LESSONS = [
    ('1', 1),
    ('2', 2)
]



def getInstruments():
    return INSTRUMENTS

def getDurations():
    return DURATIONS

def getIntervalBetweenLessons():
    return INTERVALS_BETWEEN_LESSONS

def getDurationsToPrices(duration):
    return DURATION_TO_PRICES[duration]