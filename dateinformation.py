import datetime
import os

dirName = os.path.dirname(__file__)


def isLeapYear(year):
    """Checks if the given year is a leap year"""
    if(year % 4 == 0):
        if(year % 100 == 0):
            if(year % 400 == 0):
                return True
            else:
                return False
        return True
    return False


def calcDays(month, year):
    """Calculation of ending dates"""
    if(month < 7):
        if(month % 2 != 0):
            return 31
        elif(month == 2 and isLeapYear(year)):
            return 29
        elif(month == 2):
            return 28
        else:
            return 30
    else:
        if(month % 2 != 0):
            return 30
        else:
            return 31


def monthFormat(month):
    """Formats month into proper string"""
    if(month / 10 < 1):
        return "0%d" % month
    return "%d" % month


def monthDates(month, year):
    """Returns starting date and ending date as tuple"""
    return {"start": "%d-%s-01" % (year, monthFormat(month)), "end": "%d-%s-%d" % (year, monthFormat(month), calcDays(month, year))}


def getDateDetails():
    """
    Get the current year and current month\n
    Current year serves as the main year to work out of\n
    Current month serves as the limiting month factor\n
    """
    today = datetime.date.today()
    today = str(today).split('-')
    return {"year": today[0], "month": today[1]}


def numToMonth(month):
    """Convert a numeric month to a string of the name of the month"""
    return {
        1: "jan",
        2: "feb",
        3: "mar",
        4: "apr",
        5: "may",
        6: "jun",
        7: "jul",
        8: "aug",
        9: "sep",
        10: "oct",
        11: "nov",
        12: "dec"
    }[month]


def getMonths():
    """
    Read possible months from the data folder\n
    Returns a list of possible months
    """
    files = []
    path = os.path.join(dirName, "data")
    subfolders = os.listdir(path)
    for sub in subfolders:
        fi = sub.split(".")
        if(".json" in sub):
            files.append(fi[0])
    return files


def sortMonths(monthsList):
    """Sorts month names and returns a list of sorted months"""
    numOfMonths = len(monthsList)
    sortedMonths = []
    for i in range(1, numOfMonths + 1):
        monthName = numToMonth(i)
        sortedMonths.append(monthName)
    return sortedMonths
