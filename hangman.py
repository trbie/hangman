# Tristan Biesemeier
# 3/11/2024
# DEV108
# Final Project: Hangman

import os
import random
import string
import urllib.request

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
PLAYED_WORDS = {}

EXTERNAL_WORDS = {
    "MIT": {
        "source": "https://www.mit.edu/~ecprice/wordlist.10000",
        "note": "10,000 words",
    },
    "UMich": {
        "source": "https://websites.umich.edu/~jlawler/wordlist",
        "note": "70,000 words",
    },
    "dwyl": {
        "source": "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt",
        "note": "370,000 words",
    },
}


class ASCII:
    RESET = "\033[0m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[36m"


### Game Data
options = {
    "Guesses": 8,
    "Hints": 2,
    "Hint Threshold": 2,
    "Show Category": True,
    "Show Wins": True,
    "Screen Clearing": False,
}

## Game History
# 0 - word
# 1 - guesses
# 2 - total guesses
# 3 - total hints
game_history = []
wins = 0
category = ""
externalCategory = False


### Utility Methods
def clearScreen():
    # Windows
    if os.name == "nt":
        os.system("cls")

    # Linux/Mac
    else:
        os.system("clear")


def printSeperator():
    if options["Screen Clearing"]:
        clearScreen()
    else:
        print("\n" + "=" * 25 + "\n")


def getWord():
    global WORDS
    global PLAYED_WORDS

    if externalCategory:
        word = ""
        while len(word) < 3:
            word = random.choice(EXTERNAL_WORDS[category]["words"])

        return [word, category]

    if category == "":
        noWordsLeft = True
        for cat in WORDS:
            if len(WORDS[cat]) > 0:
                noWordsLeft = False

        if noWordsLeft:
            for cat, words in PLAYED_WORDS.items():
                WORDS[cat] = words
            PLAYED_WORDS = {}

    elif category != "" and len(WORDS[category]) < 1:
        WORDS[category] = PLAYED_WORDS[category]
        del PLAYED_WORDS[category]

    cat = category
    if cat == "":
        choices = []
        for key, words in WORDS.items():
            if len(words) > 0:
                choices.append(key)
        cat = random.choice(choices)

    i = random.randint(0, len(WORDS[cat]) - 1)
    word = WORDS[cat].pop(i)

    if cat not in PLAYED_WORDS:
        PLAYED_WORDS[cat] = [word]
    else:
        PLAYED_WORDS[cat].append(word)

    return [word, cat]


def loadSource():
    global EXTERNAL_WORDS

    try:
        EXTERNAL_WORDS[category]["words"] = []

        for line in urllib.request.urlopen(EXTERNAL_WORDS[category]["source"]):
            word = line.decode("utf-8").strip()
            if word != "":
                EXTERNAL_WORDS[category]["words"].append(word)
    except:
        del EXTERNAL_WORDS[category]["words"]
        return False
    else:
        return True


def singPlur(base, value, pluralSuffix="s", singularSuffix=""):
    return base + (pluralSuffix if value != 1 else singularSuffix)


def game_summary(game, withUnderline=True):
    word = game[0]
    guesses = game[1]
    underline = ASCII.UNDERLINE if withUnderline else ""

    line = underline
    for letter in word:
        if letter.lower() not in LETTERS:
            line += ASCII.RESET + underline
        elif letter.lower() not in guesses:
            line += ASCII.RED
        else:
            index = guesses.find(letter)
            if index > 0 and guesses[index - 1] == "?":
                line += ASCII.YELLOW
            else:
                line += ASCII.GREEN

        line += letter
    line += ASCII.RESET

    return line


def print_game_details(game):
    word = game[0]
    guesses = game[1]
    total_guesses = game[2]
    total_hints = game[3]

    print(game_summary(game))

    numberLine = ""
    guessLine = ""
    guesses_used = 0
    hints_used = 0
    for i, letter in enumerate(guesses):
        if letter == "?":
            hints_used += 1
            continue

        if i > 0 and guesses[i - 1] == "?":
            guessLine += ASCII.YELLOW
        elif letter in word.lower():
            guessLine += ASCII.GREEN
        else:
            guessLine += ASCII.RED
            guesses_used += 1

        num = str(i - hints_used + 1) + " "
        numberLine += num
        guessLine += letter.ljust(len(num))
    guessLine += ASCII.RESET

    print("\n" + numberLine)
    print(guessLine)

    print(f"\nGuesses Used: {ASCII.RED}{guesses_used}{ASCII.RESET}/{total_guesses}")
    print(f"Hints Used: {ASCII.YELLOW}{hints_used}{ASCII.RESET}/{total_hints}")


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
            ASCII.BLUE
            + """┓┏ ___________ 
┣┫┏┓┏┓┏┓┏┳┓┏┓┏┓
┛┗┗┻┛┗┗┫┛┗┗┗┻┛┗
       ┛"""
            + ASCII.RESET
        )

        choice = create_menu(["Play", "Game History", "Options", "Exit"])

        if choice == 0:
            play()
        elif choice == 1:
            history_menu()
        elif choice == 2:
            options_menu()
        else:
            break

        printSeperator()


def options_menu():
    global options

    def valueToString(value):
        result = " [" + ASCII.BLUE
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
                    "\nEnter a new value for " + ASCII.BLUE + optionName + ASCII.RESET
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
    global externalCategory

    categories = sorted(list(WORDS))

    choices = categories.copy()
    choices.insert(0, "All")
    choices.append("Uncategorized")
    choices.append("Back")

    while True:
        printSeperator()
        print("Select a category\n")
        choice = create_menu(choices)

        if choice == 0:
            externalCategory = False
            category = ""
        elif choice == len(categories) + 1:
            selected = external_categories_menu()
            if not selected:
                continue
        elif choice == len(categories) + 2:
            return False
        else:
            externalCategory = False
            category = categories[choice - 1]

        return True


