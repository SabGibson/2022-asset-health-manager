"""
Import external libraries for working with google drive adn sheets API.
...
"""
from pprint import pprint
import sys
from tkinter.tix import InputOnly
import gspread
from google.oauth2.service_account import Credentials
from time import sleep
from art import *

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
    'Finacne Health Manager' is printed and held for 2 seconds.
    """
    tprint("Finance Health Manager")
    sleep(2)

def create_usrname():
    """
    create_usrname() -> string 
    part of new_user_protocol function used to accept user input as name, and validate name is unique in sheet
    username is to be used as unique ID and forign key to qurey data as a dict

    """
    valid_uname = False
    all_usrs = users.col_values(1)
    while (valid_uname is False):
        try:
            entrd_ursname = input("Please enter username")
            if entrd_ursname in all_usrs:
                raise ValueError
            
            valid_uname = True
            return entrd_ursname
        except ValueError:
            print("Username taken.")       

        
def calc_salary():

    """
    calc_salary() -> float 
    step 1) Get salary in monthly and weekly terms
    step 2) Calculate pension contribution
    step 3) Calculate taxable income
    step 4) calculate tax rate
    step 5) Calculate NI contributions
    step 6) Calculate student loan repayments 
    step 7) Calculate take home pay 
    """
    
    valid_sal = False
    valid_pension = False
    tax_free_allowence = 0
    student_loan_inpt_valid = False

    ## step 1 

    ## validate user input

    while (valid_sal is False):
        try:
            salary_pre_tax = input("Please input pre-tax salary per annum")
            if salary_pre_tax.isnumeric:
                salary_pre_tax = float(salary_pre_tax)
                valid_sal = True
            else:
                raise ValueError

        except ValueError:
            print("Please enter a valid salary as a number")       
    
    pay_pm = salary_pre_tax/12
    print(f"Salary per year: {salary_pre_tax}, slary per month = {pay_pm}")

    ## step 2
    
    ## validate user input

    while (valid_pension is False):
        try:
            pension = input("Enter pension contribution percentage")
            if pension.isnumeric:
                pension = int(pension)
                valid_pension = True
            else:
                raise ValueError

        except ValueError:
            print("Please enter a valid pension as a number")       
    
    pension_deduction_pa = salary_pre_tax * (pension*0.01)
    pension_deduction_pm = pension_deduction_pa/12
    print("pension",pension_deduction_pa,pension_deduction_pm)

    
    ## step 3 

    if salary_pre_tax > 125000 :
        tax_free_allowence = 0
    else:
        tax_free_allowence = 12570    

    taxable_income = salary_pre_tax - tax_free_allowence
    taxable_income_pm = taxable_income/12

    print("taxable income:",taxable_income,tax_free_allowence)

    ## step 4 calculate tax 

    if salary_pre_tax < 37701:
        tax_rate = 0.2
    elif salary_pre_tax < 150001:
        tax_rate = 0.4
    else:
        tax_rate = 0.45
    
    ## step 5

    if (taxable_income_pm > 792 ) and (taxable_income_pm <= 4167 ):
        ni_contributions = 0.12*(taxable_income_pm)
    elif taxable_income_pm > 4167:
        ni_contributions = 0.12*4167 + 0.02*(taxable_income_pm-4167)  

    else:
        ni_contributions = 0  

    print("ni contri", ni_contributions)
    ## step 6 

    ## validate user input
    
    while student_loan_inpt_valid is False:
        try:
            print("""

            Please select 1 or 2. Or 0.
                0)	No student loan
                1)	Student loan type 1
                2)	Student loan type 2

            """)
            student_loan_inpt = input("please enter 0,1 or 2")
            allowed_inputs = "123"
            if (student_loan_inpt not in allowed_inputs):
                raise ValueError
            student_loan_inpt_valid = True

        except ValueError:
            print("Please enter a valid option")

    if student_loan_inpt == "1":
        student_loan = 0.09*(pay_pm-1615)
    elif student_loan_inpt == "2":
        student_loan = 0.09*(pay_pm-2214) 
    else:
        student_loan = 0 

    total_deductions = student_loan + ni_contributions + (tax_rate*taxable_income_pm) + pension_deduction_pm
    take_home_pay = pay_pm - total_deductions

    print("takehome",take_home_pay,"total ded",total_deductions) 



def calc_balance_sheet():
    """
    Balance sheet asks the user questions about monthyly expenses.
    There are 5 fields in total in this section to fill
    it dosent observe the salaray on a granular level and instead is fluid
     
     """

    valid_rent = False
    valid_util = False
    valid_ent = False
    valid_shop = False
    valid_misc = False
    
    print("Please enter your rent contributions: ")
    while (valid_rent is False):
        try:
            usr_rent = input("Enter Value")
            if usr_rent.isnumeric:
                usr_rent = int(usr_rent)
                valid_rent = True
            else:
                raise ValueError

        except ValueError:
            print("Please enter a valid number")

    print("Please enter your utility bill contributions: ")
    while (valid_util is False):
        try:
            usr_utility = input("Enter Value")
            if usr_utility.isnumeric:
                usr_utility = int(usr_utility)
                valid_util= True
            else:
                raise ValueError

        except ValueError:
            print("Please enter a valid number")
    
    print("Please enter your entertainment spend: ")
    while (valid_ent is False):
        try:
            usr_ent = input("Enter Value")
            if usr_ent.isnumeric:
                usr_ent = int(usr_ent)
                valid_ent = True
            else:
                raise ValueError

        except ValueError:
            print("Please enter a valid number")

    print("Please enter your grocery spend: ")
    while (valid_shop is False):
        try:
            usr_shop= input("Enter Value")
            if usr_shop.isnumeric:
                usr_shop = int(usr_shop)
                valid_shop = True
            else:
                raise ValueError

        except ValueError:
            print("Please enter a valid number")

    print("Please enter your miscillaneous spend: ")
    while (valid_misc is False):
        try:
            usr_misc = input("Enter Value")
            if usr_misc.isnumeric:
                usr_misc = int(usr_misc)
                valid_misc = True
            else:
                raise ValueError

        except ValueError:
            print("Please enter a valid number")


    usr_bills = [usr_rent,usr_utility,usr_ent,usr_shop,usr_misc]

    #balance_sheet.append_row(usr_bills)

    print(usr_bills)

    return usr_bills





def get_insights(account:list):
    """
    DOCSRTING
    """


    


def new_user_protocol():
    """
    new_user_protocol function hosts functions used to register new users
    """

    account_user_name = create_usrname()

    calc_salary()

    balance_sheet = calc_balance_sheet()

    get_insights(balance_sheet)




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


splash_screen()
calc_salary()
