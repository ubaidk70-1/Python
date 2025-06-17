from collections import defaultdict
from datetime import datetime, date as dt
import json
import sys
import shutil
import os

# Global list to store all expenses
expenses = []

# ANSI color codes for terminal output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Helper function to sanitize text
def clean_text(text):
    return text.replace("\n", " ").replace("\t", " ").replace('\r', ' ').strip()

# Function to add a new expense
def add_expense():
    print("\n--- Add a New Expense ---")

    while True:
        amount_input = input("Enter amount (e.g., 250.75): ").strip()
        try:
            amount = float(amount_input)
            if amount <= 0:
                print("Amount must be greater than 0. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric amount.")

    while True:
        category = input("Enter category (e.g., Food, Travel): ").strip().title()
        if category == "":
            print("Category cannot be empty. Please enter a valid category.")
        else:
            break

    while True:
        date_input = input("Enter date (YYYY-MM-DD), or leave blank for today: ").strip()
        if date_input == "":
            date_str = str(dt.today())
            break
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date_str = date_input
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    note = clean_text(input("Enter a note (optional): "))

    expense = {
        "amount": amount,
        "category": category,
        "date": date_str,
        "note": note
    }

    expenses.append(expense)
    print("[✓] Expense added successfully.\n")
    save_expenses_to_file()

# Function to view all recorded expenses
def view_expenses():
    print("\n---- All Recorded Expenses ----")

    if not expenses:
        print("[!] No expenses recorded yet.")
        return

    print(f"{'Index':<6} | {'Amount':<10} | {'Category':<15} | {'Date':<12} | Note")
    print("-" * 65)

    for i, expense in enumerate(expenses):
        amount_val = expense['amount']
        amount = f"{amount_val:.2f}"
        category = expense['category']
        date = expense['date']
        note = clean_text(expense['note'])

        color = RED if amount_val > 1000 else GREEN
        print(f"{i:<6} | ₹{amount:<9} | {category:<15} | {date:<12} | {note}")

    print("-" * 65)
    total_spent = sum(exp['amount'] for exp in expenses)
    print(f"[#] Total Expenses Recorded: {len(expenses)}")
    print(f"[#] Total Amount Spent: ₹{total_spent:.2f}\n")

# Function to edit or delete an existing expense
def edit_or_delete_expense():
    print("\n--- Edit or Delete an Expense ---")

    if not expenses:
        print("[!] No expenses to edit or delete.")
        return

    view_expenses()

    try:
        index = int(input("Enter the index of the expense to modify: ").strip())
        if index < 0 or index >= len(expenses):
            print("[X] Invalid index. Please try again.")
            return
    except ValueError:
        print("[X] Please enter a valid number.")
        return

    selected = expenses[index]
    action = input("Do you want to (E)dit or (D)elete this expense? (E/D): ").strip().upper()

    if action == "E":
        print("\n--- Editing Fields (press Enter to keep current) ---")

        while True:
            new_amount = input(f"Current amount = ₹{selected['amount']}. New amount: ").strip()
            if new_amount == "":
                break
            try:
                new_amount = float(new_amount)
                if new_amount <= 0:
                    print("Amount must be greater than 0.")
                else:
                    selected['amount'] = new_amount
                    break
            except ValueError:
                print("Invalid input. Enter a number.")

        new_cat = input(f"Current category = {selected['category']}. New category: ").strip().title()
        if new_cat != "":
            selected['category'] = new_cat

        while True:
            new_date = input(f"Current date = {selected['date']}. New date (YYYY-MM-DD): ").strip()
            if new_date == "":
                break
            try:
                datetime.strptime(new_date, "%Y-%m-%d")
                selected['date'] = new_date
                break
            except ValueError:
                print("Invalid date format.")

        new_note = input(f"Current note = {selected['note']}. New note: ").strip()
        if new_note != "":
            selected['note'] = new_note

        print("[✔] Expense updated successfully.")
        save_expenses_to_file()

    elif action == "D":
        confirm = input("Are you sure you want to delete this expense? (y/n): ").strip().lower()
        if confirm == "y":
            deleted = expenses.pop(index)
            print(f"[#] Expense '{deleted['category']}' on {deleted['date']} deleted.")
            save_expenses_to_file()
        else:
            print("[~] Deletion canceled.")
    else:
        print("[X] Invalid choice. Please select E or D.")


