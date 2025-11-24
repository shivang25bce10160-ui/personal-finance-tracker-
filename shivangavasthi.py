import os  # Import os module to check if the data file exists

# Global variables to store data
transactions = []  # List of dictionaries: each dict represents a transaction with keys 'type', 'amount', 'description', 'category'
balance = 0.0  # Float to keep track of the current balance (income - expenses)
data_file = 'budget_data.txt'  # Name of the file to save/load data

def load_data():
    """
    Load transactions from the file if it exists.
    This function reads the saved data and reconstructs the transactions list and balance.
    """
    global transactions, balance  # Access global variables
    if os.path.exists(data_file):  # Check if the file exists
        with open(data_file, 'r') as f:  # Open file in read mode
            for line in f:  # Loop through each line in the file
                parts = line.strip().split('|')  # Split line by '|' delimiter (e.g., "income|100.0|Salary|Work")
                if len(parts) == 4:  # Ensure the line has exactly 4 parts
                    trans_type, amount, desc, cat = parts  # Unpack into variables
                    amount = float(amount)  # Convert amount to float
                    transactions.append({'type': trans_type, 'amount': amount, 'description': desc, 'category': cat})  # Add to list
                    if trans_type == 'income':  # Update balance based on type
                        balance += amount
                    else:
                        balance -= amount

def save_data():
    """
    Save all transactions to the file.
    This ensures data persists between program runs.
    """
    with open(data_file, 'w') as f:  # Open file in write mode (overwrites existing file)
        for trans in transactions:  # Loop through each transaction
            # Write in the format: type|amount|description|category
            f.write(f"{trans['type']}|{trans['amount']}|{trans['description']}|{trans['category']}\n")

def add_transaction():
    """
    Prompt the user to add a new income or expense transaction.
    Validates input and updates the global transactions list and balance.
    """
    trans_type = input("Enter 'income' or 'expense': ").strip().lower()  # Get and clean user input
    if trans_type not in ['income', 'expense']:  # Validate type
        print("Invalid type. Try again.")
        return  # Exit function if invalid
    try:
        amount = float(input("Enter amount: "))  # Get amount and convert to float
    except ValueError:  # Handle invalid number input
        print("Invalid amount. Try again.")
        return
    description = input("Enter description: ").strip()  # Get description
    category = input("Enter category (e.g., Food, Transport): ").strip()  # Get category
    transactions.append({'type': trans_type, 'amount': amount, 'description': description, 'category': category})  # Add to list
    global balance  # Access global balance
    if trans_type == 'income':  # Update balance
        balance += amount
    else:
        balance -= amount
    print("Transaction added successfully!")  # Confirm addition

def view_transactions():
    """
    Display all transactions in a numbered list, along with the current balance.
    If no transactions exist, inform the user.
    """
    if not transactions:  # Check if list is empty
        print("No transactions yet.")
        return
    print("\nAll Transactions:")  # Header
    for i, trans in enumerate(transactions, 1):  # Loop with index starting at 1
        # Print formatted transaction details
        print(f"{i}. {trans['type'].capitalize()}: ₹{trans['amount']:.2f} - {trans['description']} (Category: {trans['category']})")
    print(f"\nCurrent Balance: ₹{balance:.2f}")  # Show balance

def generate_report():
    """
    Generate and display a summary of expenses grouped by category.
    Calculates totals for each category and overall expenses.
    """
    if not transactions:  # Check if list is empty
        print("No transactions to report.")
        return
    categories = {}  # Dictionary to store category totals
    for trans in transactions:  # Loop through transactions
        if trans['type'] == 'expense':  # Only consider expenses
            cat = trans['category']  # Get category
            categories[cat] = categories.get(cat, 0) + trans['amount']  # Add to total (default to 0 if new)
    print("\nExpense Report by Category:")  # Header
    for cat, total in categories.items():  # Loop through category totals
        print(f"{cat}: ₹{total:.2f}")  # Print each category's total
    print(f"Total Expenses: ₹{sum(categories.values()):.2f}")  # Print overall expense total

def main():
    """
    Main function that runs the menu-driven interface.
    Loads data on start, handles user choices in a loop, and saves on exit.
    """
    load_data()  # Load existing data at startup
    while True:  # Infinite loop for menu
        print("\n--- Personal Budget Tracker ---")  # Menu header
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Generate Expense Report")
        print("4. Save and Exit")
        choice = input("Choose an option (1-4): ").strip()  # Get user choice
        if choice == '1':
            add_transaction()  # Call add function
        elif choice == '2':
            view_transactions()  # Call view function
        elif choice == '3':
            generate_report()  # Call report function
        elif choice == '4':
            save_data()  # Save data
            print("Data saved. Goodbye!")  # Exit message
            break  # Exit loop
        else:
            print("Invalid choice. Try again.")  # Handle invalid input

if __name__ == "__main__":
    main()  # Run the main function when script is executed directly
