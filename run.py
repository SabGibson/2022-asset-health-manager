"""
Import external libraries for working with google drive adn sheets API.
...
"""

import sys
from time import sleep
import gspread
from google.oauth2.service_account import Credentials
from art import tprint

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

workpages = [users,salary,balance_sheet,insights]

def splash_screen():

    """
    splash_screen() -> None 
    
    function takes no arguments and prints welcome message and service name for user.
    'Finance Health Manager' is printed and held for 2 seconds.
    """
    # tprint() form art lib prints ascii art 
    tprint("FHM")
    print("Finance Health Manager")

    #Hold splash screen with sleep 
    sleep(2)

def create_usrname():

    """
    create_usrname() -> string 

    part of new_user_protocol function used to accept user input as name, and validate name is unique in sheet
    username is to be used as unique ID and foreign key to query data as a dict

    """
    valid_uname = False
    all_usrs = users.col_values(1)
    while (valid_uname is False):
        try:
            entrd_ursname = input("Please enter username:\n")
            if entrd_ursname in all_usrs:
                raise ValueError

            if len(entrd_ursname)<=2:
                raise AttributeError
            
            valid_uname = True
            users.append_row([entrd_ursname])  
            return entrd_ursname
        except ValueError:
            print("Username taken.")
        except AttributeError:
            print("username too short")

       

        
def calc_salary(usrname):

    """
    calc_salary(usrname) -> float 

    step 1) Get salary in monthly and weekly terms
    step 2) Calculate pension contribution
    step 3) Calculate taxable income
    step 4) calculate tax rate
    step 5) Calculate NI contributions
    step 6) Calculate student loan repayments
    step 7) Calculate take home pay
    """
    # validation loop variables
    valid_sal = False
    valid_pension = False
    student_loan_inpt_valid = False

    ## step 1
    ## validate user input

    while (valid_sal is False):
        try:
            salary_pre_tax = input("Please input pre-tax salary per annum:\n")
            if salary_pre_tax.isnumeric:
                salary_pre_tax = round(float(salary_pre_tax))
                valid_sal = True
            else:
                raise ValueError

        except ValueError:
            print("Please enter a valid salary as a number ")       
    
    pay_pm = salary_pre_tax/12
    sleep(0.8)
    print(f"Pre-tax salary per year entered: £{salary_pre_tax}\n pre-tax slary per month: £{pay_pm}")
    sleep(0.4)

    ## step 2
    
    ## validate user input

    while (valid_pension is False):
        try:
            pension = input("Enter pension contribution percentage:\n")
            if pension.isnumeric:
                if (0<= int(pension) <= 45):
                    pension = int(pension)
                    valid_pension = True
                else:
                    raise AttributeError
            else:
                raise ValueError

        except ValueError:
            print("Please enter a valid pension as a number")

        except AttributeError:
            print("Please enter a value between 0 and 45 (extremes included)")       
    
    pension_deduction_pa = salary_pre_tax * (pension*0.01)
    pension_deduction_pm = pension_deduction_pa/12
    sleep(1)
    print(f"Pension contribution is {pension}%; £{pension_deduction_pm} is deducted per month.")

    
    ## step 3 

    if salary_pre_tax > 125000 :
        tax_free_allowence = 0
    else:
        tax_free_allowence = 12570    

    taxable_income = salary_pre_tax - tax_free_allowence
    taxable_income_pm = taxable_income/12
    sleep(0.5)
    print(f"Taxable income with tax-free allowence of 12570 is £{taxable_income_pm} per month")
    sleep(1)

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

    print(f"National insurance contributions are £{ni_contributions} per month")
    sleep(0.5)
    ## step 6 

    ## validate user input
    
    while student_loan_inpt_valid is False:
        try:
            print("Please select one of the options below 1 ,2 or 0. \n 0)	No student loan\n1)	Student loan type 1 \n 2) Student loan type 2")
            student_loan_inpt = input("\n")
            allowed_inputs = "123"
            if (student_loan_inpt not in allowed_inputs) or (len(student_loan_inpt) > 1):
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
    sleep(1)
    print(f"Take home pay after deductions is: £{take_home_pay}.\n Total deductions are: £{total_deductions} ")

    salary.append_row([usrname,take_home_pay,pension_deduction_pm,student_loan,ni_contributions]) 

    return take_home_pay


def calc_balance_sheet(usrname):

    """
    calc_balance_sheet(usrname:str) -> [] 

    Balance sheet asks the user questions about monthly expenses.
    There are 5 fields in total in this section to fill
    it doesn’t observe the salary on a granular level and instead is fluid
     """

    valid_rent = False
    valid_util = False
    valid_ent = False
    valid_shop = False
    valid_misc = False
    
    print("Please enter your rent contributions: ")
    while (valid_rent is False):
        try:
            usr_rent = input("Enter Value:\n")
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
            usr_utility = input("Enter Value:\n")
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
            usr_ent = input("Enter Value:\n")
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
            usr_shop= input("Enter Value\n")
            if usr_shop.isnumeric:
                usr_shop = int(usr_shop)
                valid_shop = True
            else:
                raise ValueError

        except ValueError:
            print("Please enter a valid number")

    print("Please enter your miscellaneous spend: ")
    while (valid_misc is False):
        try:
            usr_misc = input("Enter Value:\n")
            if usr_misc.isnumeric:
                usr_misc = int(usr_misc)
                valid_misc = True
            else:
                raise ValueError

        except ValueError:
            print("Please enter a valid number")


    usr_bills = [usrname,usr_rent,usr_utility,usr_ent,usr_shop,usr_misc]

    balance_sheet.append_row(usr_bills)

    return usr_bills[1:]





