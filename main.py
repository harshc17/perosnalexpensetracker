import os
import pickle
import csv
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta

# Constants
MAX_EXPENSES = 100
MAX_DESC = 50
MAX_CATEGORIES = 11
MAX_FILENAME = 100
MAX_MEMORY = 500
MEMORY_FILE = "expense_memory.dat"
CURRENT_FILE = "current_expenses.dat"
BALANCE_FILE = "balance_history.dat"
CATEGORY_FILE = "categories.dat"
MAX_PAYMENT_METHODS = 3
MAX_BALANCE_HISTORY = 100

WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

@dataclass
class Expense:
    amount: float
    description: str
    category: int
    payment_method: int
    date: float  # timestamp

@dataclass
class BalanceEntry:
    amount: float
    date: float  # timestamp

@dataclass
class ExpenseTracker:
    expenses: List[Expense] = field(default_factory=list)
    memory: List[Expense] = field(default_factory=list)
    category_names: List[str] = field(default_factory=list)
    payment_method_names: List[str] = field(default_factory=lambda: ["Cash", "UPI", "Card"])
    bank_balance: float = 0.0
    cash_balance: float = 0.0
    bank_history: List[BalanceEntry] = field(default_factory=list)
    cash_history: List[BalanceEntry] = field(default_factory=list)

    def save_expenses(self):
        with open(CURRENT_FILE, 'wb') as f:
            pickle.dump(self.expenses, f)
        with open(MEMORY_FILE, 'wb') as f:
            pickle.dump(self.memory, f)

    def load_expenses(self):
        if os.path.exists(CURRENT_FILE):
            with open(CURRENT_FILE, 'rb') as f:
                self.expenses = pickle.load(f)
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'rb') as f:
                self.memory = pickle.load(f)

    def save_balance(self):
        with open(BALANCE_FILE, 'wb') as f:
            pickle.dump({
                'bank_balance': self.bank_balance,
                'cash_balance': self.cash_balance,
                'bank_history': self.bank_history,
                'cash_history': self.cash_history
            }, f)

    def load_balance(self):
        if os.path.exists(BALANCE_FILE):
            with open(BALANCE_FILE, 'rb') as f:
                data = pickle.load(f)
                self.bank_balance = data.get('bank_balance', 0.0)
                self.cash_balance = data.get('cash_balance', 0.0)
                self.bank_history = data.get('bank_history', [])
                self.cash_history = data.get('cash_history', [])

    def save_categories(self):
        with open(CATEGORY_FILE, 'w', encoding='utf-8') as f:
            for cat in self.category_names:
                f.write(cat + '\n')

    def load_categories(self):
        if os.path.exists(CATEGORY_FILE):
            with open(CATEGORY_FILE, 'r', encoding='utf-8') as f:
                self.category_names = [line.strip() for line in f if line.strip()]
        if not self.category_names:
            self.category_names = [
                "Food & Groceries", "Transport", "Utilities", "Entertainment", "Shopping",
                "Housing", "Investment", "Healthcare", "Education", "Banking", "Miscellaneous"
            ]
            self.save_categories()

    def init_tracker(self):
        self.load_categories()
        self.load_expenses()
        self.load_balance()

    def is_duplicate(self, e1: Expense, e2: Expense) -> bool:
        return (
            e1.amount == e2.amount and
            e1.description == e2.description and
            e1.category == e2.category and
            e1.payment_method == e2.payment_method and
            e1.date == e2.date
        )

    def add_category(self, name: str):
        if len(self.category_names) >= MAX_CATEGORIES:
            print("Maximum categories reached!")
            return
        if name.lower() in (c.lower() for c in self.category_names):
            print(f"Category '{name}' already exists.")
            return
        self.category_names.append(name)
        self.save_categories()
        print(f"Category '{name}' added successfully.")

    def add_expense(self, amount, desc, category, payment_method, date):
        if len(self.expenses) >= MAX_EXPENSES or amount <= 0 or not desc or \
           category < 0 or category >= len(self.category_names) or \
           payment_method < 0 or payment_method >= len(self.payment_method_names):
            print("Error: Invalid expense data.")
            return
        expense = Expense(amount, desc, category, payment_method, date)
        self.expenses.append(expense)
        # Add to memory (front)
        self.memory.insert(0, expense)
        if len(self.memory) > MAX_MEMORY:
            self.memory = self.memory[:MAX_MEMORY]
        self.save_expenses()

    def remove_expense(self, expense: Expense):
        removed = False
        # Remove from both lists
        for lst, fname in [(self.expenses, CURRENT_FILE), (self.memory, MEMORY_FILE)]:
            idx_to_remove = None
            for i, e in enumerate(lst):
                if self.is_duplicate(e, expense):
                    idx_to_remove = i
                    break
            if idx_to_remove is not None:
                lst.pop(idx_to_remove)
                removed = True
            with open(fname, 'wb') as f:
                pickle.dump(lst, f)
        if removed:
            print("Entry deleted successfully from relevant lists.")
        else:
            print("Entry not found in any list for deletion.")

    def edit_expense(self, idx, is_memory):
        lst = self.memory if is_memory else self.expenses
        if idx < 0 or idx >= len(lst):
            print("Invalid index.")
            return
        exp = lst[idx]
        old_exp = Expense(**vars(exp))
        print(f"Editing Expense: {exp.description} (Amount: {exp.amount})")
        try:
            val = input(f"Current amount: {exp.amount}\nNew amount (Enter to keep): ")
            if val.strip():
                amt = float(val)
                if amt > 0:
                    exp.amount = amt
            val = input(f"Current description: {exp.description}\nNew description (Enter to keep): ")
            if val.strip():
                exp.description = val.strip()[:MAX_DESC]
            print("Categories:")
            for i, cat in enumerate(self.category_names):
                print(f"{i}: {cat}")
            val = input(f"Current category: {self.category_names[exp.category]}\nNew category (Enter to keep): ")
            if val.strip():
                cat = int(val)
                if 0 <= cat < len(self.category_names):
                    exp.category = cat
            print("Payment Methods:")
            for i, pm in enumerate(self.payment_method_names):
                print(f"{i}: {pm}")
            val = input(f"Current payment method: {self.payment_method_names[exp.payment_method]}\nNew payment method (Enter to keep): ")
            if val.strip():
                pm = int(val)
                if 0 <= pm < len(self.payment_method_names):
                    exp.payment_method = pm
            dt = datetime.fromtimestamp(exp.date)
            val = input(f"Current date: {dt.strftime('%d-%m-%Y')}\nChange date? (y/n): ")
            if val.strip().lower() == 'y':
                val = input("Enter new date (DD MM YYYY): ")
                try:
                    d, m, y = map(int, val.strip().split())
                    exp.date = datetime(y, m, d, 12).timestamp()
                except:
                    print("Invalid date. Keeping current.")
        except Exception as e:
            print("Edit cancelled due to error.", e)
            return
        # Update the corresponding entry in the other list
        other_lst = self.expenses if is_memory else self.memory
        for i, e in enumerate(other_lst):
            if self.is_duplicate(e, old_exp):
                # Update the entry to match the edited expense
                other_lst[i] = Expense(**vars(exp))
                break
        self.save_expenses()
        print("Expense updated and synchronized successfully.")

    def list_expenses(self):
        print("\n--- Listed Expenses ---")
        all_exp = self.expenses + [e for e in self.memory if not any(self.is_duplicate(e, c) for c in self.expenses)]
        all_exp = sorted(all_exp, key=lambda e: -e.date)
        if not all_exp:
            print("No expenses to display.")
            return
        print(f"{'No.':<5} {'Amount':<10} {'Description':<25} {'Category':<15} {'Payment':<15} {'Date':<10}")
        print("-"*80)
        for i, e in enumerate(all_exp[:20]):
            dt = datetime.fromtimestamp(e.date)
            print(f"{i+1:<5} {e.amount:<10.2f} {e.description[:25]:<25} {self.category_names[e.category]:<15} {self.payment_method_names[e.payment_method]:<15} {dt.strftime('%d-%m-%Y'):<10}")
        print("-"*80)

    def category_summary(self):
        now = datetime.now()
        month, year = now.month, now.year
        all_exp = self.expenses + [e for e in self.memory if not any(self.is_duplicate(e, c) for c in self.expenses)]
        month_exp = [e for e in all_exp if datetime.fromtimestamp(e.date).month == month and datetime.fromtimestamp(e.date).year == year]
        if not month_exp:
            print("No expenses found for the current month.")
            return
        cat_totals = [0.0]*len(self.category_names)
        for e in month_exp:
            cat_totals[e.category] += e.amount
        total = sum(cat_totals)
        print(f"{'Category':<20} {'Total':<15} {'%':<10}")
        print("-"*45)
        for i, amt in enumerate(cat_totals):
            if amt > 0:
                print(f"{self.category_names[i]:<20} {amt:<15.2f} {amt/total*100:<9.2f}%")
        print("-"*45)
        print(f"{'TOTAL MONTHLY':<20} {total:<15.2f} {100.00:<9.2f}%")

    def find_highest_expense(self):
        now = datetime.now()
        month, year = now.month, now.year
        all_exp = self.expenses + [e for e in self.memory if not any(self.is_duplicate(e, c) for c in self.expenses)]
        month_exp = [e for e in all_exp if datetime.fromtimestamp(e.date).month == month and datetime.fromtimestamp(e.date).year == year]
        if not month_exp:
            print("No expenses found for this month.")
            return
        highest = max(month_exp, key=lambda e: e.amount)
        dt = datetime.fromtimestamp(highest.date)
        print(f"Amount: {highest.amount}\nDescription: {highest.description}\nCategory: {self.category_names[highest.category]}\nPayment Method: {self.payment_method_names[highest.payment_method]}\nDate: {dt.strftime('%d-%m-%Y')}")

    def budget_alert(self, budget):
        now = datetime.now()
        month, year = now.month, now.year
        all_exp = self.expenses + [e for e in self.memory if not any(self.is_duplicate(e, c) for c in self.expenses)]
        month_exp = [e for e in all_exp if datetime.fromtimestamp(e.date).month == month and datetime.fromtimestamp(e.date).year == year]
        total = sum(e.amount for e in month_exp)
        print(f"\n--- Monthly Budget Analysis ---\nMonth: {MONTH_NAMES[month-1]} {year}\nBudget: {budget:.2f}\nExpenses: {total:.2f}\nRemaining: {budget-total:.2f}\nPercentage Used: {total/budget*100 if budget else 0:.2f}%")
        if total > budget:
            print(f"\nALERT: You have exceeded your monthly budget by {total-budget:.2f}!")
        elif total > budget*0.8:
            print(f"\nWARNING: You have used {total/budget*100:.2f}% of your budget. Be careful with your spending.")
        else:
            print(f"\nYou still have {(budget-total)/budget*100 if budget else 0:.2f}% of your budget remaining.")

    def view_monthly_total_expenses(self):
        try:
            val = input("Enter month (1-12) and year (YYYY): ")
            month, year = map(int, val.strip().split())
            if not (1 <= month <= 12 and 1900 <= year <= 2200):
                print("Invalid month or year.")
                return
        except:
            print("Invalid input format.")
            return
        all_exp = self.expenses + [e for e in self.memory if not any(self.is_duplicate(e, c) for c in self.expenses)]
        month_exp = [e for e in all_exp if datetime.fromtimestamp(e.date).month == month and datetime.fromtimestamp(e.date).year == year]
        total = sum(e.amount for e in month_exp)
        if month_exp:
            print(f"Total expenses for {MONTH_NAMES[month-1]} {year}: {total:.2f}")
        else:
            print(f"No expenses found for {MONTH_NAMES[month-1]} {year}.")

    def export_to_excel(self, year, month):
        # Use default downloads folder
        downloads_path = os.path.expanduser("~/Downloads")
        export_dir = os.path.join(downloads_path, "Expense Reports")
        os.makedirs(export_dir, exist_ok=True)
        all_exp = self.expenses + [e for e in self.memory if not any(self.is_duplicate(e, c) for c in self.expenses)]
        month_exp = [e for e in all_exp if datetime.fromtimestamp(e.date).month == month and datetime.fromtimestamp(e.date).year == year]
        if not month_exp:
            print(f"No data found for {MONTH_NAMES[month-1]} {year}. Report not generated.")
            return
        filename = f"expense_report_{month:02d}-{year}.csv"
        filepath = os.path.join(export_dir, filename)
        # --- Analysis Section ---
        export_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        total = sum(e.amount for e in month_exp)
        # Category-wise totals
        cat_totals = [0.0]*len(self.category_names)
        for e in month_exp:
            cat_totals[e.category] += e.amount
        # Payment method totals
        pm_totals = [0.0]*len(self.payment_method_names)
        for e in month_exp:
            pm_totals[e.payment_method] += e.amount
        # Highest expense
        highest = max(month_exp, key=lambda e: e.amount)
        highest_dt = datetime.fromtimestamp(highest.date)
        # --- Write to CSV ---
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["SEP=,"])
            writer.writerow([f"Expense Analysis for {MONTH_NAMES[month-1]} {year}"])
            writer.writerow([f"Exported on: {export_time}"])
            writer.writerow([])
            writer.writerow(["Detailed Expenses"])
            writer.writerow(["Index","Date","Amount","Description","Category","Payment Method","Day of Week","Month","Year"])
            for i, e in enumerate(sorted(month_exp, key=lambda e: -e.date)):
                dt = datetime.fromtimestamp(e.date)
                writer.writerow([
                    i+1, dt.strftime('%d-%m-%Y'), f"{e.amount:.2f}", e.description, self.category_names[e.category],
                    self.payment_method_names[e.payment_method], WEEKDAYS[dt.weekday()], MONTH_NAMES[dt.month-1], dt.year
                ])
            writer.writerow([])
            writer.writerow(["Total Expenses", f"{total:.2f}"])
            writer.writerow([])
            writer.writerow(["Category-wise Totals"])
            writer.writerow(["Category", "Total", "% of Total"])
            for i, amt in enumerate(cat_totals):
                if amt > 0:
                    writer.writerow([self.category_names[i], f"{amt:.2f}", f"{amt/total*100:.2f}%"])
            writer.writerow([])
            writer.writerow(["Payment Method Totals"])
            writer.writerow(["Payment Method", "Total"])
            for i, amt in enumerate(pm_totals):
                if amt > 0:
                    writer.writerow([self.payment_method_names[i], f"{amt:.2f}"])
            writer.writerow([])
            writer.writerow(["Highest Expense"])
            writer.writerow(["Amount", "Description", "Category", "Payment Method", "Date"])
            writer.writerow([
                f"{highest.amount:.2f}", highest.description, self.category_names[highest.category],
                self.payment_method_names[highest.payment_method], highest_dt.strftime('%d-%m-%Y')
            ])
        print(f"Expense Report is generated with filename: {filepath}")

    def export_to_excel_date_range(self, start_date, end_date):
        # Use default downloads folder
        downloads_path = os.path.expanduser("~/Downloads")
        export_dir = os.path.join(downloads_path, "Expense Reports")
        os.makedirs(export_dir, exist_ok=True)
        all_exp = self.expenses + [e for e in self.memory if not any(self.is_duplicate(e, c) for c in self.expenses)]
        range_exp = [e for e in all_exp if start_date <= datetime.fromtimestamp(e.date) <= end_date]
        if not range_exp:
            print(f"No data found for the selected date range. Report not generated.")
            return
        filename = f"expense_report_{start_date.strftime('%d-%m-%Y')}_to_{end_date.strftime('%d-%m-%Y')}.csv"
        filepath = os.path.join(export_dir, filename)
        # --- Analysis Section ---
        export_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        total = sum(e.amount for e in range_exp)
        # Category-wise totals
        cat_totals = [0.0]*len(self.category_names)
        for e in range_exp:
            cat_totals[e.category] += e.amount
        # Payment method totals
        pm_totals = [0.0]*len(self.payment_method_names)
        for e in range_exp:
            pm_totals[e.payment_method] += e.amount
        # Highest expense
        highest = max(range_exp, key=lambda e: e.amount)
        highest_dt = datetime.fromtimestamp(highest.date)
        # --- Write to CSV ---
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["SEP=,"])
            writer.writerow([f"Expense Analysis from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}"])
            writer.writerow([f"Exported on: {export_time}"])
            writer.writerow([])
            writer.writerow(["Detailed Expenses"])
            writer.writerow(["Index","Date","Amount","Description","Category","Payment Method","Day of Week","Month","Year"])
            for i, e in enumerate(sorted(range_exp, key=lambda e: -e.date)):
                dt = datetime.fromtimestamp(e.date)
                writer.writerow([
                    i+1, dt.strftime('%d-%m-%Y'), f"{e.amount:.2f}", e.description, self.category_names[e.category],
                    self.payment_method_names[e.payment_method], WEEKDAYS[dt.weekday()], MONTH_NAMES[dt.month-1], dt.year
                ])
            writer.writerow([])
            writer.writerow(["Total Expenses", f"{total:.2f}"])
            writer.writerow([])
            writer.writerow(["Category-wise Totals"])
            writer.writerow(["Category", "Total", "% of Total"])
            for i, amt in enumerate(cat_totals):
                if amt > 0:
                    writer.writerow([self.category_names[i], f"{amt:.2f}", f"{amt/total*100:.2f}%"])
            writer.writerow([])
            writer.writerow(["Payment Method Totals"])
            writer.writerow(["Payment Method", "Total"])
            for i, amt in enumerate(pm_totals):
                if amt > 0:
                    writer.writerow([self.payment_method_names[i], f"{amt:.2f}"])
            writer.writerow([])
            writer.writerow(["Highest Expense"])
            writer.writerow(["Amount", "Description", "Category", "Payment Method", "Date"])
            writer.writerow([
                f"{highest.amount:.2f}", highest.description, self.category_names[highest.category],
                self.payment_method_names[highest.payment_method], highest_dt.strftime('%d-%m-%Y')
            ])
        print(f"Expense Report is generated with filename: {filepath}")

    def update_balance(self, is_bank):
        bal = self.bank_balance if is_bank else self.cash_balance
        print(f"Current {'bank' if is_bank else 'cash'} balance: {bal:.2f}")
        try:
            val = input("Enter new amount: ")
            amount = float(val)
        except:
            print("Invalid amount.")
            return
        now = datetime.now().timestamp()
        if is_bank:
            self.bank_balance = amount
            self.bank_history.append(BalanceEntry(amount, now))
            if len(self.bank_history) > MAX_BALANCE_HISTORY:
                self.bank_history = self.bank_history[-MAX_BALANCE_HISTORY:]
        else:
            self.cash_balance = amount
            self.cash_history.append(BalanceEntry(amount, now))
            if len(self.cash_history) > MAX_BALANCE_HISTORY:
                self.cash_history = self.cash_history[-MAX_BALANCE_HISTORY:]
        self.save_balance()
        print(f"{'Bank' if is_bank else 'Cash'} balance updated successfully.")

    def show_balance_history(self, is_bank):
        bal = self.bank_balance if is_bank else self.cash_balance
        hist = self.bank_history if is_bank else self.cash_history
        print(f"\n--- {'Bank' if is_bank else 'Cash'} Balance History ---\nCurrent balance: {bal:.2f}")
        if not hist:
            print("No history available.")
            return
        for i, h in enumerate(hist):
            dt = datetime.fromtimestamp(h.date)
            print(f"{i+1}. {h.amount:.2f} on {dt.strftime('%d-%m-%Y')}")

    def clear_memory(self):
        """Clear all memory entries while keeping current expenses"""
        if not self.memory:
            print("Memory is already empty.")
            return
        
        confirm = input("Are you sure you want to clear all memory entries? This action cannot be undone. (y/n): ")
        if confirm.lower() == 'y':
            self.memory.clear()
            self.save_expenses()
            print("Memory cleared successfully.")
        else:
            print("Memory clear operation cancelled.")

    def reload_categories(self):
        """Force reload categories from file"""
        print("Reloading categories from file...")
        self.load_categories()
        print(f"Categories reloaded. Total categories: {len(self.category_names)}")
        for i, cat in enumerate(self.category_names):
            print(f"  {i}: {cat}")

    def reset_categories(self):
        """Reset categories to default values"""
        print("Resetting categories to default values...")
        self.category_names = [
            "Food & Groceries", "Transport", "Utilities", "Entertainment", "Shopping",
            "Housing", "Investment", "Healthcare", "Education", "Banking", "Miscellaneous"
        ]
        self.save_categories()
        print("Categories reset to default values:")
        for i, cat in enumerate(self.category_names):
            print(f"  {i}: {cat}")

    # ... (Other methods for edit/delete balance history, export date range, etc. can be added similarly)

