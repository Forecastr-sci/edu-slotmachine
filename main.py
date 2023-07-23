import random

class WrongInputError(ValueError):
    pass

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

# Array is 3 rows and 3 columns. Line is considered if three elements are on the same row. Each line contributes to the win, until number of contributors reaches lines.
# TODO: When only one line is chosen, consider only match on central row instead of any row.
ROWS = 3
COLS = 3

# frequency of different elements was taken from this image
AVAILABLE_ELEMENTS = {
    "⭐": 1,    # returns bet*3
    "🪙": 3,    # returns bet*1.5
    "🍋": 4,    # returns bet
    "🫐": 5,    # returns bet*0.8
    "🍒": 7     # returns bet*0.5
}

ELEMENTS_VALUES = {
    "⭐": 10,
    "🪙": 5,
    "🍋": 3,
    "🫐": 1,
    "🍒": 0.8
}

# TODO: Make the program generate three unique reels, that will persist in each game session. 

def deposit():
    # TODO: Implement addition of money to total balance, not just initial amount
    while True:
        amount = input("What is your initial deposit? \n$")
        # validate that the amount is a number and is more than 0
        try:
            amount = int(amount)
            if amount <= 0:
                raise WrongInputError()
        except WrongInputError:
            print("Your number must be greater than 0")
        except ValueError:
            print("Please, enter a number.")
        else:
            print(f"You have deposited {amount}$ to the account")
            return amount

def getNumberOfLines():
    while True:
        lines = input(f"Enter the number of lines you want to bet on (1-{MAX_LINES})? \n")
        # validate that the lines is a number and is within the valid range (1-MAX_LINES)
        try:
            lines = int(lines)
            if not 1 <= lines <= MAX_LINES:
                raise WrongInputError()
        except WrongInputError:
            print(f"Number of lines is invalid. Try picking a number between 1 and {MAX_LINES}")
        except ValueError:
            print("Please, enter a number.")
        else:
            print(f"Your bet will go on {lines} line(s).")
            return lines

def getBet():
    while True:
        bet = input(f"How much do you want to bet per line? ({MIN_BET}-{MAX_BET})? \n")
        # validate that the bet is a number and is within the valid range (MIN_BET-MAX_BET)
        try:
            bet = int(bet)
            if not MIN_BET <= bet <= MAX_BET:
                raise WrongInputError()
        except WrongInputError:
            print(f"This bet is invalid. Try picking a number between ${MIN_BET} and ${MAX_BET}")
        except ValueError:
            print("Please, enter a number.")
        else:
            return bet

def getSlotMachineSpin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in AVAILABLE_ELEMENTS.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    # TODO: Try to make this as a list comprehension instead of nested loops if possible
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:] # would *all_symbols also work here?
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        
        columns.append(column)
        
    return columns

def displaySlotMachineSpin(columns):
    """
    Transposes columns for display that is easier to understand
    """
    # TODO: Try using zip() function instead of nested loops. Alternatively, maybe condition if column is columns[-1] can work. that way we avoid using enumerate() function.
    print("Here is the result of the spin!")
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row])

def checkWinnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol_to_check != symbol:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return int(winnings), winning_lines



def spin(balance):
    lines = getNumberOfLines()
    while True:
        bet = getBet()
        total_bet = bet * lines
        unsufficient_balance = total_bet > balance
        if unsufficient_balance:
            print(f"You don't have enough to bet that amount, your current balance is {balance}, but you are trying to bet {total_bet}. You can bet at most {balance // lines}. Please try again.")
        else:
            break
    print(f"Your current bet is ${bet}.\nYou are currently betting on {lines} line(s).")

    slots = getSlotMachineSpin(ROWS, COLS, AVAILABLE_ELEMENTS)
    displaySlotMachineSpin(slots)
    winnings, winning_lines = checkWinnings(slots, lines, bet, ELEMENTS_VALUES)
    if winnings == 0:
        print("Better luck next time!")
    else:
        print(f"Congratulations, you won ${winnings}.")
        print(f"You won on line(s)", *winning_lines)
    
    return winnings - total_bet



def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        spin_prompt = input("Press enter to play. Press q to quit.\n")
        if spin_prompt == 'q':
            break
        balance += spin(balance)
    
    print(f"Your final balance is ${balance}. Have a nice day")

main()