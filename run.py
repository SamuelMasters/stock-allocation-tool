from os import system, name
import time
from pprint import pprint

import gspread
from google.oauth2.service_account import Credentials

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
num_of_total_rows = len(inventory_data.col_values(1))
overstock = 1
dos_target = 50
master_dict = {}
sku_list = []
pick_list = []
headers = ["SKU", "Country", "Price", "30-Day Revenue", "30-Day Sales",
           "Daily Average", "Available Units", "Inbound Units",
           "Days of Supply (inc. Inbound)"]
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
    print("\nMain Menu\n")
    print(f"{'-' * 50}")
    print("\nPlease select an operation:\n")
    time.sleep(1)

    for option in options:
        print(f"{option}\n")
        time.sleep(0.5)

    while True:  # Loop until valid input given
        try:
            selection = int(input("To select an option, type the corresponding"
                                  " number, and press Enter.\n"))
            if selection not in range(1, 7):
                raise ValueError(
                    "Please enter a value between 1 and 6, you "
                    f"entered {selection}."
                )
            break
        except ValueError:
            print("\nInvalid input. Please try again.\n")

    return selection


def instructions():
    """
    Prints instructions about the operation of the application
    to the user.
    """
    clear()
    print(f"{'-' * 50}")
    print("\nInstructions\n")
    print(f"{'-' * 50}")
    print("\nWelcome to the Stock Allocation Tool!")
    print(
        "\nThis application connects to an external Google Sheet containing "
        "\ninventory and sales data, and provides recommendations about what "
        "stock \nshould be replenished."
    )
    input("\nPress Enter to continue...\n")
    print(
        "Please note that this application is purely for educational "
        "purposes, \nand is intended as a proof of concept rather than "
        "a \ncomplete product."
    )
    input("\nPress Enter to continue...\n")
    clear()
    print(f"\n{'-' * 50}\n")
    print("\n'Capture New Snapshot'")
    print(
        "\nThis option captures and saves data from the connected Google "
        "Sheet, \nand allows that data to then be used within this "
        "application. \nPlease note, this process is carried out "
        "automatically when booting \nup. Therefore, this function should "
        "be used if data is changed in \nthe Google Sheet whilst the "
        "application is already running."
    )
    input("\nPress Enter to continue...\n")
    clear()
    print(f"\n{'-' * 50}\n")
    print("\n'Export Replenishment'")
    print(
        "\nThis option reads the data from the connected Google Sheet, and"
        "\n uses it to calculate a recommended amount of stock to replenish "
        "\n for each SKU, in each market. The calculation for this is as  "
        "follows:"
    )
    print(
        "\nStock to Replenish = ((Target Days of Supply - Current Days \nof "
        "Supply) * Daily Average) * Overstock Multiplier\n"
    )
    print(
        "The default values for 'Target Days of Supply' and 'Overstock "
        "Multiplier' \nare 50 and 1, respectively. If you so wish, these "
        "values can be changed by \nusing the 'Adjust Variables' option "
        "from the main menu."
    )
    input("\nPress Enter to continue...\n")
    clear()
    print(f"\n{'-' * 50}\n")
    print("\n'Adjust Variables'")
    print(
        "\nThis option allows the user to manually change the values "
        "of the 'Target Days \nof Supply' and 'Overstock' variables, "
        "which as described above, are \na key part of the "
        "replenishment calculation."
    )
    input("\nPress Enter to continue...\n")
    print(f"\n{'-' * 50}\n")
    print("\n'Query Data'")
    print(
        "\nThis option allows the user to examine the saved data "
        "on a more granular \nlevel. You can choose to examine "
        "information for a specific SKU, look at all \nvalues in a "
        "given row or column, or calculate the SUM, MEAN AVERAGE, "
        "or \nRANGE of a given column."
    )
    input("\nPress Enter to continue...\n")
    clear()
    print(f"\n{'-' * 50}\n")
    print("\n'Exit'")
    print(
        "\nThis option allows the user to safely end the program."
    )
    input("\nPress Enter to return to main menu...\n")


class Row:
    """
    A class for each row object in the dataset. Used to cache
    the connected dataset by saving each row of data as a
    new row object.
    """
    def __init__(self, sku, country, price, revenue, units_sold,
                 daily_average, available, inbound, days_supply):
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
    print("Parsing data rows...\n")

    # Create new objects for each row of data using Row class
    for i in range(1, num_of_total_rows):
        current_row = inventory_data.row_values(i)
        key = current_row[0] + '_' + current_row[1]
        value = Row(current_row[0], current_row[1], current_row[2],
                    current_row[3], current_row[4], current_row[5],
                    current_row[6], current_row[7], current_row[8])
        master_dict[key] = value
        sku_list.append(key)

    # Delete the entry containing headers only
    del master_dict["Merchant SKU_Country"]
    print("Data cached successfully!\n")
    print("Moving to main menu...\n")
    time.sleep(3)


