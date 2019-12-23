import json
import datetime
import os
from dateinformation import numToMonth, getMonths, sortMonths
from timeconversion import convertToTimeValue, secondsToMinutes, minutesToHours

dirName = os.path.dirname(__file__)


def read(file):
    """Reads file and returns data object"""
    data = {}
    try:
        with open(file) as f:
            data = json.load(f)
    except FileNotFoundError:
        return -1
    finally:
        return data


def getTotalTime(dict):
    """Returns total time from dictionary"""
    time = 0
    for i in range(len(dict["data"])):
        time += dict["data"][i]["grand_total"]["total_seconds"]
    return time


def calcLanguageTotals(combined):
    """Calculate total time per each programming language"""
    lang = {}
    for data in combined["data"]:
        languages = data["languages"]
        for languageDetails in languages:
            if(lang.get(languageDetails["name"], -1) == -1):
                lang[languageDetails["name"]] = languageDetails["total_seconds"]
            else:
                lang[languageDetails["name"]] += languageDetails["total_seconds"]
    return lang


def createLanguagesDict():
    """Return the dictionary of language time totals"""
    return calcLanguageTotals(combineFiles())


def sort(dict):
    """Sort a dictionary based on values"""
    newDict = {}
    values = list(dict.values())
    keys = list(dict.keys())
    for i in range(len(values)):
        for j in range(i, len(values)):
            if(values[i] < values[j]):
                temp = values[i]
                values[i] = values[j]
                values[j] = temp
    for value in values:
        for key in keys:
            if(dict[key] == value):
                newDict[key] = value
    return newDict


def getData():
    """Iterates through data folder.
    Stores all data into a larger dictionary with the
    month as the key and the month data as the value.\n
    Returns said dictionary of all data"""
    monthData = {}
    months = getMonths()
    path = os.path.join(dirName, "data")
    for month in months:
        monthText = month + ".json"
        file = os.path.join(path, monthText)
        data = read(file)
        monthData[month] = data
    return monthData


def combineFiles():
    """Combines the data from getData into
    a larger dictionary with all values
    from each month"""
    data = getData()
    combined = {"data": [], "start": "", "end": ""}
    count = 0
    monthsList = sortMonths(getMonths())
    firstMonth = monthsList[0]
    lastMonth = monthsList[-1]
    for month in data:
        temp = data[month]
        if(count == len(data.keys()) - 1):
            continue
        combined["data"] = combined["data"] + temp["data"]
        count += 1
    combined['start'] = data[firstMonth]['start']
    combined['end'] = data[lastMonth]['end']
    return combined


def getDateRange(startDate, endDate):
    """
    Get the range of dates available.\n
    Used to calculate the averages
    """
    start = startDate[0:startDate.index("T")]
    end = endDate[0:endDate.index("T")]

    start = start.split("-")
    end = end.split("-")
    startDateValue = datetime.date(int(start[0]), int(start[1]), int(start[2]))
    endDateValue = datetime.date(int(end[0]), int(end[1]), int(end[2]))
    calc = (endDateValue - startDateValue)
    days = calc.days
    return days


def getTopLanguages(n, languages):
    """Get the list of top n languages"""
    topLanguages = []
    count = 0
    for key in languages:
        topLanguages.append(key)
        count += 1
        if(count == n):
            break
    return topLanguages


def printTopLanguages(topLanguages, languages):
    '''Print out the top languages to the console'''
    for (i, lang) in enumerate(topLanguages):
        if(lang == "JSX"):
            print("%d. React JSX: %d hours" %
                  (i + 1, int(minutesToHours(secondsToMinutes(languages[lang])))))
        else:
            print("%d. %s: %.1f hours" % (i + 1, lang,
                                                  minutesToHours(secondsToMinutes(languages[lang]))))


def getProjects():
    """
    Get a dictionary of all the projects
    with the project name as the key
    and the total seconds as their value
    """
    combined = combineFiles()
    projects = {}
    n = 100
    for categories in combined["data"]:
        for project in categories["projects"]:
            name = project["name"]
            time = project["total_seconds"]
            if(projects.get(name, -1) == -1):
                projects[name] = time
            else:
                projects[name] += time
    return projects


def getTopProjects(n, projects):
    """Get a list of the top n projects"""
    topProjects = []
    count = 0
    for key in projects:
        topProjects.append(key)
        count += 1
        if(count == n):
            break
    return topProjects


def printTopProjects(topProjects, projects):
    """Print out the top projects to the console"""
    for (i, proj) in enumerate(topProjects):
        print("%d. %s: %.1f hours" % (i + 1, proj,
                                             minutesToHours(secondsToMinutes(projects[proj]))))


def writeToStatistics():
    """Write out statistics to a file called statistics.txt"""
    f = open("statistics.txt", "w")
    languages = sort(createLanguagesDict())
    combined = combineFiles()
    projects = sort(getProjects())
    time = getTotalTime(combined)
    hours = (minutesToHours(secondsToMinutes(time)))
    minutes = secondsToMinutes(time)
    days = getDateRange(combined["start"], combined['end'])
    average = minutes / days
    year = 2019
    n_lang = 10
    n_proj = 10

    f.write("Statistics:\n")
    f.write('\n')
    f.write("Averages:\n")
    f.write("Total number of hours spent coding in %d: %.1f hours\n" %
            (year, hours))
    f.write("Average number of minutes per day spent coding in %d: %.1f minutes\n" % (
        year, average))
    f.write("Average number of hours per day spent coding in %d: %.1f hours\n" % (
        year, hours / days))
    f.write("\n")
    f.write("Top %d Languages:\n" % (n_lang))
    topLang = getTopLanguages(n_lang, languages)
    for (i, lang) in enumerate(topLang):
        if(lang == "JSX"):
            f.write("%d. React JSX: %d hours\n" % (
                i + 1, int(minutesToHours(secondsToMinutes(languages[lang])))))
        else:
            f.write("%d. %s: %.1f hours\n" % (i + 1, lang,
                                                      minutesToHours(secondsToMinutes(languages[lang]))))
    f.write("\n")
    f.write("Top %d Projects:\n" % n_proj)
    topProj = getTopProjects(n_proj, projects)
    for (i, proj) in enumerate(topProj):
        f.write("%d. %s: %.1f hours\n" % (i + 1, proj,
                                                 minutesToHours(secondsToMinutes(projects[proj]))))
    f.close()


def printStatisticsToConsole():
    """Write out statistics to console"""
    languages = sort(createLanguagesDict())
    combined = combineFiles()
    projects = sort(getProjects())
    time = getTotalTime(combined)
    hours = (minutesToHours(secondsToMinutes(time)))
    minutes = secondsToMinutes(time)
    days = getDateRange(combined["start"], combined['end'])
    average = minutes / days
    year = 2019
    n_lang = 20
    n_proj = 20

    print("Statistics:")
    print()
    print("Averages:")
    print("Total number of hours spent coding in %d: %.1f hour" % (year, hours))
    print("Average number of minutes per day spent coding in %d: %.1f minute" %
          (year, average))
    print("Average number of hours per day spent coding in %d: %.1f hours" %
          (year, hours / days))
    print()
    print("Top %d Languages:" % (n_lang))
    topLang = getTopLanguages(n_lang, languages)
    printTopLanguages(topLang, languages)
    print()
    print("Top %d Projects:" % n_proj)
    topProj = getTopProjects(n_proj, projects)
    printTopProjects(topProj, projects)
    print()


def main():
    """Print out statistics to console
    and write out to file"""
    printStatisticsToConsole()
    writeToStatistics()


if(__name__ == "__main__"):
    main()