# Function to search or filter expenses based on various criteria 
def search_or_filter_expenses():
    print("\n--- Search or Filter Expenses ---")

    if not expenses:
        print("[!] No expenses to filter.")
        return

    print("Select filters to apply (leave blank to skip):")

    # Get filter inputs
    category_filter = input("Category (e.g., Food): ").strip().lower()
    date_filter = input("Specific Date (YYYY-MM-DD): ").strip()
    month_filter = input("Month (MM): ").strip()
    year_filter = input("Year (YYYY): ").strip()
    min_amount_input = input("Min Amount (e.g., 100): ").strip()
    max_amount_input = input("Max Amount (e.g., 1000): ").strip()
    keyword_filter = input("Keyword in Note: ").strip().lower()

    # Check if ALL filters are blank
    if not (category_filter or date_filter or month_filter or year_filter or min_amount_input or max_amount_input or keyword_filter):
        print("[!] No filters selected. Please enter at least one filter.")
        return

    # Validate & convert amount range
    try:
        min_amount = float(min_amount_input) if min_amount_input else None
    except ValueError:
        print("[X] Invalid Min Amount.")
        return

    try:
        max_amount = float(max_amount_input) if max_amount_input else None
    except ValueError:
        print("[X] Invalid Max Amount.")
        return

    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        print("[X] Min amount cannot be greater than max amount.")
        return

    from datetime import datetime
    if date_filter:
        try:
            datetime.strptime(date_filter, "%Y-%m-%d")
        except ValueError:
            print("[X] Invalid date format. Use YYYY-MM-DD.")
            return

    if month_filter and (not month_filter.isdigit() or not (1 <= int(month_filter) <= 12)):
        print("[X] Invalid month. Use format MM (e.g., 01, 02...12).")
        return

    if year_filter and (not year_filter.isdigit() or not (1900 <= int(year_filter) <= 2100)):
        print("[X] Invalid year. Use format YYYY (e.g., 2024).")
        return

    filtered = []
    for expense in expenses:
        match = True

        if category_filter and category_filter != expense["category"].strip().lower():
            match = False

        if date_filter and date_filter != expense["date"].strip():
            match = False

        try:
            expense_date_obj = datetime.strptime(expense["date"], "%Y-%m-%d")
        except ValueError:
            continue

        if month_filter and int(month_filter) != expense_date_obj.month:
            match = False
        if year_filter and int(year_filter) != expense_date_obj.year:
            match = False

        if min_amount is not None and expense["amount"] < min_amount:
            match = False
        if max_amount is not None and expense["amount"] > max_amount:
            match = False

        if keyword_filter:
            note = expense["note"].strip().lower()
            if keyword_filter not in note:
                match = False

        if match:
            filtered.append(expense)

    if not filtered:
        print("[!] No matching expenses found for given filters.")
        return

    print("\n[+] Matching Expenses:\n")
    print(f"{'Index':<6} | {'Amount':<10} | {'Category':<15} | {'Date':<12} | Note")
    print("-" * 65)
    for i, expense in enumerate(filtered):
        amount = f"{expense['amount']:.2f}"
        category = expense['category']
        date = expense['date']
        note = expense['note']
        print(f"{i:<6} | ₹{amount:<9} | {category:<15} | {date:<12} | {note}")
    print("-" * 65)
    total_amount = sum(e["amount"] for e in filtered)
    print(f"[#] Total Matches: {len(filtered)} | Total Amount: ₹{total_amount:.2f}\n")