def adjust_variables():
    """
    Changes global variables according to user input.
    """
    global overstock
    global dos_target
    clear()
    print(f"{'-' * 50}")
    print("\nAdjust Variables\n")
    print(f"{'-' * 50}")
    time.sleep(0.5)
    print("\n1) Overstock\n")
    time.sleep(0.5)
    print("2) Days of Supply Target\n")
    time.sleep(0.5)
    print("3) Return to Main Menu\n")
    time.sleep(0.5)

    while True:  # Loop until valid input received
        try:
            x = int(input("What variable would you like to change? Please "
                          "type a number and press Enter.\n"))
            if handle_other_input(x, "variables") is True:
                clear()
                break
        except ValueError:
            print("\nInvalid input. Please try again.\n")

    if x == 1:
        print(f"{'-' * 50}")
        print("\nAdjust Variables\n")
        print(f"{'-' * 50}")
        print(f"\nThe current overstock multiplier is set to x{overstock}\n")
        time.sleep(0.5)

        while True:  # Loop until valid input received
            try:
                overstock = float(input("Please type a multiplier in to "
                                        "represent desired overstock, as "
                                        "either a\nwhole number or a number to"
                                        " one decimal place (e.g. 1.2).\n"))
                break
            except ValueError:
                print("\nInvalid input. Please try again.\n")

        print(f"\nAdjusting overstock to {overstock}...")
        time.sleep(2)
        print("\nOverstock variable successfully changed.\n")
        input("Press Enter to return to main menu...\n")

    elif x == 2:
        print(f"{'-' * 50}")
        print("\nAdjust Variables\n")
        print(f"{'-' * 50}")
        print(f"\nThe current days of supply target is set to {dos_target}.\n")
        time.sleep(0.5)

        while True:  # Loop until valid input received
            try:
                dos_target = int(input("Please enter a whole number to "
                                       "represent desired days of supply "
                                       "target, \nand press Enter to "
                                       "confirm.\n"))
                break
            except ValueError:
                print("\nInvalid input. Please try again.\n")

        print("\nAdjusting variable...")
        time.sleep(2)
        print(f"\nThe days of supply target is now set to {dos_target}.\n")
        input("Press Enter to return main menu...\n")

    elif x == 3:  # Return to main menu
        return

    clear()


