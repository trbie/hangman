# Tristan Biesemeier
# 3/16/2024
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
total_guesses_used = 0
total_hints_used = 0
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

    # If using special category
    if externalCategory:
        word = ""
        # Get a random word that is at least 3 characters long
        while len(word) < 3:
            word = random.choice(EXTERNAL_WORDS[category]["words"])

        return [word, category]

    # If using all categories
    if category == "":
        # Check if there are unused words left
        noWordsLeft = True
        for cat in WORDS:
            if len(WORDS[cat]) > 0:
                noWordsLeft = False

        # If there are no words left, reset the used words
        if noWordsLeft:
            for cat, words in PLAYED_WORDS.items():
                WORDS[cat] = words
            PLAYED_WORDS = {}

    # If the selected category has no words left, reset the used words
    elif category != "" and len(WORDS[category]) < 1:
        WORDS[category] = PLAYED_WORDS[category]
        del PLAYED_WORDS[category]

    cat = category
    # If all categories are selected
    if cat == "":
        # Select a random category with unused words
        choices = []
        for key, words in WORDS.items():
            if len(words) > 0:
                choices.append(key)
        cat = random.choice(choices)

    # Select a random word in the selected category
    i = random.randint(0, len(WORDS[cat]) - 1)
    word = WORDS[cat].pop(i)

    # Move selected word to the used word list
    if cat not in PLAYED_WORDS:
        PLAYED_WORDS[cat] = [word]
    else:
        PLAYED_WORDS[cat].append(word)

    return [word, cat]


def loadSource():
    global EXTERNAL_WORDS

    # Try to load words from url, return if it was successful
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
    # For every letter in the word
    for letter in word:
        # If the letter is not guessable, color is unset
        if letter.lower() not in LETTERS:
            line += ASCII.RESET + underline
        # If the letter was not guessed, color is red
        elif letter.lower() not in guesses:
            line += ASCII.RED
        # Else, the letter was guessed
        else:
            index = guesses.find(letter)
            # If the guess was a hint, color is yellow
            if index > 0 and guesses[index - 1] == "?":
                line += ASCII.YELLOW
            # Else the color is green
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

    ## Game Timeline
    numberLine = ""
    guessLine = ""
    guesses_used = 0
    hints_used = 0
    # For each letter in guess
    for i, letter in enumerate(guesses):
        # If it is a hint marker, skip
        if letter == "?":
            hints_used += 1
            continue

        # If it was a hint, color is yellow
        if i > 0 and guesses[i - 1] == "?":
            guessLine += ASCII.YELLOW
        # If it was a correct guess, color is green
        elif letter in word.lower():
            guessLine += ASCII.GREEN
        # Else, it was a wrong guess, color is red
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

    ## Print choices and get shortcuts
    shortcuts = {}
    width = len(str(len(choices)))
    # For every choice
    for i, choice in enumerate(choices):
        line = str(i + 1).rjust(width) + ". "

        # Don't use display text for the shortcut
        selector = choice
        if type(choice) == list:
            selector = choice[0]

        foundShortcut = False
        # For each letter in the selector
        for letter in selector:
            # If a shorcut hasn't been found and the current letter is not already a shortcut
            if not foundShortcut and letter.lower() not in shortcuts:
                # Use letter as a shortcut
                shortcuts[letter.lower()] = i
                foundShortcut = True
                line += ASCII.UNDERLINE + letter + ASCII.RESET
            else:
                line += letter

        # Add display text to the end
        if type(choice) == list:
            line += choice[1]

        print(line)

    # Keep looping until valid input
    while True:
        inpt = input("\n> ").lower().strip()
        # Select the choice with the list number
        if inpt.isnumeric():
            try:
                choiceIndex = int(inpt) - 1
                if len(choices) <= choiceIndex or choiceIndex < 0:
                    raise Exception("Not valid choice")
            except:
                pass
            else:
                return choiceIndex

        # Select the choice with a shortcut
        for shortcut, choice in shortcuts.items():
            if shortcut == inpt:
                return choice

        # Select the choice with the full selector (not display text)
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

        # Play
        if choice == 0:
            play()
        # Game History
        elif choice == 1:
            history_menu()
        # Options
        elif choice == 2:
            options_menu()
        # Exit
        else:
            break

        printSeperator()


