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


def splash_screen():
    """
    splash_screen() function takes no arguments and prints welcome message and service name for user.
    'Welcome!' is printed to screen and held for 1 second.
    'Finacne Health Manager' is printed and held for 2 seconds.
    """
    print("""
 __          __  _                          _ 
 \ \        / / | |                        | |
  \ \  /\  / /__| | ___ ___  _ __ ___   ___| |
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ |
    \  /\  /  __/ | (_| (_) | | | | | |  __/_|
     \/  \/ \___|_|\___\___/|_| |_| |_|\___(_)
                                              
                                              """)

    sleep(2)
    print("""

  ______ _                              _    _            _ _   _       __  __                                   
 |  ____(_)                            | |  | |          | | | | |     |  \/  |                                  
 | |__   _ _ __   __ _ _ __   ___ ___  | |__| | ___  __ _| | |_| |__   | \  / | __ _ _ __   __ _  __ _  ___ _ __ 
 |  __| | | '_ \ / _` | '_ \ / __/ _ \ |  __  |/ _ \/ _` | | __| '_ \  | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
 | |    | | | | | (_| | | | | (_|  __/ | |  | |  __/ (_| | | |_| | | | | |  | | (_| | | | | (_| | (_| |  __/ |   
 |_|    |_|_| |_|\__,_|_| |_|\___\___| |_|  |_|\___|\__,_|_|\__|_| |_| |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   
                                                                                                  __/ |          
                                                                                                 |___/           
                                                                                                 """)
    sleep(2)

def create_usrname():
    valid_uname = False
    all_usrs = users.col_values(1)
    while (valid_uname is False):
        try:
            entrd_ursname = input("Please enter username")
            if entrd_ursname in all_usrs:
                raise UsernameError
            
            valid_uname = True
            return entrd_ursname
        except UsernameError:
            print("Username taken.")       

        
def calc_salary():
    pass

def calc_balance_sheet():
    pass

def get_insights():
    pass


def new_user_protocol():
    """
    new_user_protocol function hosts functions used to register new users
    """

    create_usrname()

    calc_salary()

    balance_sheet = calc_balance_sheet()

    get_insights()



def return_user_protocol():
    pass


def welcome_screen():

    """
    welcome_screen function represents the first page the user can interact with.
    It is the home pg and features three options:
    1) New User, 2) Returning User, 3) Quit 
    The input is formatted with lower() and is kept in the string format.
    The input is stored in a variable 'choice' and is validated
    Valid input required to proceed
    """

    print("""

    Please select 1 or 2. Or type “q” to quit.
        1)	New User – if you would like to register a new user, and complete finance assessment
        2)	Returning User – if you would like to view, update or delete an existing profile
        3)	Quit – to end program

        """)

    is_valid = False

    while (is_valid is False):
        try:
            choice = input("Please select 1 or 2. Or type “q” to quit.")
            if ((choice != "1")|(choice != "2")|(choice != "q")):
                raise ValueError
            is_valid = True
            return choice

        except ValueError:
            print("please enter a valid input form the options given.")


def launch_interface(user_choice):
    """
    launch_interface(inpt:str) it accepts user choice from earlier in sequence.
    It launches corrisponding function for each user experience type 'new' or 'returning'
    output of function is 
    """
    if user_choice == "1":
        new_user_protocol()
    else:
        return_user_protocol()


def main ():
    splash_screen()
    user_choice = welcome_screen()

    if (user_choice == "q"):
        print("Thank you! Bye!")
        sleep(3)
        sys.exit()
    else:
        launch_interface(user_choice)