def query_data():
    """
    Presents options to the user that allow them to query specific
    data points or calculations within the connected dataset.
    """

    options = ["1) Specific SKU data",
               "2) SUM, AVERAGE or RANGE of entire column",
               "3) All values from an entire row",
               "4) Return to Main Menu"]

    clear()
    print(f"{'-' * 50}")
    print("\nQuery Data\n")
    print(f"{'-' * 50}")
    print("\nWhat type of query would you like to make?\n")
    time.sleep(1)

    for option in options:
        print(f"{option}\n")
        time.sleep(0.5)

    while True:  # Loop until valid input received
        try:
            x = int(input("To select an option, type the corresponding number,"
                          " and press Enter.\n"))
            if x not in range(1, 5):
                raise ValueError(
                    f"Please enter a value between 1 and 4, you entered {x}."
                )
            break
        except ValueError:
            print("Invalid input. Please try again.\n")

    if x == 1:
        clear()
        print(f"{'-' * 50}")
        print("\nQuery Data\n")
        print(f"{'-' * 50}")
        print("\nRetrieving SKU list...\n")
        pprint(sku_list)

        while True:  # Loop until valid input received
            target = input("\nWhich SKU would you like to query? Please "
                           "type it exactly as it appears in the\nlist, "
                           "without quotation marks, and press Enter.\n")
            if handle_other_input(target, "sku exist"):
                break

        print("\nValid SKU entered!")
        query_sku(target)

    elif x == 2:
        options = ["1) Price", "2) 30-Day Revenue", "3) 30-Days Units Sold",
                   "4) 30-Day Daily Average", "5) Available Units",
                   "6) Inbound Units", "7) Days of Supply "
                   "(inc. Inbound)", "8) Return to Main Menu"]

        clear()
        print(f"{'-' * 50}")
        print("\nQuery Data\n")
        print(f"{'-' * 50}")
        print("\nWhat data would you like to perform a calculation on?\n")

        for option in options:
            print(f"{option}\n")
            time.sleep(0.5)

        while True:  # Loop until valid input received
            try:
                y = int(input("To select an option, type the corresponding "
                              "number, and press Enter.\n"))
                if y not in range(1, 9):
                    raise ValueError(
                        "Please enter a value between 1 and 8, you "
                        f"entered {y}."
                    )
                break
            except ValueError:
                print("\nInvalid input. Please try again.\n")

        if y == 8:
            return  # Return to main menu without continuing through function

        clear()
        print(f"{'-' * 50}")
        print("\nQuery Data\n")
        print(f"{'-' * 50}")
        print("\nWhat calculation would you like to perform on the column?\n")

        options = ["1) SUM of data", "2) AVERAGE of data",
                   "3) RANGE of data", "4) Return to Main Menu"]

        for option in options:
            print(f"{option}\n")
            time.sleep(0.5)

        while True:  # Loop until valid input received
            try:
                z = int(input("To select an option, type the corresponding "
                              "number, and press Enter.\n"))
                if z not in range(1, 5):
                    raise ValueError(
                        "Please enter a value between 1 and 4, you "
                        f"entered {z}."
                    )
                break
            except ValueError:
                print("\nInvalid input. Please try again.\n")

        y += 2  # Adjust number for use in following queries

        if z == 1:  # SUM query
            raw_col = inventory_data.col_values(y)
            del raw_col[0]  # Removes the header string from column
            float_list = []

            for i in raw_col:  # Create a new list with floats
                float_list.append(float(i))

            col_sum = round(sum(float_list), 2)
            print(f"\nThe sum of all values from the "
                  f"specified column is {col_sum}.\n")
            input("Press Enter to return to main menu...\n")
        elif z == 2:  # AVERAGE query
            raw_col = inventory_data.col_values(y)
            del raw_col[0]  # Removes the header string from column
            float_list = []

            for i in raw_col:  # Create a new list with floats
                float_list.append(float(i))

            col_average = round(sum(float_list) / len(float_list), 2)
            print("\nThe mean average of all values from "
                  f"the specified list is {col_average}.\n")
            input("Press Enter to return to main menu...\n")
        elif z == 3:  # RANGE query
            raw_col = inventory_data.col_values(y)
            del raw_col[0]  # Removes the header string from column
            float_list = []

            for i in raw_col:  # Create a new list with floats
                float_list.append(float(i))

            col_min = round(min(float_list), 2)
            col_max = round(max(float_list), 2)

            print("\nThe smallest value in the specified data is "
                  f"{col_min}.")
            print("\nThe largest value in the specified data is "
                  f"{col_max}.\n")
            input("Press Enter to return to main menu...\n")
        elif z == 4:
            return  # Return to Main Menu

    elif x == 3:
        clear()
        print(f"{'-' * 50}")
        print("\nQuery Data\n")
        print(f"{'-' * 50}")
        print(f"\nThere are {num_of_total_rows} total rows. Which "
              "row would you like to examine?")

        while True:
            try:
                x = int(input(f"\nPlease type a whole number between 1 and "
                              f"{num_of_total_rows} and press Enter.\n"))
                if x not in range(1, (num_of_total_rows + 1)):
                    raise ValueError(
                        f"\nPlease enter a whole number between 1 and "
                        f"{num_of_total_rows}, you entered {x}.\n"
                    )
                break
            except ValueError:
                print("\nInvalid input. Please try again.\n")

        find_row(x)

    elif x == 4:
        return

    else:
        print("Input not recognised. Please try again.")


def query_sku(sku):
    """
    Retrieves specific data points from master_dict for user-specified SKU.
    """
    options = ["1) Price", "2) 30-Day Revenue", "3) 30-Day Units Sold",
               "4) 30-Day Daily Average", "5) Units Available in Stock",
               "6) Units Inbound to Warehouse",
               "7) Days of Supply (exc. Inbound Stock)",
               "8) Days of Supply (inc. Inbound Stock)",
               "9) Return to Main Menu"]

    clear()
    print(f"{'-' * 50}")
    print("\nQuery Data\n")
    print(f"{'-' * 50}")
    print(f"\nWhat data do you wish to see for the SKU '{sku}'?\n")
    time.sleep(1)

    for option in options:
        print(f"{option}\n")
        time.sleep(0.5)

    while True:  # Loop until valid input received
        try:
            x = int(input("To select an option, type the corresponding number,"
                          " and press Enter.\n"))
            if handle_other_input(x, "sku operation"):
                break
        except ValueError:
            print("\nInvalid input. Please try again.\n")

    if x == 1:
        # Return price
        z = master_dict[sku].price
        print(f"\nThe price of {sku} is {z}.\n")
        input("Press Enter to return to main menu...\n")
    elif x == 2:
        # Return revenue
        z = master_dict[sku].revenue
        print(f"\nIn the last 30 days, {sku} has brought in {z} in revenue.\n")
        input("Press Enter to return to main menu...\n")
    elif x == 3:
        # Return units sold
        z = master_dict[sku].units_sold
        print(f"\nIn the last 30 days, {sku} has sold {z} units.\n")
        input("Press Enter to return to main menu...\n")
    elif x == 4:
        # Return daily average
        z = master_dict[sku].daily_average
        print(f"\nOver the last 30 days, on average, {sku} has sold {z} "
              "units each day.\n")
        input("Press Enter to return to main menu...\n")
    elif x == 5:
        # Return available units
        z = master_dict[sku].available
        print(f"\nThere are currently {z} units available to buy for {sku}.\n")
        input("Press Enter to return to main menu...\n")
    elif x == 6:
        # Return inbound units
        z = master_dict[sku].inbound
        print(f"\nThere are currently {z} units inbound to the warehouse "
              "for {sku}.\n")
        input("Press Enter to return to main menu...\n")
    elif x == 7:
        # Return DoS (exc. Inbound)
        z = round((float(master_dict[sku].available) /
                  float(master_dict[sku].daily_average)), 1)
        print(f"\nExcluding inbound stock, {sku} has {z} days of supply "
              "remaining.\n")
        input("Press Enter to return to main menu...\n")
    elif x == 8:
        # Return DoS (inc. Inbound)
        z = master_dict[sku].days_supply
        print(f"\nIncluding inbound stock, {sku} has {z} days of supply "
              "remaining.\n")
        input("Press Enter to return to main menu...\n")
    elif x == 9:
        return  # Return to Main Menu