def options_menu():
    global options

    def valueToString(value):
        # Format option value: [ ]/[X], or [#]
        result = " [" + ASCII.BLUE
        if type(value) == bool:
            result += "X" if value else " "
        else:
            result += str(value)

        return result + ASCII.RESET + "]"

    # Turn every option into a choice for the menu
    choices = []
    for name, value in options.items():
        choices.append([name, valueToString(value)])
    choices.append("Back")

    # Keep looping until user exits menu
    while True:
        printSeperator()

        print("Select an option to change\n")

        choice = create_menu(choices)

        # If the choice is an option
        if choice < len(options) and choice > -1:
            optionName = list(options)[choice]
            optionValue = options[optionName]

            # If the option is boolean, toggle its value
            if type(optionValue) == bool:
                print(optionName)
                optionValue = not optionValue

            # If the option is integer, ask for a new value
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

            # Apply the new value
            options[optionName] = optionValue
            choices[choice][1] = valueToString(optionValue)

        # Back
        else:
            break


def categories_menu():
    global category
    global externalCategory

    # Create menu choices with all categories
    categories = sorted(list(WORDS))

    choices = categories.copy()
    choices.insert(0, "All")
    choices.append("Uncategorized")
    choices.append("Back")

    while True:
        printSeperator()
        print("Select a category\n")
        choice = create_menu(choices)

        # All
        if choice == 0:
            externalCategory = False
            category = ""
        # Uncategorized
        elif choice == len(categories) + 1:
            selected = external_categories_menu()
            if not selected:
                continue
        # Back
        elif choice == len(categories) + 2:
            return False
        # Specific category
        else:
            externalCategory = False
            category = categories[choice - 1]

        return True


def external_categories_menu():
    global category
    global externalCategory

    # Create menu choices with all external categories
    choices = []
    for name, data in EXTERNAL_WORDS.items():
        note = ASCII.DIM + f" ({data['note']})" + ASCII.RESET
        choices.append([name, note])
    choices.append("Back")

    error = None
    while True:
        printSeperator()

        # If there is an error, print it
        if error != None:
            print(ASCII.RED + error + ASCII.RESET + "\n")
            error = None

        print("Select a word list\n")

        choice = create_menu(choices)

        # Back
        if choice == len(EXTERNAL_WORDS):
            return False
        # Specific category
        else:
            externalCategory = True
            category = list(EXTERNAL_WORDS)[choice]

            # If the category has not been loaded
            if "words" not in EXTERNAL_WORDS[category]:
                # Try to load words
                print(ASCII.YELLOW + f"\nLoading {category} word list..." + ASCII.RESET)
                success = loadSource()

                # If words could not be loaded, show error
                if not success:
                    error = f"Failed to load word list from '{EXTERNAL_WORDS[category]['source']}'\nPlease select another list or try again later"
                    continue

            return True


def history_menu():
    global game_history

    while True:
        printSeperator()

        print("Game History\n")

        # If no games to view, go back to main menu
        if len(game_history) < 1:
            print(ASCII.YELLOW + "You have no games to view" + ASCII.RESET)
            input(f"\nPress {ASCII.BLUE}Enter{ASCII.RESET} to go back ")
            break

        # Show all game summaries
        padding = len(str(len(game_history)))
        for i, game in enumerate(game_history):
            line = str(i + 1).rjust(padding) + " "
            line += game_summary(game, False)
            print(line)

        # Show game stats
        print(f"\nGames won: {ASCII.GREEN}{wins}{ASCII.RESET}/{len(game_history)}")
        print(f"Total guesses used: {ASCII.RED}{total_guesses_used}{ASCII.RESET}")
        print(f"Total hints used: {ASCII.YELLOW}{total_hints_used}{ASCII.RESET}")

        print()
        choice = create_menu(["Show Details", "Show All Details", "Clear All", "Back"])

        # Show Details
        if choice == 0:
            print("\nEnter a game number to show its details")
            # Get game number to show details of
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
        # Show All Details
        elif choice == 1:
            printSeperator()
            print("Detailed Game History\n")

            # Print all games in detail
            for i, game in enumerate(game_history):
                print(f"----- Game {i + 1} -----")
                print_game_details(game)
                if i == len(game_history) - 1:
                    print(f"-------------------\n")
                else:
                    print()

            input(f"Press {ASCII.BLUE}Enter{ASCII.RESET} to go back ")
        # Clear All
        elif choice == 2:
            print(
                f"\nAre you sure you want to {ASCII.RED}permanently delete{ASCII.RESET} all game history?"
            )
            # Confirm game history reset
            choice = create_menu(["Yes", "No"])
            if choice == 0:
                game_history = []
        # Back
        else:
            break