def show_main_menu():
    print("\n--- Expense Tracker Menu ---\n1. Expenses Management\n2. Balance Management\n3. Reports & Analysis\n4. Settings & Tools\n5. Exit\nChoose option: ", end='')

def show_expenses_menu():
    print("\n--- Expenses Management ---\n1. Add Expense\n2. List Expenses\n3. Edit Expenses\n4. Delete Expenses\n5. Back to Main Menu\nChoose option: ", end='')

def show_balance_menu():
    print("\n--- Balance Management ---\n1. Update Balance (Bank/Cash)\n2. View Balance History (Bank/Cash)\n3. Back to Main Menu\nChoose option: ", end='')

def show_reports_menu():
    print("\n--- Reports & Analysis ---\n1. Total Expenses\n2. Category Summary\n3. Highest Expense\n4. Budget Alert\n5. Export to Excel\n6. Back to Main Menu\nChoose option: ", end='')

def show_export_menu():
    print("\n--- Export to Excel ---\n1. Export Current Month\n2. Export Specific Month\n3. Export Custom Date Range\n4. Back to Reports Menu\nChoose option: ", end='')

def show_settings_menu():
    print("\n--- Settings & Tools ---\n1. Add Category\n2. Clear Memory\n3. Reload Categories\n4. Reset Categories\n5. Back to Main Menu\nChoose option: ", end='')