def find_row(row):
    """
    Find and prints all values from a specified row.
    """

    target_row = inventory_data.row_values(row)
    print("\nThe headers and data correspond in their order. For example, "
          "the first value\nin your selected row is situated under the 'SKU' "
          "header in the dataset.\n")
    pprint(headers)
    pprint(target_row)

    input("\nPress Enter to return to main menu...\n")


def calculate_replenishment():
    """
    Reads data and calculates required replenishment per SKU
    to hit days of supply target variable.
    """
    pick_list = []  # Clean list variable before appending fresh values
    for key in master_dict:
        daily_average = float(master_dict[key].daily_average)
        current_dos = int(float(master_dict[key].days_supply))
        if current_dos < dos_target:
            stock_to_send = int((dos_target - current_dos) * daily_average)
            adjusted_stock_to_send = round(stock_to_send * overstock)
            entry = str(key + ' : ' + str(adjusted_stock_to_send))
            pick_list.append(entry)

    clear()
    print(f"{'-' * 50}")
    print("\nExport Replenishment\n")
    print(f"{'-' * 50}")
    print("\nThe following data shows how many units should be sent "
          "to replenish \neach SKU.")
    print("\nPrinting final pick list...\n")
    time.sleep(2)
    pprint(pick_list)
    input("\nPress Enter to return to main menu...\n")


def clear():
    """
    Clears the terminal. Found on
    https://www.geeksforgeeks.org/clear-screen-python/
    """
    if name == 'nt':  # For Windows devices
        _ = system('cls')
    else:  # For non-Windows devices
        _ = system('clear')


def quit_program():
    """
    Closes the program.
    """
    print("\nExiting application...")
    time.sleep(2)
    clear()
    exit()


def handle_other_input(x, query_type):
    """
    Validates input across different types of user-input.
    """
    if query_type == "variables":
        if x in range(1, 4):
            return True
        else:
            print(f"\nYou entered {x}, please enter either 1, 2 or 3.\n")
            return False
    elif query_type == "sku exist":
        if x in master_dict:
            return True
        else:
            print("SKU not recognised - please verify spelling and try "
                  "again.\n")
            return False
    elif query_type == "query data":
        if x in range(1, 4):
            return True
        else:
            print(f"You entered {x}, please enter a value between 1 and 3.\n")
            return False
    elif query_type == "sku operation":
        if x in range(1, 10):
            return True
        else:
            print(f"You entered {x}, please enter a number between 1 and 8.\n")
            return False
    elif query_type == "row query":
        if x in range(1, num_of_total_rows):
            return True
        else:
            print(f"You entered {x}, please enter a whole number between 1 "
                  f"and {num_of_total_rows}.\n")
            return False


def handle_menu_input(x):
    """
    Validates input for inital main menu selection.
    """
    if x == 1:
        instructions()
        clear()
    elif x == 2:
        global sku_list
        sku_list = []
        capture_data()
        clear()
    elif x == 3:
        calculate_replenishment()
        clear()
    elif x == 4:
        adjust_variables()
        clear()
    elif x == 5:
        query_data()
        clear()
    elif x == 6:
        quit_program()
        clear()
    else:
        print("Input not recognised, please try again.\n")


def main():
    """
    Initiates program loop on startup.
    """
    introduction()
    time.sleep(4)
    capture_data()

    while True:
        clear()
        x = int(show_menu())
        handle_menu_input(x)


main()
