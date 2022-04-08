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

# Variable setup for connection to Google Sheets
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Stock Allocation Tool: Dummy Data')
inventory_data = SHEET.worksheet('dummy data')


# Declaration of initial variables
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


class Row:
    """ A dictionary constructor for each row in the dataset """
    def __init__(self, sku, country, price, revenue, units_sold, daily_average, available, inbound, days_supply):
        self.sku = sku
        self.country = country
        self.price = price
        self.revenue = revenue
        self.units_sold = units_sold
        self.daily_average = daily_average
        self.available = available
        self.inbound = inbound
        self.days_supply = days_supply


num_of_total_rows = len(inventory_data.col_values(1)) + 1
print(f"\nThere are {num_of_total_rows} rows in total.\n")
master_dict = {}

for i in range(1, num_of_total_rows):
    current_row = inventory_data.row_values(i)
    key = current_row[0] + '_' + current_row[1]
    value = Row(current_row[0], current_row[1], current_row[2], current_row[3], current_row[4], current_row[5], current_row[6], current_row[7], current_row[8])
    master_dict[key] = value

print(f"\nPrinting master dictionary...\n")
pprint(master_dict)
print(master_dict.get("Test SKU1_NA"))

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

    options = ["1) Specific SKU data", "2) SUM or AVERAGE of entire row/column", "3) All values from entire row/column"]
    print("What data would to like to query?")
    time.sleep(1)

    for option in options:
        print(f"{option}\n")
        time.sleep(0.5)

    x = int(input(f"To select an option, type the corresponding number, and press Enter.\n"))

    if x == 1:
        print("Retreiving SKUs...")
        # target = target_SKU()
        pprint(inventory_data.get_all_records())
        target = input("Which SKU would you like to query?")
        # Run a function to proceed with request here, taking target as parameter
    elif x == 2:
        print("What operation will you request?")
        # Run a function to print a list of multiple options, SUM, AVERAGE, RANGE
    elif x == 3:
        print("Which row or column would you like to examine?")
        # Run a function to target and return values from a row or column
    else:
        print("Input not recognised. Please try again.")


def target_SKU():
    """

    """


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


# main()