def main():
    tracker = ExpenseTracker()
    tracker.init_tracker()
    while True:
        show_main_menu()
        try:
            choice = int(input())
        except:
            print("Invalid input.")
            continue
        if choice == 1:
            while True:
                show_expenses_menu()
                try:
                    ch = int(input())
                except:
                    print("Invalid input.")
                    continue
                if ch == 1:
                    try:
                        amount = float(input("Amount: "))
                        desc = input("Description: ")[:MAX_DESC]
                        print("Categories:")
                        for i, cat in enumerate(tracker.category_names):
                            print(f"{i}: {cat}")
                        category = int(input("Choose category: "))
                        print("Payment Methods:")
                        for i, pm in enumerate(tracker.payment_method_names):
                            print(f"{i}: {pm}")
                        payment_method = int(input("Choose payment method: "))
                        use_current = input("Use current date? (y/n): ").strip().lower()
                        if use_current == 'n':
                            d, m, y = map(int, input("Enter date (DD MM YYYY): ").split())
                            dt = datetime(y, m, d, 12)
                        else:
                            dt = datetime.now()
                        tracker.add_expense(amount, desc, category, payment_method, dt.timestamp())
                    except Exception as e:
                        print("Invalid input.", e)
                elif ch == 2:
                    tracker.list_expenses()
                elif ch == 3:
                    tracker.list_expenses()
                    try:
                        idx = int(input("Enter number to edit (0 to cancel): "))
                        if idx == 0:
                            continue
                        tracker.edit_expense(idx-1, False)
                    except:
                        print("Invalid input.")
                elif ch == 4:
                    tracker.list_expenses()
                    try:
                        idx = int(input("Enter number to delete (0 to cancel): "))
                        if idx == 0:
                            continue
                        all_exp = tracker.expenses + [e for e in tracker.memory if not any(tracker.is_duplicate(e, c) for c in tracker.expenses)]
                        all_exp = sorted(all_exp, key=lambda e: -e.date)
                        if 1 <= idx <= len(all_exp):
                            tracker.remove_expense(all_exp[idx-1])
                        else:
                            print("Invalid selection.")
                    except:
                        print("Invalid input.")
                elif ch == 5:
                    break
                else:
                    print("Invalid option.")
        elif choice == 2:
            while True:
                show_balance_menu()
                try:
                    ch = int(input())
                except:
                    print("Invalid input.")
                    continue
                if ch == 1:
                    is_bank = int(input("Update Bank (1) or Cash (2) balance? "))
                    if is_bank in [1,2]:
                        tracker.update_balance(is_bank==1)
                elif ch == 2:
                    is_bank = int(input("View Bank (1) or Cash (2) history? "))
                    if is_bank in [1,2]:
                        tracker.show_balance_history(is_bank==1)
                elif ch == 3:
                    break
                else:
                    print("Invalid option.")
        elif choice == 3:
            while True:
                show_reports_menu()
                try:
                    ch = int(input())
                except:
                    print("Invalid input.")
                    continue
                if ch == 1:
                    total = sum(e.amount for e in tracker.expenses)
                    print(f"Total for all current expenses: {total:.2f}")
                elif ch == 2:
                    tracker.category_summary()
                elif ch == 3:
                    tracker.find_highest_expense()
                elif ch == 4:
                    try:
                        budget = float(input("Enter monthly budget: "))
                        tracker.budget_alert(budget)
                    except:
                        print("Invalid input.")
                elif ch == 5:
                    while True:
                        show_export_menu()
                        try:
                            export_ch = int(input())
                        except:
                            print("Invalid input.")
                            continue
                        if export_ch == 1:
                            now = datetime.now()
                            tracker.export_to_excel(now.year, now.month)
                        elif export_ch == 2:
                            try:
                                val = input("Enter month (1-12) and year (YYYY): ")
                                month, year = map(int, val.strip().split())
                                if not (1 <= month <= 12 and 1900 <= year <= 2200):
                                    print("Invalid month or year.")
                                    continue
                                tracker.export_to_excel(year, month)
                            except:
                                print("Invalid input.")
                        elif export_ch == 3:
                            try:
                                start_str = input("Enter start date (DD MM YYYY): ")
                                end_str = input("Enter end date (DD MM YYYY): ")
                                sd, sm, sy = map(int, start_str.strip().split())
                                ed, em, ey = map(int, end_str.strip().split())
                                start_date = datetime(sy, sm, sd, 0, 0, 0)
                                end_date = datetime(ey, em, ed, 23, 59, 59)
                                tracker.export_to_excel_date_range(start_date, end_date)
                            except:
                                print("Invalid input.")
                        elif export_ch == 4:
                            break
                        else:
                            print("Invalid option.")
                elif ch == 6:
                    break
                else:
                    print("Invalid option.")
        elif choice == 4:
            while True:
                show_settings_menu()
                try:
                    ch = int(input())
                except:
                    print("Invalid input.")
                    continue
                if ch == 1:
                    name = input("Enter new category name: ").strip()
                    if name:
                        tracker.add_category(name)
                elif ch == 2:
                    tracker.clear_memory()
                elif ch == 3:
                    tracker.reload_categories()
                elif ch == 4:
                    tracker.reset_categories()
                elif ch == 5:
                    break
                else:
                    print("Invalid option.")
        elif choice == 5:
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main() 