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



STATUSES = [
    ('in_progress', 'in_progress'),
    ('fulfilled', 'fulfilled')
]



def getInstruments():
    return INSTRUMENTS

def getDurations():
    return DURATIONS

def getStatuses():
    return STATUSES

def getDurationsToPrices(duration):
    return DURATION_TO_PRICES[duration]