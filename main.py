import auth
import parse


def isValid(action):
    """Check if the action inputted is valid"""
    try:
        return int(action)
    except ValueError:
        return -1


def printMenu():
    """Print out the menu of options and get a user choice"""
    QUIT = "Q"
    PULL_DATA = 1
    PARSE_DATA = 2
    MAX = 2
    MIN = 1
    print("Options are:")
    print("[%d]: Authenticate and Pull Data" % PULL_DATA)
    print("[%d]: Parse and Print out Data" % PARSE_DATA)
    print()
    print("[%s]: Quit" % QUIT)
    selection = input()
    if(selection.upper() == QUIT):
        print("Closing!")
        return -1
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
    while(action != -1):
        if(action == 1):
            auth.main()
        elif(action == 2):
            parse.main()
        action = printMenu()
    print("Exited!")


if __name__ == "__main__":
    main()
