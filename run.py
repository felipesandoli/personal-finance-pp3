# Connecting to google sheets API following love sandwiches walkthrough project
import gspread
from google.oauth2.service_account import Credentials
import os

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

SHEET = GSPREAD_CLIENT.open("personal-finance-pp3")


category_dictionary = {
    "expenses_categories": {
    "1": "Housing",
    "2": "Transportation",
    "3": "Groceries",
    "4": "Utilities",
    "5": "Medical & Healthcare",
    "6": "Personal Spending",
    "7": "Leisure",
    "8": "Others",
    },

    "incomes_categories": {
        "1": "Salary & Wages",
        "2": "Investment returns",
        "3": "Rental Income",
        "4": "Others",
    }
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
    print("5. Add a new income")
    print("6. Exit\n")

    # Validates option, based on love sandwiches walkthrough project
    while True:
        choice = input(
            "Please chosse an option by typing a number from the menu above: \n"
        )

        if validate_choice(choice):
            break

    return choice


def evaluate_choice(choice):
    """
    Evaluates the user choice and calls the respective functions.
    """
    # Clear terminal, code taken from Stack Overflow
    os.system("cls" if os.name == "nt" else "clear")
    if int(choice) == 1:
        balance = calculate_balance()
        display_balance(balance)
    elif int(choice) == 2:
        expenses_by_category = calculate_amounts_by_category("expenses")
        display_amounts_by_category(expenses_by_category, "expenses")
    elif int(choice) == 3:
        income_by_category = calculate_amounts_by_category("incomes")
        display_amounts_by_category(income_by_category, "incomes")
    elif int(choice) == 4:
        confirm = ""
        while True:
            if (confirm.upper() == "") or (confirm.upper() == "N"):
                amount, category = get_amount("expense")
                print("Please confirm the category and amount:")
                print(f"{category}: ${amount}\n")
                confirm = input("Please choose Y/N, or if you like to cancel type EXIT:\n")
            if confirm.upper() == "Y":
                print(f"Adding ${amount} spent on {category} to the worksheet...")
                #add new expense to worksheet
                break
            elif confirm.upper() == "N":
                print("Erasing data...Try again.\n")
                continue
            elif confirm.upper() == "EXIT":
                print("Canceling operation...\n")
                break
            else:
                confirm = input("Invalid answer.Please type Y, N, or EXIT:")
                pass
    elif int(choice) == 5:
        amount, category = get_amount("income")
        print(f"Adding ${amount} earned from {category} to the worksheet...")
        #add new expense to worksheet
    elif int(choice) == 6:
        print("Exiting program. Goodbye!\n")


def calculate_balance():
    """
    Gets data from spreadsheet. Calculates and returns the balance.
    """
    print("Calculating balance...")
    expenses = SHEET.worksheet("expenses").col_values(1)[1:]
    incomes = SHEET.worksheet("incomes").col_values(1)[1:]
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


def calculate_amounts_by_category(type):
    """
    Calculate the total amount spent for each expense category or the total amount of income
    for each income category.
    """
    print(f"Calculating your {type} summary...")
    amounts = SHEET.worksheet(type).col_values(1)
    worksheet_categories = SHEET.worksheet(type).col_values(2)
    amounts_by_category = {key: 0 for key in category_dictionary[f"{type}_categories"].values()}
    for value in category_dictionary[f"{type}_categories"].values():
        for amount, category in zip(amounts, worksheet_categories):
            if value.lower() == category:
                amounts_by_category[value] += float(amount)
    return amounts_by_category


def display_amounts_by_category(amounts_dict, type):
    """ "
    Displays the total expenses by each category to the terminal
    """
    print(f"The total amount of {type} by each category is:\n")
    for key in amounts_dict:
        print(f"{key}: ${amounts_dict[key]:.2f}")
    print("\n")


def get_amount(type):
    """"
    Requests an amount from the user to be added as an income or expense with its
    respective category to the spreadsheet. Return the amount and category as a tuple.
    """
    print(f"Adding a new {type}...\n")
    amount = input("Please enter the amount you would like to add:\n")
    #validate_amount()
    categories = category_dictionary[f"{type}s_categories"]
    print(f"Please choose one of the following categories for this {type}\n")
    for item in categories:
        print(f"{item}: {categories[item]}")
    print("\n")
    category_index = input(f"Please enter the number corresponding to your category:\n")
    #validate_category
    return (amount, category_dictionary[f"{type}s_categories"][category_index])


# Validation method inspired by love sandwiches walkthrough project
def validate_choice(choice):
    """
    Tries to convert choice into an integer and checks if it is in the range
    of possible choices. Raises ValueError if cannot convert into an integer or
    if it is outside of range.
    """
    try:
        int(choice)
    except:
        print("Not a number. Please try again.")
        return False
    try:
        if int(choice) not in range(1, 7):
            raise ValueError("Option not found")
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
        if choice == "6":
            break
        again = input("Would you like to do something else? (Y/N)\n")
        if again.upper() == "Y":
            # Clear terminal, code taken from Stack Overflow
            os.system("cls" if os.name == "nt" else "clear")
            choice = display_menu()
            evaluate_choice(choice)
        elif again.upper() == "N":
            # Clear terminal, code taken from Stack Overflow
            os.system("cls" if os.name == "nt" else "clear")
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid answer, please type Y or N.\n")


main()