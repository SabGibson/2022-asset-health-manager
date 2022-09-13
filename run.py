"""
Import external libraries for working with google drive adn sheets API.
...
"""
from pprint import pprint
import sys
import gspread
from google.oauth2.service_account import Credentials
from time import sleep

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("finance-health-manager-db")

users = SHEET.worksheet("users")
salary = SHEET.worksheet("salary")
balance_sheet = SHEET.worksheet("balance-sheet")
insights = SHEET.worksheet("insights")


def main ():
    splansh_screen()
    user_choice = welcome_screen()

    if (user_choice == "q"):
        print("Thank you! Bye!")
        sleep(3)
        sys.exit()
    else:
        launch_interface(user_choice)
