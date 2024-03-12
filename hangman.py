# Tristan Biesemeier
# 3/11/2024
# DEV108
# Final Project: Hangman

from os import system
import random
import string

LETTERS = string.ascii_lowercase
WORDS = {
    "FRUITS": ["Apple", "Banana", "Orange"],
    "ANIMALS": ["Armadillo", "Beaver", "Cat", "Dog"],
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

        name = choice["name"]
        foundShortcut = False
        for letter in name:
            if not foundShortcut and letter.lower() not in shortcuts:
                shortcuts[letter.lower()] = choice
                foundShortcut = True
                line += ASCII.UNDERLINE + letter + ASCII.RESET
            else:
                line += letter

        print(line)

    success = False
    while not success:
        inpt = input("\n> ").lower()
        if inpt.isnumeric():
            try:
                choiceIndex = int(inpt) - 1
                if len(choices) <= choiceIndex or choiceIndex < 0:
                    raise Exception("Not valid choice")
                success = True
            except:
                pass

            if success:
                if choices[choiceIndex]["action"] != None:
                    choices[choiceIndex]["action"]()
                break

        for shortcut, choice in shortcuts.items():
            if shortcut == inpt:
                if choice["action"] != None:
                    choice["action"]()
                success = True
                break

        for choice in choices:
            if choice["name"].lower() == inpt:
                if choice["action"] != None:
                    choice["action"]()
                success = True
                break

        if not success:
            print(
                ASCII.RED
                + "Invalid input. To select a choice please enter the\nfull name, corresponding number, or underlined shortcut"
                + ASCII.RESET
            )


def main_menu():
    # https://patorjk.com/software/taag/#p=display&f=Tmplr&t=Hangman
    print(
        """┓┏ ___________ 
┣┫┏┓┏┓┏┓┏┳┓┏┓┏┓
┛┗┗┻┛┗┗┫┛┗┗┗┻┛┗
       ┛"""
    )

    create_menu(
        [
            {"name": "Play", "action": playGame},
            {"name": "Options", "action": options_menu},
            {"name": "Exit", "action": None},
        ]
    )


def options_menu(): ...


def playagain_menu():
    def back():
        printSeperator()
        main_menu()

    create_menu(
        [
            {"name": "Play Again", "action": playGame},
            {"name": "Categories", "action": None},
            {"name": "Back", "action": back},
        ]
    )


def playGame():
    word = random.choice(WORDS["ANIMALS"]).lower()
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
            if len(inpt) > 1:
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

    playagain_menu()


def main():
    # minor amounts of stack overflowing is possible
    if SCREEN_CLEARING:
        system("cls")
    main_menu()
    print("\nThank you for playing")


if __name__ == "__main__":
    main()
