def convertToTimeValue(seconds):
    """Convert seconds to time string"""
    minutes = (seconds / 60) % 60
    hours = (seconds / 60 / 60) % 24
    days = (seconds / 60 / 60 / 24)
    return "Days: " + str(days) + " Hours: " + str(hours) + " Minutes: " + str(minutes)


def secondsToMinutes(seconds):
    """Convert seconds to minutes"""
    return seconds / 60


def minutesToHours(minutes):
    """Convert minutes to hours"""
    return minutes / 60
