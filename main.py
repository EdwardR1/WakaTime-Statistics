from auth import auth, updateCurrentMonth
from parse import main as parse

PULL_DATA = 1
UPDATE_CURRENT_MONTH = 2
PARSE_DATA = 3
EXIT_VAL = -1

def isValid(action):
    """Check if the action inputted is valid"""
    try:
        return int(action)
    except ValueError:
        return -1


def printMenu():
    """Print out the menu of options and get a user choice"""
    QUIT = "Q"
    MIN = 1
    MAX = 3
    print("Options are:")
    print("[%d]: Authenticate and Pull Data" % PULL_DATA)
    print("[%d]: Update only current month data" % UPDATE_CURRENT_MONTH)
    print("[%d]: Parse and Print out Data" % PARSE_DATA)
    print()
    print("[%s]: Quit" % QUIT)
    selection = input()
    if(selection.upper() == QUIT):
        print("Closing!")
        return EXIT_VAL
    elif(isValid(selection) < MIN or isValid(selection) > MAX):
        print("Invalid choice! Try again!")
        printMenu()
    return isValid(selection)


def main():
    """
    Print out menu\n
    Run auth.main() if choice == 1\n
    Run parse.main() if choice == 2
    """
    action = printMenu()
    while(action != EXIT_VAL):
        if(action == PULL_DATA):
            auth()
        elif(action == UPDATE_CURRENT_MONTH):
            updateCurrentMonth()
        elif(action == PARSE_DATA):
            parse()
        action = printMenu()
    print("Exited!")


if __name__ == "__main__":
    main()
