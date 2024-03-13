# Tristan Biesemeier
# 3/11/2024
# DEV108
# Final Project: Hangman

from os import system
import random
import string

### Constants
LETTERS = string.ascii_lowercase
WORDS = {
    "Fruits": [
        "Apple",
        "Banana",
        "Orange",
        "Grape",
        "Strawberry",
        "Watermelon",
        "Pineapple",
        "Mango",
        "Kiwi",
        "Peach",
        "Pear",
        "Cherry",
        "Plum",
        "Blueberry",
        "Raspberry",
    ],
    "Animals": [
        "Elephant",
        "Tiger",
        "Lion",
        "Giraffe",
        "Monkey",
        "Zebra",
        "Kangaroo",
        "Hippo",
        "Rhino",
        "Panda",
        "Leopard",
        "Crocodile",
        "Gorilla",
        "Koala",
        "Squirrel",
    ],
    "Countries": [
        "United States",
        "Canada",
        "Brazil",
        "India",
        "China",
        "Russia",
        "Germany",
        "Japan",
        "Australia",
        "Mexico",
        "France",
        "United Kingdom",
        "Italy",
        "Spain",
        "South Korea",
    ],
    "Sports": [
        "Football",
        "Basketball",
        "Soccer",
        "Tennis",
        "Golf",
        "Cricket",
        "Rugby",
        "Baseball",
        "Hockey",
        "Volleyball",
        "Swimming",
        "Boxing",
        "Cycling",
        "Running",
        "Wrestling",
    ],
    "Professions": [
        "Doctor",
        "Teacher",
        "Engineer",
        "Artist",
        "Lawyer",
        "Chef",
        "Pilot",
        "Nurse",
        "Firefighter",
        "Police Officer",
        "Scientist",
        "Architect",
        "Writer",
        "Musician",
        "Athlete",
    ],
    "Transportation": [
        "Car",
        "Bus",
        "Train",
        "Bicycle",
        "Motorcycle",
        "Airplane",
        "Boat",
        "Helicopter",
        "Truck",
        "Subway",
        "Taxi",
        "Ferry",
        "Scooter",
        "Van",
        "Jet",
    ],
}


class ASCII:
    RESET = "\033[0m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"


### Game Data
options = {
    "Guesses": 8,
    "Hints": 2,
    "Hint Threshold": 2,
    "Screen Clearing": False,
    "Show Category": True,
}

game_history = [{"word": "Apple", "guesses": "abc?de"}]
category = ""


### Utility Methods
def printSeperator():
    if options["Screen Clearing"]:
        system("cls")
    else:
        print("\n" + "=" * 25 + "\n")


def singPlur(base, value, pluralSuffix="s", singularSuffix=""):
    return base + (pluralSuffix if value != 1 else singularSuffix)


def create_menu(choices):
    if len(choices) < 1:
        return -1

    shortcuts = {}
    width = len(str(len(choices)))
    for i, choice in enumerate(choices):
        line = str(i + 1).rjust(width) + ". "

        selector = choice
        if type(choice) == list:
            selector = choice[0]

        foundShortcut = False
        for letter in selector:
            if not foundShortcut and letter.lower() not in shortcuts:
                shortcuts[letter.lower()] = i
                foundShortcut = True
                line += ASCII.UNDERLINE + letter + ASCII.RESET
            else:
                line += letter

        if type(choice) == list:
            line += choice[1]

        print(line)

    while True:
        inpt = input("\n> ").lower().strip()
        if inpt.isnumeric():
            try:
                choiceIndex = int(inpt) - 1
                if len(choices) <= choiceIndex or choiceIndex < 0:
                    raise Exception("Not valid choice")
            except:
                pass
            else:
                return choiceIndex

        for shortcut, choice in shortcuts.items():
            if shortcut == inpt:
                return choice

        for i, choice in enumerate(choices):
            if type(choice) == list:
                choice = choice[0]

            if choice.lower() == inpt:
                return i

        print(
            ASCII.RED
            + "Invalid input. To select a choice please enter the\nfull name, corresponding number, or underlined shortcut"
            + ASCII.RESET
        )


### Menus
def main_menu():
    while True:
        # https://patorjk.com/software/taag/#p=display&f=Tmplr&t=Hangman
        print(
            """┓┏ ___________ 
┣┫┏┓┏┓┏┓┏┳┓┏┓┏┓
┛┗┗┻┛┗┗┫┛┗┗┗┻┛┗
       ┛"""
        )

        choice = create_menu(["Play", "Options", "Exit"])

        if choice == 0:
            play()
        elif choice == 1:
            options_menu()
        else:
            exit()

        printSeperator()


