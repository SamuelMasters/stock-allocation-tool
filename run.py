# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
import time
import csv
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
dos_target = 50
master_dict = {}
sku_list = []
pick_list = []
headers = ["SKU", "Country", "Price", "30-Day Revenue", "30-Day Sales", "Daily Average", "Available Units", "Inbound Units", "Days of Supply (inc. Inbound"]
# Used to provide information in row queries


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
    options = ["1) Instructions", "2) Capture New Snapshot",
                "3) Export Replenishment",
                "4) Adjust Variables", "5) Query Data", "6) Exit"]
    print(f"{'-' * 50}")
    print("Please select an operation:\n")
    time.sleep(1)
    for option in options:
        print(f"{option}\n")
        time.sleep(0.5)

    while True:
        try:
            selection = int(input("To select an option, type the corresponding number, and press Enter.\n"))
            if selection not in range(1, 7):
                raise ValueError(
                    f"Please enter a value between 1 and 6, you entered {selection}"
                )
            break
        except ValueError as e:
            print(f"Invalid data: {e}. Please try again.\n")

    return selection


def instructions():
    """
    Prints instructions about the operation of the application
    to the user.
    """
    print(f"\n{'-' * 50}\n")
    print("\nWelcome to the Stock Allocation Tool!")
    print(
        "\nThis application connects to an external Google Sheet containing "
        "inventory and sales data, and provides recommendations about what "
        "stock should be replenished."
    )
    input("\nPress Enter to continue...\n")
    print(
        "Please note that this application is purely for educational "
        "purposes, and is intended as a proof of concept rather than "
        "a complete product."
    )
    input("\nPress Enter to continue...\n")
    print(f"\n{'-' * 50}\n")
    print("\n'Capture New Snapshot'")
    print(
        "\nThis option captures and saves data from the connected Google "
        "Sheet, and allows that data to then be used within this "
        "application. Please note, this process is carried out "
        "automatically when booting up. Therefore, this function should "
        "be used if data is changed in the Google Sheet whilst the "
        "application is already running."
    )
    input("\nPress Enter to continue...\n")
    print(f"\n{'-' * 50}\n")
    print("\n'Export Replenishment'")
    print(
        "\nThis option reads the data from the connected Google Sheet, and "
        "uses it to calculate a recommended amount of stock to replenish for "
        "each SKU, in each market. The calculation for this is as follows: "
    )
    print(
        "\nStock to Replenish = ((Target Days of Supply - Current Days of "
        "Supply) * Daily Average) * Overstock Multiplier\n"
    )
    input("\nPress Enter to continue...\n")
    print(
        "The default values for 'Target Days of Supply' and 'Overstock "
        "Multiplier' are 50 and 1, respectively. If you so wish, these "
        "values can be changed by using the 'Adjust Variables' option "
        "from the main menu."
    )
    input("\nPress Enter to continue...\n")
    print(f"\n{'-' * 50}\n")
    print("\n'Adjust Variables'")
    print(
        "\nThis option allows the user to manually change the values "
        "of the 'Target Days of Supply' and 'Overstock' variables, "
        "which as described above, are a key part of the "
        "replenishment calculation."
    )
    input("\nPress Enter to continue...\n")
    print(f"\n{'-' * 50}\n")
    print("\n'Query Data'")
    print(
        "\nThis option allows the user to examine the saved data "
        "on a more granular level. You can choose to examine "
        "information for a specific SKU, look at all values in a "
        "given row or column, or calculate the SUM, MEAN AVERAGE, "
        "or RANGE of a given column."
    )
    input("\nPress Enter to continue...\n")
    print(f"\n{'-' * 50}\n")
    print("\n'Exit'")
    print(
        "\nThis option allows the user to safely end the program."
    )
    input("\nPress Enter to return to main menu...\n")


class Row:
    """ A class for each row object in the dataset """
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


def capture_data():
    """
    Captures a snapshot of the current dataset, and creates an
    object for each row within it using the Row constructor.
    """
    print("Capturing data snapshot...\n")
    num_of_total_rows = len(inventory_data.col_values(1)) + 1
    print("Parsing data rows...\n")

    for i in range(1, num_of_total_rows):
        current_row = inventory_data.row_values(i)
        key = current_row[0] + '_' + current_row[1]
        value = Row(current_row[0], current_row[1], current_row[2], current_row[3], current_row[4], current_row[5], current_row[6], current_row[7], current_row[8])
        master_dict[key] = value
        sku_list.append(key)

    del master_dict["Merchant SKU_Country"] # Delete the entry containing headers only
    print("Data cached successfully!\n")
    print("Moving to main menu...\n")
    time.sleep(3)


