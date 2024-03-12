# Tristan Biesemeier
# 3/11/2024
# DEV108
# Final Project: Hangman

from os import system
import random
import string

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


SCREEN_CLEARING = True

TOTAL_GUESSES = 8
TOTAL_HINTS = 2
HINT_THRESHOLD = 2

game_history = [{"word": "Apple", "guesses": "abc?de"}]
category = ""


def printSeperator():
    if SCREEN_CLEARING:
        system("cls")
    else:
        print("\n" + "=" * 25 + "\n")


def singPlur(base, value, pluralSuffix="s", singularSuffix=""):
    return base + (pluralSuffix if value != 1 else singularSuffix)


def create_menu(choices):
    shortcuts = {}
    for i, choice in enumerate(choices):
        line = str(i + 1) + ". "

        foundShortcut = False
        for letter in choice:
            if not foundShortcut and letter.lower() not in shortcuts:
                shortcuts[letter.lower()] = i
                foundShortcut = True
                line += ASCII.UNDERLINE + letter + ASCII.RESET
            else:
                line += letter

        print(line)

    while True:
        inpt = input("\n> ").lower()
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
            if choice.lower() == inpt:
                return i

        print(
            ASCII.RED
            + "Invalid input. To select a choice please enter the\nfull name, corresponding number, or underlined shortcut"
            + ASCII.RESET
        )


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


def options_menu(): ...


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


def playGame():
    cat = category
    if cat == "":
        cat = random.choice(list(WORDS))

    word = random.choice(WORDS[cat]).lower()

    guess_history = ""
    guesses = TOTAL_GUESSES
    hints = TOTAL_HINTS
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

        print(f"The category is {cat}\n")
        print(board + "\n")

        if hints < TOTAL_HINTS and guess_history[-2] == "?":
            print(
                ASCII.YELLOW
                + f"A hint was used and revealed the letter '{guess_history[-1]}'"
                + ASCII.RESET
            )

        if not won and guesses > 0:
            print(f"You have {guesses} {singPlur('guess', guesses, 'es')} left")

            if guesses <= HINT_THRESHOLD:
                print(f"You have {hints} {singPlur('hint', hints)} (?) left")

            if error != None:
                print(ASCII.RED + error + ASCII.RESET)
                error = None

            inpt = input("\n> ").lower()
            if len(inpt) != 1:
                error = f"Please enter a single letter{' or a question mark' if guesses <= HINT_THRESHOLD else ''}"
                continue
            elif inpt == "?":
                if guesses <= HINT_THRESHOLD:
                    possibleHints = []
                    for letter in word:
                        if letter not in possibleHints and letter not in guess_history:
                            possibleHints.append(letter)

                    guess_history += "?" + random.choice(possibleHints)
                    hints -= 1
                else:
                    error = f"Hints are not available until there are only {HINT_THRESHOLD} {singPlur('guess', guesses, 'es')} left"
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
            f"You {ASCII.GREEN}won{ASCII.RESET} with {TOTAL_GUESSES - guesses} {singPlur('guess', TOTAL_GUESSES - guesses, 'es')} and {TOTAL_HINTS - hints} {singPlur('hint', TOTAL_HINTS - hints)}"
        )
    else:
        print(f"You {ASCII.RED}lost{ASCII.RESET}")
    print(f"The word was {ASCII.UNDERLINE}{word}{ASCII.RESET}\n")


def main():
    if SCREEN_CLEARING:
        system("cls")
    main_menu()
    print("\nThank you for playing")


if __name__ == "__main__":
    main()