# Function to view a summary of expenses
def view_summary():
    print("\n==== Expense Summary ====\n")

    if not expenses:
        print("[!] No expenses recorded yet.")
        return

    total_amount = sum(exp["amount"] for exp in expenses)
    total_count = len(expenses)
    average = total_amount / total_count

    print(f"[Total Spent] ₹{total_amount:.2f}")
    print(f"[Total Entries] {total_count}")
    print(f"[Average per Entry] ₹{average:.2f}")

    # Min and Max expense
    min_expense = min(expenses, key=lambda x: x["amount"])
    max_expense = max(expenses, key=lambda x: x["amount"])

    print(f"[Lowest Expense] ₹{min_expense['amount']:.2f} on {min_expense['date']} ({min_expense['note']})")
    print(f"[Highest Expense] ₹{max_expense['amount']:.2f} on {max_expense['date']} ({max_expense['note']})\n")

    # Category-wise breakdown
    category_summary = defaultdict(float)
    for exp in expenses:
        category_summary[exp["category"]] += exp["amount"]

    print("[Category-wise Summary]")
    sorted_cat = sorted(category_summary.items(), key=lambda x: x[1], reverse=True)
    for cat, amt in sorted_cat:
        percent = (amt / total_amount) * 100
        bar = "|" * int(percent // 2)  # 2% per bar block
        print(f"- {cat:<12}: ₹{amt:>8.2f} ({percent:>5.1f}%) {bar}")

    # Top category
    top_category = max(category_summary.items(), key=lambda x: x[1])
    print(f"\n[Top Spending Category] {top_category[0]} (₹{top_category[1]:.2f})")

    # Monthly summary
    monthly_summary = defaultdict(float)
    for exp in expenses:
        try:
            dt_obj = datetime.strptime(exp["date"], "%Y-%m-%d")
            key = f"{dt_obj.year}-{dt_obj.month:02d}"
            monthly_summary[key] += exp["amount"]
        except ValueError:
            continue  # skip invalid dates

    print("\n[Monthly Summary]")
    for month, amt in sorted(monthly_summary.items()):
        print(f"- {month}: ₹{amt:.2f}")

    # Most expensive entry
    print(f"\n[Most Expensive Entry]\n  ₹{max_expense['amount']:.2f} | \"{max_expense['note']}\" | {max_expense['date']} | {max_expense['category']}")

    print("\n===========================\n")




# Define file paths
DATA_DIR = "data"
EXPENSE_FILE = os.path.join(DATA_DIR, "expenses.json")
BACKUP_FILE = os.path.join(DATA_DIR, "expenses_backup.json")

# Load expenses from file when app starts
def load_expenses_from_file(filename=EXPENSE_FILE):
    global expenses
    try:
        with open(filename, "r") as f:
            expenses = json.load(f)
        print(f"[INFO] Loaded {len(expenses)} expenses from '{filename}'.")
    except FileNotFoundError:
        expenses = []
        print("[INFO] No existing expense file found. Starting with an empty list.")

# Save current expenses to file
def save_expenses_to_file(filename=EXPENSE_FILE):
    try:
        # Ensure the data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)

        # Save main file
        with open(filename, "w") as f:
            json.dump(expenses, f, indent=4)

        # Create a backup
        shutil.copy(filename, BACKUP_FILE)

        # Timestamp log
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[SAVED] {len(expenses)} expenses saved to '{filename}' at {timestamp}.")
        print(f"[BACKUP] Copy created at '{BACKUP_FILE}'.")
    except Exception as e:
        print(f"[ERROR] Failed to save or backup expenses: {e}")

# Exit app safely
def exit_app():
    confirm = input("[!] Are you sure you want to exit? (y/n): ").strip().lower()
    if confirm == 'y':
        save_expenses_to_file()
        print("[INFO] Goodbye! Your data has been saved. Exiting now...")
        sys.exit(0)
    else:
        print("[INFO] Exit cancelled. Returning to main menu.")



 


def main_menu():
    while True:
        print("\n==== [ Personal Expense Tracker ]====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Edit or Delete Expense")
        print("4. Search or Filter Expenses")
        print("5. View Summary")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            edit_or_delete_expense()
        elif choice == '4':
            search_or_filter_expenses()
        elif choice == '5':
            view_summary()
        elif choice == '6':
            exit_app()
        else:
            print("[ERROR] Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    load_expenses_from_file()  # Load existing expenses at startup
    main_menu()  # Start the main menu loop