def adjust_variables():
    """
    Changes global variables according to user input.
    """
    global overstock
    global dos_target
    print("\n1) Overstock\n")
    print("2) Days of Supply Target\n")

    while True:
        x = int(input("What variable would you like to change? Please type a number and press Enter.\n"))
        if handle_other_input(x, "variables") is True:
            break

    if x == 1:
        print(f"\nThe current overstock multiplier is set to {overstock}.\n")
        time.sleep(2)

        while True:
            try:
                overstock = float(input("Please type a multiplier in to "
                "represent desired overstock, as either a whole number "
                "or a number to one decimal place (e.g. 1.2).\n"))
                break
            except ValueError as e:
                print(f"\nInvalid input: {e}. Please try again.\n")

        print(f"\nAdjusting overstock to {overstock}...")
        time.sleep(2)
        print("\nOverstock variable successfully changed.\n")
        input("Press Enter to return to main menu...")

    elif x == 2:
        print(f"\nThe current days of supply target is set to {dos_target}.\n")
        time.sleep(2)

        while True:
            try:
                dos_target = int(input("Please enter a whole number to represent desired "
                "days of supply target.\n"))
                break
            except ValueError as e:
                print(f"\nInvalid input: {e}. Please try again.\n")

        print("\nAdjusting variable...\n")
        time.sleep(2)
        print(f"\nThe days of supply target is now set to {dos_target}.\n")
        input("Press Enter to return main menu...")


def query_data():
    """
    Presents options to the user that allow them to query specific
    data points or calculations within the connected dataset.
    """

    options = ["1) Specific SKU data", "2) SUM, AVERAGE or RANGE of entire column", "3) All values from an entire row"]
    print("\nWhat type of query would you like to make?\n")
    time.sleep(1)

    for option in options:
        print(f"{option}\n")
        time.sleep(0.5)

    x = int(input("To select an option, type the corresponding number, and press Enter.\n"))

    if x == 1:
        print("Retrieving SKU list...")
        pprint(sku_list)

        while True:
            target = input("Which SKU would you like to query? Please type it exactly as it appears in the list, without quotation marks, and press Enter.\n")
            if handle_other_input(target, "sku exist"):
                break

        print("\nValid SKU entered!\n")
        query_sku(target)

    elif x == 2:
        options = ["1) Price", "2) 30-Day Revenue", "3) 30-Days Units Sold",
                   "4) 30-Day Daily Average", "5) Available Units",
                   "6) Inbound Units", "7) Days of Supply "
                   "(inc. Inbound)"]

        print("\nWhat data would you like to perform a calculation on?\n")

        for option in options:
            print(f"{option}\n")
            time.sleep(0.5)

        while True:
            try:
                y = int(input("To select an option, type the corresponding "
                              "number, and press Enter.\n"))
                if y not in range(1, 8):
                    raise ValueError(
                        "Please enter a value between 1 and 7, you "
                        f"entered {y}"
                    )
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.\n")

        print("\nWhat calculation would you like to perform on the column?\n")

        options = ["1) SUM of data", "2) AVERAGE of data", "3) RANGE of data"]

        for option in options:
            print(f"{option}\n")
            time.sleep(0.5)

        while True:
            try:
                z = int(input("To select an option, type the corresponding "
                              "number, and press Enter.\n"))
                if z not in range(1, 4):
                    raise ValueError(
                        "Please enter a value between 1 and 3, you "
                        f"entered {z}"
                    )
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.\n")

        y += 2 # Adjust number for use in following queries

        if z == 1: # SUM query
            raw_col = inventory_data.col_values(y)
            del raw_col[0] # Removes the header string from column
            float_list = []

            for i in raw_col: # Create a new list with floats
                float_list.append(float(i))

            col_sum = round(sum(float_list), 2)
            print(f"The sum of all values from the "
                  f"specified column is {col_sum}.\n")
            input("Press Enter to return to main menu...")
        elif z == 2: # AVERAGE query
            raw_col = inventory_data.col_values(y)
            del raw_col[0] # Removes the header string from column
            float_list = []

            for i in raw_col: # Create a new list with floats
                float_list.append(float(i))

            col_average = round(sum(float_list) / len(float_list), 2)
            print("The mean average of all values from "
                 f"the specified list is {col_average}.")
            input("Press Enter to return to main menu...")
        elif z == 3: # RANGE query
            raw_col = inventory_data.col_values(y)
            del raw_col[0] # Removes the header string from column
            float_list = []

            for i in raw_col: # Create a new list with floats
                float_list.append(float(i))

            col_min = round(min(float_list), 2)
            col_max = round(max(float_list), 2)

            print("\nThe smallest value in the specified data is "
                 f"{col_min}.")
            print("\nThe largest value in the specified data is "
                 f"{col_max}.")
            input("\nPress Enter to return to main menu...")

    elif x == 3:
        num_of_total_rows = len(inventory_data.col_values(1))
        print(f"\nThere are {num_of_total_rows} total rows. Which "
              "would you like to examine?")

        while True:
            try:
                x = int(input(f"\nPlease type a whole number between 1 and "
                              f"{num_of_total_rows}.\n"))
                if x not in range(1, num_of_total_rows):
                    raise ValueError(
                        f"\nPlease enter a whole number between 1 and "
                        f"{num_of_total_rows}, you entered {x}.\n"
                    )
                break
            except ValueError as e:
                print(f"Invalid data: {e}. Please try again.\n")

        find_row(x)

    else:
        print("Input not recognised. Please try again.")