def history_details_menu(index):
    while True:
        printSeperator()
        # Print game details
        print(f"Game {index + 1}\n")
        print_game_details(game_history[index])
        print()

        # Create navigation menu
        choices = []
        # If there is a next game, add next
        if index < len(game_history) - 1:
            choices.append("Next")
        # If there is a previous game, add previous
        if index > 0:
            choices.append("Previous")
        choices.append("Back")

        choice = create_menu(choices)
        # Back
        if choice < 0 or choice >= len(choices) - 1:
            break
        # Next
        elif choices[choice] == "Next":
            index += 1
        # Previous
        else:
            index -= 1


def play():
    choice = 1
    while True:
        # Play Again
        if choice == 0:
            playGame()
        # Categories
        elif choice == 1:
            categorySelected = categories_menu()
            if not categorySelected:
                break

            playGame()
        # Back
        else:
            break

        choice = create_menu(["Play Again", "Categories", "Back"])


### Core Game
def playGame():
    global game_history
    global wins
    global total_guesses_used
    global total_hints_used

    # Get random word from selected category
    [word, cat] = getWord()

    # Game data
    guess_history = ""
    guesses = options["Guesses"]
    hints = options["Hints"]
    error = None

    # Keep looping until word is guessed or no guesses left
    while True:
        printSeperator()
        board = ""

        ## Build the unrevealed word
        won = True
        # For each letter in the target word
        for letter in word:
            # If the letter was guessed or is unguessable
            if letter.lower() in guess_history or letter.lower() not in LETTERS:
                # If the letter was just guessed, make it blue
                if len(guess_history) > 0 and letter.lower() == guess_history[-1]:
                    board += ASCII.BLUE + letter + ASCII.RESET
                # Else, show the letter with no color
                else:
                    board += letter
            # Else, show an underscore
            else:
                board += "_"
                # There is an ungessed letter, so the game is not over
                won = False

        ## Build the alphabet
        board += "\n\n"
        # For every guessable letter
        for i, letter in enumerate(LETTERS):
            wasGuessed = letter in guess_history
            isInWord = letter in word.lower()
            isHint = (
                len(guess_history) > 1
                and guess_history[guess_history.find(letter) - 1] == "?"
            )

            # If the letter was just guessed, color it blue
            if len(guess_history) > 0 and letter == guess_history[-1]:
                board += ASCII.BLUE
            # If the letter was a correct guess
            elif wasGuessed and isInWord:
                # If it was a hint, color it yellow
                if isHint:
                    board += ASCII.YELLOW
                # Else, color it green
                else:
                    board += ASCII.GREEN
            # If it was an incorrect guess, color it red
            elif wasGuessed:
                board += ASCII.RED
            # Else, it was not guessed, dim it
            else:
                board += ASCII.DIM

            board += letter + ASCII.RESET + " "

            if i % 10 == 9:
                board += "\n"

        # Print the category if it is enabled
        if options["Show Category"]:
            print(f"The category is {cat}\n")
        print(board + "\n")

        # Show what the latest hint revealed
        if hints < options["Hints"] and guess_history[-2] == "?":
            print(
                ASCII.YELLOW
                + f"A hint was used and revealed the letter '{guess_history[-1]}'"
                + ASCII.RESET
            )

        # If the game is still going, ask for a guess
        if not won and guesses > 0:
            print(f"You have {guesses} {singPlur('guess', guesses, 'es')} left")

            # If hints can be used, show how many hints are left
            if guesses <= options["Hint Threshold"] and hints > 0:
                print(f"You have {hints} {singPlur('hint', hints)} (?) left")

            # If there is an error, show it
            if error != None:
                print(ASCII.RED + error + ASCII.RESET)
                error = None

            inpt = input("\n> ").lower().strip()
            # Make sure input is a single letter
            if len(inpt) != 1:
                error = f"Please enter a single letter{' or a question mark' if guesses <= options['Hint Threshold'] and hints > 0 else ''}"
                continue
            # If they are trying to use a hint
            elif inpt == "?":
                # Show an error if no hints are left
                if hints < 1:
                    error = "You have no more hints left"
                    continue
                # If hints can be used, use a hint
                elif guesses <= options["Hint Threshold"]:
                    possibleHints = []
                    # Loop through the letters in the word and get all possible hints
                    for letter in word.lower():
                        if (
                            letter not in possibleHints
                            and letter in LETTERS
                            and letter not in guess_history
                        ):
                            possibleHints.append(letter)

                    # Choose a random letter that hasn't already been guessed and is guessable
                    guess_history += "?" + random.choice(possibleHints)
                    hints -= 1
                # Else, hints are not available, show an error
                else:
                    error = f"Hints are not available until there are only {options['Hint Threshold']} {singPlur('guess', guesses, 'es')} left"
                    continue
            # If the input has already be guessed, show an error
            elif inpt in guess_history:
                error = "That letter has already been guessed"
                continue
            # If the input is not guessable, show an error
            elif inpt not in LETTERS:
                error = "That is not a valid letter"
                continue
            # Else, it is a valid guess
            else:
                guess_history += inpt

                # If the guess is incorrect, remove a guess
                if inpt not in word.lower():
                    guesses -= 1
        # The game is over
        else:
            break

    # Print win/loss message
    if won:
        print(
            f"You {ASCII.GREEN}won{ASCII.RESET} with {options['Guesses'] - guesses} {singPlur('guess', options['Guesses'] - guesses, 'es')} and {options['Hints'] - hints} {singPlur('hint', options['Hints'] - hints)}"
        )
        wins += 1
    else:
        print(f"You {ASCII.RED}lost{ASCII.RESET}")
    print(f"The word was {ASCII.UNDERLINE}{word}{ASCII.RESET}\n")

    # Add game to history
    game_history.append([word, guess_history, options["Guesses"], options["Hints"]])
    total_guesses_used += options["Guesses"] - guesses
    total_hints_used += options["Hints"] - hints

    # Print the total wins if they are enabled
    if options["Show Wins"]:
        print(f"You have won {wins}/{len(game_history)} games\n")


