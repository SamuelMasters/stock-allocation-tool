# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

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


def introduction():
    """
    Prints a welcome message to the user.
    """
    print(f"{'#' * 50}")
    print(f"{' ' * 50}")
    print("Welcome to the stock allocation tool!")
    print(f"{' ' * 50}")
    print(f"{'#' * 50}")
    print(f"{' ' * 50}")


def show_menu():
    """
    Presents the main menu to the user and requests input.
    """
    options = ["1) Instructions", "2) Import Data", "3) Export Replenishment",
    "4) Adjust Variables", "5) Query Data", "6) Exit"]
    print(f"Please select an operation:\n")
    for option in options:
        print(f"{option}\n")
    print("To select an option, type the corresponding number, and press Enter.")


def main():
    introduction()
    show_menu()


main()