def external_categories_menu():
    global category
    global externalCategory

    choices = []
    for name, data in EXTERNAL_WORDS.items():
        note = ASCII.DIM + f" ({data['note']})" + ASCII.RESET
        choices.append([name, note])
    choices.append("Back")

    error = None
    while True:
        printSeperator()

        if error != None:
            print(ASCII.RED + error + ASCII.RESET + "\n")
            error = None

        print("Select a word list\n")

        choice = create_menu(choices)

        if choice == len(EXTERNAL_WORDS):
            return False
        else:
            externalCategory = True
            category = list(EXTERNAL_WORDS)[choice]

            if "words" not in EXTERNAL_WORDS[category]:
                print(ASCII.YELLOW + f"\nLoading {category} word list..." + ASCII.RESET)
                success = loadSource()

                if not success:
                    error = f"Failed to load word list from '{EXTERNAL_WORDS[category]['source']}'\nPlease select another list or try again later"
                    continue

            return True


def history_menu():
    global game_history

    while True:
        printSeperator()

        print("Game History\n")

        if len(game_history) < 1:
            print(ASCII.YELLOW + "You have no games to view" + ASCII.RESET)
            input(f"\nPress {ASCII.BLUE}Enter{ASCII.RESET} to go back ")
            break

        padding = len(str(len(game_history)))
        for i, game in enumerate(game_history):
            line = str(i + 1).rjust(padding) + " "
            line += game_summary(game, False)
            print(line)

        print()
        choice = create_menu(["Show Details", "Show All Details", "Clear All", "Back"])

        if choice == 0:
            print("\nEnter a game number to show its details")
            while True:
                inpt = input("> ")

                if inpt.isnumeric():
                    try:
                        gameId = int(inpt) - 1
                        if 0 <= gameId and gameId < len(game_history):
                            break
                    except:
                        pass

                print(
                    ASCII.RED
                    + f"\nPlease enter a whole number from 1 to {len(game_history)}"
                    + ASCII.RESET
                )

            history_details_menu(gameId)
        elif choice == 1:
            printSeperator()
            print("Detailed Game History\n")
            for i, game in enumerate(game_history):
                print(f"----- Game {i + 1} -----")
                print_game_details(game)
                if i == len(game_history) - 1:
                    print(f"-------------------\n")
                else:
                    print()

            input(f"Press {ASCII.BLUE}Enter{ASCII.RESET} to go back ")
        elif choice == 2:
            print(
                f"\nAre you sure you want to {ASCII.RED}permanently delete{ASCII.RESET} all game history?"
            )
            choice = create_menu(["Yes", "No"])
            if choice == 0:
                game_history = []
        else:
            break


def history_details_menu(index):
    while True:
        printSeperator()
        print(f"Game {index + 1}\n")
        print_game_details(game_history[index])
        print()

        choices = []
        if index < len(game_history) - 1:
            choices.append("Next")
        if index > 0:
            choices.append("Previous")
        choices.append("Back")

        choice = create_menu(choices)
        if choice < 0 or choice >= len(choices) - 1:
            break
        elif choices[choice] == "Next":
            index += 1
        else:
            index -= 1


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
    global game_history
    global wins

    [word, cat] = getWord()

    guess_history = ""
    guesses = options["Guesses"]
    hints = options["Hints"]
    error = None

    while True:
        printSeperator()
        board = ""

        won = True
        for letter in word:
            if letter.lower() in guess_history or letter.lower() not in LETTERS:
                if len(guess_history) > 0 and letter.lower() == guess_history[-1]:
                    board += ASCII.BLUE + letter + ASCII.RESET
                else:
                    board += letter
            else:
                board += "_"
                won = False

        board += "\n\n"
        for i, letter in enumerate(LETTERS):
            wasGuessed = letter in guess_history
            isInWord = letter in word.lower()
            isHint = (
                len(guess_history) > 1
                and guess_history[guess_history.find(letter) - 1] == "?"
            )

            if len(guess_history) > 0 and letter == guess_history[-1]:
                board += ASCII.BLUE
            elif wasGuessed and isInWord:
                if isHint:
                    board += ASCII.YELLOW
                else:
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

            inpt = input("\n> ").lower().strip()
            if len(inpt) != 1:
                error = f"Please enter a single letter{' or a question mark' if guesses <= options['Hint Threshold'] and hints > 0 else ''}"
                continue
            elif inpt == "?":
                if hints < 1:
                    error = "You have no more hints left"
                    continue
                elif guesses <= options["Hint Threshold"]:
                    possibleHints = []
                    for letter in word.lower():
                        if (
                            letter not in possibleHints
                            and letter in LETTERS
                            and letter not in guess_history
                        ):
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

                if inpt not in word.lower():
                    guesses -= 1
        else:
            break

    if won:
        print(
            f"You {ASCII.GREEN}won{ASCII.RESET} with {options['Guesses'] - guesses} {singPlur('guess', options['Guesses'] - guesses, 'es')} and {options['Hints'] - hints} {singPlur('hint', options['Hints'] - hints)}"
        )
        wins += 1
    else:
        print(f"You {ASCII.RED}lost{ASCII.RESET}")
    print(f"The word was {ASCII.UNDERLINE}{word}{ASCII.RESET}\n")

    game_history.append([word, guess_history, options["Guesses"], options["Hints"]])

    if options["Show Wins"]:
        print(f"You have won {wins}/{len(game_history)} games\n")


def main():
    clearScreen()

    main_menu()
    print("\nThank you for playing")


if __name__ == "__main__":
    main()
