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
    print("Welcome to your personal finance.\n")
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
    
    if int(choice) == 1:
        print("choice: check balance.")
    elif int(choice) == 2:
        print("choice: check expenses summary.")
    elif int(choice) == 3:
        print("choice: check income summary.")
    elif int(choice) == 4:
        print("choice: add new expense.")
    elif int(choice) == 5:
        print("choice: add ne income.")


main()