def get_insights(usrname:str,sal:float,account:list):

    """
    get_insights(usrname:str,sal:float,account:list) -> None
    observes spend by comparing expesses as percentage of take home pay and delivers insights
    """
    insight = [usrname]
    infraction_count = 0
    print(account)

    rent_percent = round((account[0]/sal)*100)
    util_percent = round((account[1]/sal)*100)
    ent_percent = round((account[2]/sal)*100)
    shop_percent = round((account[3]/sal)*100)
    misc_percent = round((account[4]/sal)*100)

    if rent_percent > 35:
        print(f"You spend {rent_percent}% of your salary on rent! Consider alternatives.")
        infraction_count +=1
    insight.append(rent_percent)

    
    if util_percent > 25:
        print(f"You spend {util_percent}% of your salary on utilities! Too high!.")
        infraction_count +=1
    insight.append(util_percent)

    if ent_percent > 5:
        print(f"You spend {ent_percent}% of your salary on entertainment! Cancell subscriptions.")
        infraction_count +=1
    insight.append(ent_percent)

    if shop_percent > 15:
        print(f"You spend {shop_percent}% of your salary on gorgeries! Consider alternatives.")
        infraction_count +=1
    insight.append(shop_percent)

    if misc_percent > 3:
        print(f"You spend {misc_percent}% of your salary on miscellaneous items! Cut out waste.")
        infraction_count +=1
    insight.append(misc_percent)

    if infraction_count > 3:
        print("Managment strategy needs improvment. URGENT")
        insight.append("NO")
    else:
        print("Balance sheet healthy! Keep it up!")
        insight.append("Yes")
    
    insights.append_row(insight)



def new_user_protocol():
    """
    new_user_protocol function hosts functions used to register new users
    """

    account_user_name = create_usrname()

    usr_sal = calc_salary(account_user_name)

    usr_finances = calc_balance_sheet(account_user_name)

    get_insights(account_user_name,usr_sal,usr_finances)


def view_existing_usr():
    
    """
    view_existing_user()
    """
    valid_uname = False
    all_usrs = users.col_values(1)
    while (valid_uname is False):
        try:
            entrd_ursname = input("Please enter username to view or 'q' to quit\n")

            if entrd_ursname == "q":
                sys.exit()

            elif entrd_ursname not in all_usrs:
                raise ValueError
            
            
            
            valid_uname = True
            index = users.find(entrd_ursname).row

            sal_data = salary.row_values(index)
            insights_data = insights.row_values(index)
            print("Loading profile ...")
            sleep(3)
            print(f"Username: {entrd_ursname}\n Take home pay: £{sal_data[1]}\n Student Loan per month: {sal_data[3]} \n Is account in good health?: {insights_data[-1]} {insights_data[1]}% of salaray spent on rent")

        except ValueError:
            print("User not found.")


def del_existing_usr():

    """
    del_exisiting_usr()
    """

    valid_uname = False
    all_usrs = users.col_values(1)
    while (valid_uname is False):
        try:
            entrd_ursname = input("Please enter username to delete or 'q' to quit\n")
            if entrd_ursname == "q":
                sys.exit()

            elif entrd_ursname not in all_usrs:
                raise ValueError
            
            
            valid_uname = True
            print("Deleting account ...")
            sleep(2)
            cell = users.find(entrd_ursname)

            for page in workpages:
                page.delete_rows(cell.row)
            
            print("Account deleted and cannot be recovered.")

        except ValueError:
            print("User not found.")
    


def return_user_protocol():

    """
    retrun_user_protocol() -> None
    acts as interface for viewing user from sheet or deleting user information
    """
    print("Welcome back. Please choose an option below")
    sleep(1)
    print("""

    Please select 1 or 2.
        1)	view Existing User
        2)	Delete Exisiting User
        """)
    sleep(1)
    is_valid = False
    while (is_valid is False):
        try:
            choice = int(input("Please select 1 or 2. Or type 3 to quit.\n"))
            if ((choice == 1)|(choice == 2)|(choice == 3)):
                is_valid = True
            raise ValueError

        except ValueError:
            print("please enter a valid input form the options given.")
    
    if choice == 1:
        view_existing_usr()
    elif choice == 2:
        del_existing_usr()
    else:
        sys.exit()



def welcome_screen():

    """
    welcome_screen function represents the first page the user can interact with.
    It is the home pg and features three options:
    1) New User, 2) Returning User, 3) Quit 
    The input is formatted with lower() and is kept in the string format.
    The input is stored in a variable 'choice' and is validated
    Valid input required to proceed
    """

    print("Please select 1 or 2. Or type “q” to quit. \n 1)	New User – if you would like to register a new user, and complete finance assessment\n 2)	Returning User – if you would like to view, update or delete an existing profile \n 3)	Quit – to end program")

    is_valid = False

    while (is_valid == False):
        try:
            choice = int(input("Please select 1 or 2. Or 3 to quit.\n"))
            if (choice == 1) or (choice ==2) or (choice == 3):
                is_valid = True
                return choice
            else:
                raise ValueError

        except ValueError:
            print("please enter a valid input form the options given.")


def launch_interface(user_choice):
    """
    launch_interface(inpt:str) it accepts user choice from earlier in sequence.
    It launches corrisponding function for each user experience type 'new' or 'returning'
    output of function is 
    """

    print("launching...")
    sleep(2)
    if user_choice == 1:
        new_user_protocol()
    else:
        return_user_protocol()


def main ():
    splash_screen()
    user_choice = welcome_screen()

    if (user_choice == 3):
        print("Thank you! Bye!")
        sleep(3)
        sys.exit()
    else:
        launch_interface(user_choice)

main()
