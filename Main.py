import json

# Global list that created store transactions
transactions = {}


# File handling functions
def load_transactions():
    """Load the JASON file to the code"""
    global transactions
    try:
        with open("transactions.json", "r") as f:
            transactions = json.load(f)
    except FileNotFoundError:
        print("No transactions file found!. Creating a new one.")
        # transactions = {}


def save_transactions():
    """Save the JASON file after changes."""
    with open('transactions.json', 'w') as f:
        json.dump(transactions, f, indent=2)
    print('\nSaved to transactions successfully')


def add_transaction():
    """Add values/data to the JASON file."""
    try:
        expense_type = input('Enter the type of expense: ').capitalize()
        amount = float(input('Enter the amount : '))
        date = input('Enter the date (YYYY-MM-DD) : ')

        transaction = {"amount": amount, "date": date}

        if expense_type in transactions:
            transactions[expense_type].append(transaction)
        else:
            transactions[expense_type] = [transaction]
        save_transactions()
    except ValueError:
        print('Invalid Input‼ Please try again.')


def display_summary():
    """ Display the Summary of transactions. """
    total_expenses = {expense_type: sum(transaction["amount"] for transaction in transactions_list) for
                      expense_type, transactions_list in transactions.items()}
    # print("Expense Type\tTotal Amount")
    for expense_type, total_amount in total_expenses.items():
        print(expense_type, "\t", total_amount)


def read_bulk_transactions_from_file(filename):
    """ Read transaction data from a text file and add to the transactions json file """
    try:
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                fields = line.strip().split(',')   # Split the line into fields
                # print(fields)
                if len(fields) != 3:
                    # print(f"Error: Line {line_number} does not contain three fields. Skipping.")
                    continue

                expense_type = (fields[0]).capitalize()
                amount = (float(fields[1]))
                date = (fields[2])
                # print(amount)

                transaction_data = {"amount": amount, "date": date}
                # Add transaction to the dictionary
                if expense_type not in transactions:
                    transactions[expense_type] = []
                transactions[expense_type].append(transaction_data)

        print("Transactions loaded successfully.")

        # Save the updated transactions dictionary to the JSON file
        save_transactions()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred while reading transactions from '{filename}': {e}")


def view_transactions():
    """View the transaction details"""
    # Check if there are any transactions
    if not transactions:
        print("No transactions found.")
    else:
        for expense_type, transaction_list in transactions.items():
            print(f"{expense_type}:")
            for transaction in transaction_list:
                print(f"  Amount: {transaction['amount']}, Date: {transaction['date']}")


def update_transaction():
    """View the transactions"""
    # Check if there are any transactions
    if not transactions:
        print("No transactions found.")
        return

    print("Current transactions:")
    view_transactions()
    expense_type = input("\nEnter expense type to update: ").capitalize()
    if expense_type in transactions:
        index = int(input("Enter the index of the transaction to update (\033[1mstarting from 1\033[0m): "))
        while index == 0:
            print('Invalid index input ‼')
            print('Please enter a correct index greater than zero.')
            index = int(input("Enter the index of the transaction to delete(\033[1mstarting from 1\033[0m): "))
        index_p = index - 1  # Subtract 1 from user entered index to get the indexing number
        # print(index_p)
        if 0 <= index_p < len(transactions[expense_type]):
            # Prompt user to enter the details for update
            amount = float(input("Enter updated transaction amount: "))
            transaction_date = input("Enter updated date (YYYY-MM-DD): ")

            # Update the transaction
            transactions[expense_type][index_p] = {"amount": amount, "date": transaction_date}
            save_transactions()
            print("Transaction updated successfully.")
        else:
            print("Invalid transaction index.")
    else:
        print("Expense type not found.")


def delete_transaction():
    if not transactions:
        print("No transactions found.")
        return

    print("Current transactions:")
    view_transactions()
    expense_type = input("\nEnter expense type to delete from: ").capitalize()
    if expense_type in transactions:
        index = int(input("Enter the index of the transaction to delete(\033[1mstarting from 1\033[0m): "))
        while index == 0:
            print('Invalid index input ‼')
            print('Please enter a correct index greater than zero.')
            index = int(input("Enter the index of the transaction to delete(\033[1mstarting from 1\033[0m): "))
        index_p = index - 1  # Subtract 1 from user entered index to get the indexing number
        if 0 <= index_p < len(transactions[expense_type]):
            del transactions[expense_type][index_p]
            print("Transaction deleted successfully.")
            save_transactions()
        else:
            print("Invalid transaction index.")
    else:
        print("Expense type not found.")


def open_gui():
    try:
        import GUI
        GUI.main()
        print('\nGUI closed.')
    except:
        print('\nError occurred‼')

def main_menu():
    """Main menu that shows at the first"""
    load_transactions()  # Load transactions at the start
    # Get the inputs from user
    while True:
        print(('\n'), ("\033[1mPersonal Finance Tracker\033[0m").center(44, '-'))
        print("\n1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Read Bulk Transactions from a text File")
        print("7. Save Transactions")
        print("8. Open Graphical user interface")
        print("9. Exit")

        choice = input("Enter your choice (1...9): ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            update_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            display_summary()
        elif choice == "6":
            filename = input("Enter filename to read transactions from: ")
            read_bulk_transactions_from_file(filename)
        elif choice == "7":
            save_transactions()
            print("Transactions saved.")
        elif choice == "8":
            open_gui()
        elif choice == "9":
            print('Exiting the program.')
            break
        else:
            print("Invalid choice. Please try again.")


# Start
if __name__ == "__main__":
    main_menu()
