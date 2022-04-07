# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
import time

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
    time.sleep(1.5)
    for option in options:
        print(f"{option}\n")
    selection = input(f"To select an option, type the corresponding number, and press Enter.\n")
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
    time.sleep(2)
    col_values = inventory_data.col_values(col)
    pprint(col_values)
    return col_values


def get_all_data():
    """
    Returns and prints all values from the connected worksheet.
    """
    print(f"Retrieving data...\n")
    time.sleep(2)
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


def quit_program():
    """
    """
    print("Exiting application...")
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
        all_data = get_all_data()
        pprint(all_data)
    elif x == 6:
        quit_program()
    else:
        print(f"Input not recognised, please try again.\n")


def main():
    introduction()
    time.sleep(2)

    while True:
        x = int(show_menu())
        handle_input(x)

main()