def options_menu():
    global options

    def valueToString(value):
        result = " [" + ASCII.YELLOW
        if type(value) == bool:
            result += "X" if value else " "
        else:
            result += str(value)

        return result + ASCII.RESET + "]"

    choices = []
    for name, value in options.items():
        choices.append([name, valueToString(value)])
    choices.append("Back")

    while True:
        printSeperator()

        print("Select an option to change\n")

        choice = create_menu(choices)

        if choice < len(options) and choice > -1:
            optionName = list(options)[choice]
            optionValue = options[optionName]

            if type(optionValue) == bool:
                print(optionName)
                optionValue = not optionValue

            elif type(optionValue) == int:
                print(
                    "\nEnter a new value for " + ASCII.YELLOW + optionName + ASCII.RESET
                )

                while True:
                    inpt = input("> ")

                    if inpt.isnumeric():
                        try:
                            optionValue = int(inpt)
                            break
                        except:
                            pass

                    print(
                        ASCII.RED
                        + "\nPlease enter a non-negative whole number"
                        + ASCII.RESET
                    )

            options[optionName] = optionValue
            choices[choice][1] = valueToString(optionValue)

        else:
            break


def categories_menu():
    global category

    choices = list(WORDS)
    choices.insert(0, "All")
    choices.append("Back")

    printSeperator()
    print("Select a category\n")
    choice = create_menu(choices)

    if choice == 0:
        category = ""
    elif choice == len(WORDS) + 1:
        return False
    else:
        category = list(WORDS)[choice - 1]

    return True


def play():
    choice = 1
    while True:
        if choice == 0:
            playGame()
        elif choice == 1:
            categorySelected = categories_menu()
            if not categorySelected:
                break

            playGame()
        else:
            break

        choice = create_menu(["Play Again", "Categories", "Back"])


### Core Game
def playGame():
    cat = category
    if cat == "":
        cat = random.choice(list(WORDS))

    word = random.choice(WORDS[cat]).lower()

    guess_history = ""
    guesses = options["Guesses"]
    hints = options["Hints"]
    error = None

    while True:
        printSeperator()
        board = ""

        won = True
        for letter in word:
            if letter in guess_history:
                if letter == guess_history[-1]:
                    board += ASCII.YELLOW + letter + ASCII.RESET
                else:
                    board += letter
            else:
                board += "_"
                won = False

        board += "\n\n"
        for i, letter in enumerate(LETTERS):
            wasGuessed = letter in guess_history
            isInWord = letter in word

            if len(guess_history) > 0 and letter == guess_history[-1]:
                board += ASCII.YELLOW
            elif wasGuessed and isInWord:
                board += ASCII.GREEN
            elif wasGuessed:
                board += ASCII.RED
            else:
                board += ASCII.DIM

            board += letter + ASCII.RESET + " "

            if i % 10 == 9:
                board += "\n"

        if options["Show Category"]:
            print(f"The category is {cat}\n")
        print(board + "\n")

        if hints < options["Hints"] and guess_history[-2] == "?":
            print(
                ASCII.YELLOW
                + f"A hint was used and revealed the letter '{guess_history[-1]}'"
                + ASCII.RESET
            )

        if not won and guesses > 0:
            print(f"You have {guesses} {singPlur('guess', guesses, 'es')} left")

            if guesses <= options["Hint Threshold"] and hints > 0:
                print(f"You have {hints} {singPlur('hint', hints)} (?) left")

            if error != None:
                print(ASCII.RED + error + ASCII.RESET)
                error = None

            inpt = input("\n> ").lower()
            if len(inpt) != 1:
                error = f"Please enter a single letter{' or a question mark' if guesses <= options['Hint Threshold'] and hints > 0 else ''}"
                continue
            elif inpt == "?":
                if hints < 1:
                    error = "You have no more hints left"
                    continue
                elif guesses <= options["Hint Threshold"]:
                    possibleHints = []
                    for letter in word:
                        if letter not in possibleHints and letter not in guess_history:
                            possibleHints.append(letter)

                    guess_history += "?" + random.choice(possibleHints)
                    hints -= 1
                else:
                    error = f"Hints are not available until there are only {options['Hint Threshold']} {singPlur('guess', guesses, 'es')} left"
                    continue
            elif inpt in guess_history:
                error = "That letter has already been guessed"
                continue
            elif inpt not in LETTERS:
                error = "That is not a valid letter"
                continue
            else:
                guess_history += inpt

                if inpt not in word:
                    guesses -= 1
        else:
            break

    if won:
        print(
            f"You {ASCII.GREEN}won{ASCII.RESET} with {options['Guesses'] - guesses} {singPlur('guess', options['Guesses'] - guesses, 'es')} and {options['Hints'] - hints} {singPlur('hint', options['Hints'] - hints)}"
        )
    else:
        print(f"You {ASCII.RED}lost{ASCII.RESET}")
    print(f"The word was {ASCII.UNDERLINE}{word}{ASCII.RESET}\n")


def main():
    if options["Screen Clearing"]:
        system("cls")
    main_menu()
    print("\nThank you for playing")


if __name__ == "__main__":
    main()
