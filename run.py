# Connecting to google sheets API following love sandwiches walkthrough project
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT =gspread.authorize(SCOPED_CREDS)

SHEET = GSPREAD_CLIENT.open("personal-finance-pp3")

expenses_categories = {
    "1": "Housing",
    "2": "Transportation",
    "3": "Groceries",
    "4": "Utilities",
    "5": "Medical & Healthcare",
    "6": "Personal Spending",
    "7": "Leisure",
    "8": "Others"
}

income_categories = {
    "1": "Salary & Wages",
    "2": "Investment returns",
    "3": "Rental Income",
    "4": "Others"
}

def display_menu():
    """
    Displays the menu of options in the terminal
    """
    print("What would you like to do?\n")
    print("1. Check balance")
    print("2. Check expenses summary by category")
    print("3. Check income summary by category")
    print("4. Add a new expense")
    print("5. Add a new income\n")

    # Validates option, based on love sandwiches walkthrough project
    while True:
        choice = input("Please chosse an option by typing a number from the menu above: ")

        if validate_choice(choice):
            break

    return choice

def evaluate_choice(choice):
    """
    Evaluates the user choice and calls the respective functions.
    """
    if int(choice) == 1:
        balance = calculate_balance()
        display_balance(balance)
    elif int(choice) == 2:
        expenses_by_category = calculate_expenses_by_category()
        print(expenses_by_category)
    elif int(choice) == 3:
        print("choice: check income summary.\n")
    elif int(choice) == 4:
        print("choice: add new expense.\n")
    elif int(choice) == 5:
        print("choice: add ne income.\n")

def calculate_balance():
    """
    Gets data from spreadsheet. Calculates and returns the balance.
    """
    expenses = SHEET.worksheet("expenses").col_values(1)[1:]
    incomes = SHEET.worksheet("income").col_values(1)[1:]
    total_expenses = 0
    total_income = 0
    for expense in expenses:
        total_expenses += float(expense)
    for income in incomes:
        total_income += float(income)
    return total_income - total_expenses

def display_balance(balance):
    """
    Displays the current balance to the terminal.
    """
    print(f"Your current balance is: ${balance:.2f}\n") 

def calculate_expenses_by_category():
    """
    Calculate the total amount spent for each expense category.
    """
    expenses = SHEET.worksheet("expenses").col_values(1)
    worksheet_categories = SHEET.worksheet("expenses").col_values(2)
    expenses_by_category = {key: 0 for key in expenses_categories.values()}
    for value in expenses_categories.values():
        for expense, category in zip(expenses, worksheet_categories):
            if value.lower() == category:
                expenses_by_category[value] += float(expense)
    return expenses_by_category

# Validation method inspired by love sandwiches walkthrough project
def validate_choice(choice):
    """
    Tries to convert choice into an integer and checks if it is in the range
    of possible choices. Raises ValueError if cannot convert into an integer or
    if it is outside of range.
    """
    try:
        int(choice)
        if int(choice) not in range(1,6):
            raise ValueError("Option not found.")
    except ValueError as e:
        print(f"{e}. Try again.")
        return False
    return True

def main():
    """
    Calls functin for displaying the menu to the terminal, then calls function to evaluate the user choice.
    """
    print("Welcome to your personal finance.\n")
    choice = display_menu()
    evaluate_choice(choice)
    
    while True:
        again = input("Would you like to do something else? (Y/N)")
        if again.upper() == "Y":
            choice = display_menu()
            evaluate_choice(choice)
        elif again.upper() == "N":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid answer, please type Y or N.\n")   

main()
