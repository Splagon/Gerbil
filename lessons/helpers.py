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

STATUSES = [
    ('in_progress', 'in_progress'),
    ('fulfilled', 'fulfilled')
]


DURATION_TO_PRICES = {
    '30' : 20,
    '45' : 30,
    '60' : 40
}



def getInstruments():
    return INSTRUMENTS

def getDurations():
    return DURATIONS

def getStatuses():
    return STATUSES

def getPrice(duration):
    return DURATION_TO_PRICES[duration]