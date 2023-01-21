# Connecting to google sheets API following love sandwiches walkthrough project
import gspread
from google.oauth2.service_account import Credentials
import os
from colorama import Fore, Back, Style

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
    },
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

    # Validates function based on Love Sandwiches walkthrough project
    while True:
        choice = input(
            "Please chosse an option by typing a number from the menu above: \n"
        )

        if validate_choice(choice, 1, 7):
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
        amount, category = get_amount("expense")
        if amount != None and category != None:
            print(
                "Adding "
                + Fore.GREEN
                + f"${amount}"
                + Style.RESET_ALL
                + f" spent on {category} to the worksheet...\n"
            )
            update_worksheet([float(amount), category], "expenses")
    elif int(choice) == 5:
        amount, category = get_amount("income")
        if amount != None and category != None:
            print(
                f"Adding "
                + Fore.GREEN
                + f"${amount}"
                + Style.RESET_ALL
                + f" earned from {category} to the worksheet...\n"
            )
            update_worksheet([float(amount), category], "incomes")
    elif int(choice) == 6:
        display_exit_message()


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
    if balance < 0:
        color = Fore.RED + "-$"
    else:
        color = Fore.GREEN + "$"
    print("Your current balance is: " + color + f"{abs(balance):.2f}\n")
    print(Style.RESET_ALL)


def calculate_amounts_by_category(type):
    """
    Calculate the total amount spent for each expense category or the total amount of income
    for each income category.
    """
    print(f"Calculating your {type} summary...")
    amounts = SHEET.worksheet(type).col_values(1)
    worksheet_categories = SHEET.worksheet(type).col_values(2)
    amounts_by_category = {
        key: 0 for key in category_dictionary[f"{type}_categories"].values()
    }
    for value in category_dictionary[f"{type}_categories"].values():
        for amount, category in zip(amounts, worksheet_categories):
            if value == category:
                amounts_by_category[value] += float(amount)
    return amounts_by_category


def display_amounts_by_category(amounts_dict, type):
    """ "
    Displays the total expenses by each category to the terminal
    """
    print(f"The total amount of {type} by each category is:\n")
    for key in amounts_dict:
        print(f"{key}: " + Fore.GREEN + f"${amounts_dict[key]:.2f}" + Style.RESET_ALL)
    print("\n")


def get_amount(type):
    """ "
    Requests an amount from the user to be added as an income or expense with its
    respective category to the spreadsheet. Return the amount and category as a tuple.
    Type can be income or expense
    """
    categories = category_dictionary[f"{type}s_categories"]
    print(f"Adding a new {type}...\n")

    # asks for the amount and category. loops until the user confirm choice or exit
    while True:
        while True:
            amount = input("Please enter the amount you would like to add:\n")
            if validate_amount(amount):
                break

        while True:
            print(f"Please choose one of the following categories for this {type}\n")
            for item in categories:
                print(f"{item}: {categories[item]}")
            print("\n")
            category_index = input(
                f"Please enter the number corresponding to your category:\n"
            )
            categories_size = len(categories) + 1
            if validate_choice(category_index, 1, categories_size):
                break

        category = category_dictionary[f"{type}s_categories"][category_index]

        print(
            f"Adding {category}: "
            + Fore.GREEN
            + f"${amount}"
            + Style.RESET_ALL
            + " to the worksheet..."
        )
        confirm = confirm_choice()
        if confirm == "Y":
            break
        elif confirm == "N":
            print("Deleting entry... Try again.\n")
            pass
        elif confirm == "EXIT":
            amount = None
            category = None
            print("Cancelling operation...\n")
            break

    return (amount, category)


# Update worksheet function based on Love Sandwiches walkthrough project
def update_worksheet(amount_category, worksheet):
    """
    Insert a list containing an amount and a category to the corresponding worksheet.

    """
    SHEET.worksheet(worksheet).append_row(amount_category)
    print(
        f"Worksheet updated successfully. {amount_category[1]}: "
        + Fore.GREEN
        + f"${amount_category[0]}"
        + Style.RESET_ALL
        + f" Added to {worksheet}"
    )


def confirm_choice():
    while True:
        confirm = input("Please choose Y/N, or if you like to cancel type EXIT:\n")
        if confirm.upper() == "Y":
            return "Y"
        elif confirm.upper() == "N":
            return "N"
        elif confirm.upper() == "EXIT":
            return "EXIT"
        else:
            print(Fore.RED + "Invalid choice. Please try again")
            print(Style.RESET_ALL)
            continue


# Validation function based on Love Sandwiches walkthrough project
def validate_choice(choice, lower_limit, upper_limit):
    """
    Tries to convert choice into an integer and checks if it is in the range
    of possible choices. Informs the user if cannot convert into an integer or
    if it is outside of range.
    """
    try:
        int(choice)
    except:
        print(Fore.RED + "Not a number. Please try again.")
        print(Style.RESET_ALL)
        return False
    try:
        if int(choice) not in range(lower_limit, upper_limit):
            raise ValueError("Option not found")
    except ValueError as e:
        print(Fore.RED + f"{e}. Try again.")
        print(Style.RESET_ALL)
        return False
    return True


def validate_amount(amount):
    if len(amount.split(".")) == 2 and len(amount.split(".")[-1]) == 2:
        return True
    else:
        print(
            Fore.RED
            + "Please enter an amount with two decimal places separated by a dot (i.e. 100.00)\n"
        )
        print(Style.RESET_ALL)
        return False


def display_exit_message():
    print(Fore.BLUE + Back.WHITE + "Thank you for using Personal Finance!")
    print("Exiting program...Goodbye!" + Style.RESET_ALL + "\n")


def main():
    """
    Calls functin for displaying the menu to the terminal, then calls function to evaluate the user choice.
    """
    # Clear terminal, code taken from Stack Overflow
    os.system("cls" if os.name == "nt" else "clear")
    print(
        Fore.BLUE
        + Back.WHITE
        + "Welcome to your personal finance.\n"
        + Style.RESET_ALL
        + "\n"
    )
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
            display_exit_message()
            break
        else:
            print(Fore.RED + "Invalid answer, please type Y or N.\n")
            print(Style.RESET_ALL)


main()
