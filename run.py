# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
import time
from os import system, name

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Stock Allocation Tool: Dummy Data')

inventory_data = SHEET.worksheet('dummy data')

data = inventory_data.get_all_values()
overstock = 1


def introduction():
    """
    Prints a welcome message to the user.
    """
    print(f"{'#' * 50}")
    print(f"{' ' * 50}")
    print("Welcome to the Stock Allocation Tool!")
    print(f"{' ' * 50}")
    print(f"{'#' * 50}")
    print(f"{' ' * 50}")


def show_menu():
    """
    Presents the main menu to the user and requests input.
    """
    options = ["1) Instructions", "2) Import Data", "3) Export Replenishment",
        "4) Adjust Variables", "5) Query Data", "6) Exit"]
    print(f"{'-' * 50}")
    print(f"Please select an operation:\n")
    time.sleep(1)
    for option in options:
        print(f"{option}\n")
        time.sleep(0.5)

    while True:
        try:
            selection = int(input(f"To select an option, type the corresponding number, and press Enter.\n"))
            if selection not in range(1,7):
                raise ValueError(
                    f"Please enter a value between 1 and 6, you entered {selection}"
                )
            break
        except ValueError as e:
            print(f"Invalid data: {e}. Please try again.\n")            

    return selection


def get_specific_value(cell):
    """
    Returns the value of a specific cell as specified by the user.
    """
    print(f"Retrieving data...\n")
    time.sleep(2)
    specific_value = inventory_data.acell(cell).value
    print(specific_value)
    return specific_value


def get_col_values(col):
    """
    Returns and prints all values from the specified column.
    """
    print(f"Retrieving data...\n")
    time.sleep(1.5)
    col_values = inventory_data.col_values(col)
    pprint(col_values)
    return col_values


def get_all_data():
    """
    Returns and prints all values from the connected worksheet.
    """
    print(f"Retrieving data...\n")
    time.sleep(1.5)
    all_data = inventory_data.get_all_values()
    return all_data


def adjust_variables():
    """
    Changes global variables according to user input.
    """
    global overstock
    print(f"The current overstock multiplier is set to {overstock}.\n")
    time.sleep(2)
    overstock = float(input(f"Please type a multiplier in to represent desired overstock.\n"))
    print(f"Adjusting variable...\n")
    time.sleep(2)
    print(f"The overstock multiplier is now set to {overstock}.\n")
    time.sleep(2)


def query_data():
    """
    Presents options to the user that allow them to query specific
    data points or calculations within the connected dataset. 
    """

    options = ["1. Specific SKU data", "2. SUM or AVERAGE of entire row/column", "3. All values from entire row/column"]
    print("What data would to like to query?")
    time.sleep(1)

    for option in options:
        print(f"{option}\n")
        time.sleep(0.5)

    x = int(input(f"To select an option, type the corresponding number, and press Enter.\n"))

    if x == 1:
        print("What SKU would you like to query?")
    elif x == 2:
        print("What operation will you request?")
    elif x == 3:
        print("Which row or column would you like to examine?")
    else:
        print("Input not recognised. Please try again.")


def clear():
    """
    Clears the CLI. Found on https://www.geeksforgeeks.org/clear-screen-python/.
    """
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def quit_program():
    """
    Closes the program. 
    """
    print("Exiting application...")
    time.sleep(2)
    clear()
    exit()


def handle_input(x):
    if x == 1:
        pass
    elif x == 2:
        pass
    elif x == 3:
        pass
    elif x == 4:
        adjust_variables()
    elif x == 5:
        query_data()
    elif x == 6:
        quit_program()
    else:
        print(f"Input not recognised, please try again.\n")


def main():
    introduction()
    time.sleep(2)

    while True:
        clear()
        x = int(show_menu())
        handle_input(x)


main()