def query_sku(sku):
    """
    Retrieves specific data points from master_dict for user-specified SKU.
    """
    options = ["1) Price", "2) 30-Day Revenue", "3) 30-Day Units Sold", "4) 30-Day Daily Average", "5) Units Available in Stock", "6) Units Inbound to Warehouse", "7) Days of Supply (exc. Inbound Stock)", "8) Days of Supply (inc. Inbound Stock)"]
    print("\nWhat data do you wish to see for this SKU?\n")
    time.sleep(1)

    for option in options:
        print(f"{option}\n")
        time.sleep(0.5)

    while True:
        x = int(input("To select an option, type the corresponding number, and press Enter.\n"))
        if handle_other_input(x, "sku operation"):
            break

    if x == 1:
        # Return price
        z = master_dict[sku].price
        print(f"The price of {sku} is {z}.\n")
        input("Press enter to continue...")
    elif x == 2:
        # Return revenue
        z = master_dict[sku].revenue
        print(f"In the last 30 days, {sku} has brought in {z} in revenue.")
        input("Press enter to continue...")
    elif x == 3:
        # Return units sold
        z = master_dict[sku].units_sold
        print(f"In the last 30 days, {sku} has sold {z} units.")
        input("Press enter to continue...")
    elif x == 4:
        # Return daily average
        z = master_dict[sku].daily_average
        print(f"Over the last 30 days, on average, {sku} has sold {z} units each day.")
        input("Press enter to continue...")
    elif x == 5:
        # Return available units
        z = master_dict[sku].available
        print(f"There are currently {z} units available to buy for {sku}.")
        input("Press enter to continue...")
    elif x == 6:
        # Return inbound units
        z = master_dict[sku].inbound
        print(f"There are currently {z} units inbound to the warehouse for {sku}.")
        input("Press enter to continue...")
    elif x == 7:
        # Return DoS (exc. Inbound)
        z = float(master_dict[sku].available) / float(master_dict[sku].daily_average)
        print(f"Excluding inbound stock, {sku} has {z} days of supply remaining.")
        input("Press enter to continue...")
    elif x == 8:
        # Return DoS (inc. Inbound)
        z = master_dict[sku].days_supply
        print(f"Including inbound stock, {sku} has {z} days of supply remaining.")
        input("Press enter to continue...")


def find_row(row):
    """
    Find and prints all values from a specified row.
    """

    target_row = inventory_data.row_values(row)
    pprint(headers)
    pprint(target_row)

    input("\nPress Enter to return to main menu...")


def calculate_replenishment():
    """
    Reads data and calculates required replenishment per SKU
    to hit days of supply target variable.
    """
    for key in master_dict:
        daily_average = float(master_dict[key].daily_average)
        current_dos = int(float(master_dict[key].days_supply))
        if current_dos < dos_target:
            stock_to_send = int((dos_target - current_dos) * daily_average)
            adjusted_stock_to_send = stock_to_send * overstock
            entry = str(key + ' : ' + str(adjusted_stock_to_send))
            pick_list.append(entry)

    print("\nPrinting final pick list...\n")
    pprint(pick_list)
    input("\nPress Enter to continue...")
    # with open(r'C:\Temp\picklist.txt', 'w') as f:
    #     f.write(str(pick_list))
    # # with open('picklist.csv', 'w', newline = '') as csvfile:
    # #     my_writer = csv.writer(csvfile, delimiter = ' ')
    # #     my_writer.writerow(pick_list)


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


def handle_other_input(x, type):
    """
    Validates input across different types of user-input.
    """
    if type == "variables":
        if x in range(1, 3):
            return True
        else:
            print(f"You entered {x}, please enter either 1 or 2.\n")
            return False
    elif type == "sku exist":
        if x in master_dict:
            return True
        else:
            print("SKU not recognised - please verify spelling and try again.\n")
            return False
    # elif type == "operation query":
    #     if x == "sum" or x == "range" or x == "average":
    #         return True
    #     else:
    #         print(f"You entered {x}, please enter either 'sum', 'range' or 'average'.\n")
    #         return False
    elif type == "query data":
        if x in range(1, 4):
            return True
        else:
            print(f"You entered {x}, please enter a value between 1 and 3.\n")
            return False
    elif type == "sku operation":
        if x in range(1, 9):
            return True
        else:
            print(f"You entered {x}, please enter a number between 1 and 8.\n")
            return False
    elif type == "row query":
        if x in range(1, num_of_total_rows):
            return True
        else:
            print(f"You entered {x}, please enter a whole number between {num_of_total_rows}.\n")
            return False
    else:
        print("Debug: no block matched within handle_other_input function.")


def handle_menu_input(x):
    if x == 1:
        instructions()
    elif x == 2:
        global sku_list
        sku_list = []
        capture_data()
    elif x == 3:
        calculate_replenishment()
    elif x == 4:
        adjust_variables()
    elif x == 5:
        query_data()
    elif x == 6:
        quit_program()
    else:
        print("Input not recognised, please try again.\n")


def main():
    introduction()
    time.sleep(4)
    capture_data()

    while True:
        clear()
        x = int(show_menu())
        handle_menu_input(x)


main()