def main():
    global game_history
    global options
    global wins
    global total_guesses_used
    global total_hints_used

    # Clear screen to fix ascii color errors on older terminals
    clearScreen()

    # If there is saved data, load it
    if os.path.exists("hangman.data") and os.path.isfile("hangman.data"):
        try:
            with open("hangman.data") as file:
                loadingHistory = False
                for line in file:
                    line = line.strip()

                    # Skip empty lines
                    if line == "":
                        continue
                    # Done loading options, start loading game history
                    elif line == "==":
                        loadingHistory = True
                    # Load game history
                    elif loadingHistory:
                        game = line.split(",")
                        if len(game) == 4:
                            game[2] = int(game[2])
                            game[3] = int(game[3])
                            game_history.append(game)

                            word = game[0].lower()
                            for letter in word:
                                if letter not in LETTERS:
                                    word = word.replace(letter, "")

                            # Keep track of games stats from saved data
                            for letter in game[1]:
                                if letter == "?":
                                    total_hints_used += 1
                                elif letter in word:
                                    word = word.replace(letter, "")
                                else:
                                    total_guesses_used += 1

                            if len(word) == 0:
                                wins += 1
                    # Load option
                    else:
                        [name, value] = line.split("=")
                        if type(options[name]) == bool:
                            options[name] = value == "True"
                        else:
                            options[name] = int(value)

        except:
            print(ASCII.RED + "Failed to load saved data" + ASCII.RESET)
        else:
            print(ASCII.YELLOW + "Loaded saved data" + ASCII.RESET)

    main_menu()

    try:
        with open("hangman.data", "w") as file:
            # Save options
            for name, value in options.items():
                file.write(f"{name}={value}\n")

            file.write("==\n")

            # Save game history
            for game in game_history:
                file.write(f"{game[0]},{game[1]},{game[2]},{game[3]}\n")

    except:
        ...

    print("\nThank you for playing")


if __name__ == "__main__":
    main()
