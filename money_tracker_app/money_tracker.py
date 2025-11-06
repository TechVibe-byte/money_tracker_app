import json
import os
import uuid
from datetime import datetime
from collections import defaultdict
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

DATA_FILE = "money_tracker_data.json"

# Define your expense categories
EXPENSE_CATEGORIES = [
    "Transport", "Groceries", "Personal", "Food", "Health", "Tax", "Housing",
    "Gifts & Charity", "Entertainment & Subscriptions", "Another Subscription",
    "Education Fee", "Pet Maintenance", "Gadgets & Electronics", "Plantation",
    "Other" # Added 'Other' for flexibility
]

def display_banner():
    """Displays a banner for the application."""
    banner_text = """
███╗   ███╗ ██████╗ ███╗   ██╗███████╗██╗   ██╗
████╗ ████║██╔═══██╗████╗  ██║██╔════╝╚██╗ ██╔╝
██╔████╔██║██║   ██║██╔██╗ ██║█████╗   ╚████╔╝ 
██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══╝    ╚██╔╝  
██║ ╚═╝ ██║╚██████╔╝██║ ╚████║███████╗   ██║   
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   
"""
    console.print(f"[bold green]{banner_text}[/bold green]")
    console.print("[bold yellow]Welcome to your Personal Money Tracker![/bold yellow]")
    console.print("[bold blue]Let's manage your finances.[/bold blue]\n")

def load_data():
    if not os.path.exists(DATA_FILE):
        return [], [], [], [], []
    with open(DATA_FILE, 'r') as f:
        try:
            data = json.load(f)
            # Migration for old data format
            if data and data.get('daily_expenses') and isinstance(data['daily_expenses'][0], list):
                console.print("[yellow]Old data format detected. Migrating to new format...[/yellow]")
                for L_name in ['credit_expenses', 'borrowed_records', 'lent_records', 'daily_expenses']:
                    migrated_list = []
                    for item in data.get(L_name, []):
                        migrated_list.append({'id': str(uuid.uuid4()), 'date': item[0], 'amount': item[1], 'desc': item[2]})
                    data[L_name] = migrated_list
                
                migrated_loans = []
                for item in data.get('loan_records', []):
                    migrated_loans.append({'id': str(uuid.uuid4()), 'date': item[0], 'amount': item[1], 'desc': item[2], 'bank_name': item[3]})
                data['loan_records'] = migrated_loans
                
                # Save migrated data
                with open(DATA_FILE, 'w') as fw:
                    json.dump(data, fw, indent=4)
                console.print("[green]Migration successful![/green]")

            return data.get('credit_expenses', []), data.get('borrowed_records', []), data.get('lent_records', []), data.get('loan_records', []), data.get('daily_expenses', [])
        except (json.JSONDecodeError, IndexError, KeyError):
            # This will handle empty file, corrupted JSON, or old format with missing keys
            return [], [], [], [], []

def save_data():
    data = {
        'credit_expenses': credit_expenses,
        'borrowed_records': borrowed_records,
        'lent_records': lent_records,
        'loan_records': loan_records,
        'daily_expenses': daily_expenses
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Storage lists
credit_expenses, borrowed_records, lent_records, loan_records, daily_expenses = load_data()


def format_amount(amount):
    return f"{amount:,.2f}rs"


def add_record(record_list, title):
    desc = Prompt.ask(f"[cyan]Enter {title} description[/cyan]")
    amount_str = Prompt.ask(f"[yellow]Enter amount (in ₹)[/yellow]")
    try:
        amount = float(amount_str)
    except ValueError:
        console.print("[red]Invalid amount. Please enter a number.[/red]")
        return

    date = datetime.today().strftime("%Y-%m-%d")
    record = {'id': str(uuid.uuid4()), 'date': date, 'amount': amount, 'desc': desc}
    
    # --- NEW CODE FOR CATEGORY SELECTION ---
    if title == "Daily Expense":
        console.print("\n[bold blue]Select a category:[/bold blue]")
        for i, category in enumerate(EXPENSE_CATEGORIES):
            console.print(f"[cyan]{i+1}.[/cyan] {category}")
        
        while True:
            category_choice = Prompt.ask(f"[bold yellow]Enter category number [1-{len(EXPENSE_CATEGORIES)}][/bold yellow]")
            try:
                selected_category = EXPENSE_CATEGORIES[int(category_choice) - 1]
                record['category'] = selected_category
                break
            except (ValueError, IndexError):
                console.print("[red]Invalid category number. Please try again.[/red]")
    # --- END NEW CODE ---

    if title in ["Borrowed Money", "Lent Money"]:
        status = Prompt.ask("[cyan]Enter status (e.g., Pending, Paid, Received)[/cyan]", default="Pending")
        record['status'] = status
        
    record_list.append(record)
    save_data()
    console.print(f"[green]✅ {title} added successfully![/green]")

def add_loan_record():
    desc = Prompt.ask("[cyan]Enter loan description[/cyan]")
    amount_str = Prompt.ask("[yellow]Enter amount (in ₹)[/yellow]")
    bank_name = Prompt.ask("[cyan]Enter bank name[/cyan]")
    try:
        amount = float(amount_str)
    except ValueError:
        console.print("[red]Invalid amount. Please enter a number.[/red]")
        return

    date = datetime.today().strftime("%Y-%m-%d")
    loan_records.append({'id': str(uuid.uuid4()), 'date': date, 'amount': amount, 'desc': desc, 'bank_name': bank_name})
    save_data()
    console.print("[green]✅ Loan added successfully![/green]")

def delete_record(record_list, record_id):
    record_found = False
    for record in record_list:
        if record['id'] == record_id:
            record_list.remove(record)
            record_found = True
            break
    if record_found:
        save_data()
        console.print("[green]✅ Record deleted successfully![/green]")
    else:
        console.print("[red]Record not found.[/red]")

def edit_record(record_list, record_id, title):
    record_to_edit = None
    for record in record_list:
        if record['id'] == record_id:
            record_to_edit = record
            break
    
    if record_to_edit:
        console.print(f"Editing {title} record. Press Enter to keep current value.")
        
        new_desc = Prompt.ask(f"[cyan]Enter new description[/cyan]", default=record_to_edit['desc'])
        new_amount_str = Prompt.ask(f"[yellow]Enter new amount (in ₹)[/yellow]", default=str(record_to_edit['amount']))
        
        # --- NEW CODE FOR EDITING CATEGORY ---
        if title == "Daily Expenses":
            console.print("\n[bold blue]Select a new category (or press Enter to keep current):[/bold blue]")
            for i, category in enumerate(EXPENSE_CATEGORIES):
                console.print(f"[cyan]{i+1}.[/cyan] {category}")
            
            current_category_index = EXPENSE_CATEGORIES.index(record_to_edit.get('category', 'Other')) + 1 if record_to_edit.get('category') else ''
            category_choice = Prompt.ask(
                f"[bold yellow]Enter new category number (current: {record_to_edit.get('category', 'N/A')})[/bold yellow]", 
                default=str(current_category_index)
            )
            if category_choice:
                try:
                    selected_category = EXPENSE_CATEGORIES[int(category_choice) - 1]
                    record_to_edit['category'] = selected_category
                except (ValueError, IndexError):
                    console.print("[red]Invalid category number. Keeping current category.[/red]")
        # --- END NEW CODE ---

        if title in ["Borrowed Records", "Lent Records"]:
            new_status = Prompt.ask("[cyan]Enter new status[/cyan]", default=record_to_edit.get('status', 'Pending'))
            record_to_edit['status'] = new_status

        try:
            new_amount = float(new_amount_str)
        except ValueError:
            console.print("[red]Invalid amount. Please enter a number.[/red]")
            return

        record_to_edit['desc'] = new_desc
        record_to_edit['amount'] = new_amount
        save_data()
        console.print(f"[green]✅ {title} updated successfully![/green]")
    else:
        console.print("[red]Record not found.[/red]")

def edit_loan_record(record_list, record_id):
    record_to_edit = None
    for record in record_list:
        if record['id'] == record_id:
            record_to_edit = record
            break

    if record_to_edit:
        console.print("Editing loan record. Press Enter to keep current value.")
        
        new_desc = Prompt.ask("[cyan]Enter new description[/cyan]", default=record_to_edit['desc'])
        new_amount_str = Prompt.ask("[yellow]Enter new amount (in ₹)[/yellow]", default=str(record_to_edit['amount']))
        new_bank_name = Prompt.ask("[cyan]Enter new bank name[/cyan]", default=record_to_edit['bank_name'])

        try:
            new_amount = float(new_amount_str)
        except ValueError:
            console.print("[red]Invalid amount. Please enter a number.[/red]")
            return

        record_to_edit['desc'] = new_desc
        record_to_edit['amount'] = new_amount
        record_to_edit['bank_name'] = new_bank_name
        save_data()
        console.print("[green]✅ Loan updated successfully![/green]")
    else:
        console.print("[red]Record not found.[/red]")


def view_timeline(records, title, icon, editable=False, is_loan=False, show_status=False):
    if not records:
        console.print(f"[red]No {title.lower()} records found.[/red]")
        return

    grouped = defaultdict(list)
    total_all = 0
    for record in records:
        grouped[record['date']].append(record)

    sorted_dates = sorted(grouped.keys(), reverse=True)

    console.print(f'''
[bold magenta] 📒 {title} (Timeline View)[/bold magenta]
''')
    for date_str in sorted_dates:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d %B %Y")
        day_items = grouped[date_str]
        total_day = sum(item['amount'] for item in day_items)
        total_all += total_day

        console.print(f"[cyan]🗓️ {formatted_date:<18}[/cyan][green] 💰 {format_amount(total_day)}[/green]")
        console.print("   |")
        for record in day_items:
            id_str = f" [dim](ID: {record['id'][:8]})[/dim]" if editable else ""
            status_str = f" - [bold]{record.get('status', 'N/A')}[/bold]" if show_status else ""
            # --- NEW CODE FOR DISPLAYING CATEGORY ---
            category_str = f" ({record.get('category', 'N/A')})" if title == "Daily Expenses" else ""
            # --- END NEW CODE ---

            if is_loan:
                 console.print(f"   └── [yellow]{icon} {format_amount(record['amount']):>10}[/yellow] - {record['desc']} ([bold]{record['bank_name']}[/bold]){id_str}")
            else:
                console.print(f"   └── [yellow]{icon} {format_amount(record['amount']):>10}[/yellow] - {record['desc']}{category_str}{status_str}{id_str}") # Added category_str here
        console.print("")

    console.print("[bold green]==============================[/bold green]")
    console.print(f'''[bold green]🧮 Total {title}: {format_amount(total_all)}[/bold green]
''')

    if editable:
        while True:
            action = Prompt.ask("[bold yellow]Choose an action: (E)dit, (D)elete, or (B)ack to menu[/bold yellow]", choices=["e", "d", "b"], default="b").lower()
            if action == 'b':
                break
            
            record_id_prefix = Prompt.ask("[cyan]Enter the first 8 characters of the record ID[/cyan]")
            
            full_record_id = None
            for record in records:
                if record['id'].startswith(record_id_prefix):
                    full_record_id = record['id']
                    break
            
            if not full_record_id:
                console.print("[red]Record ID not found.[/red]")
                continue

            if action == 'd':
                delete_record(records, full_record_id)
                break 
            elif action == 'e':
                if is_loan:
                    edit_loan_record(records, full_record_id)
                else:
                    edit_record(records, full_record_id, title)
                break

def view_loans_timeline():
    view_timeline(loan_records, "Monthly Loans", "🏦", editable=True, is_loan=True)


def generate_totals():
    total_daily = sum(record['amount'] for record in daily_expenses)
    total_credit = sum(record['amount'] for record in credit_expenses)
    total_loans = sum(record['amount'] for record in loan_records)
    grand_total = total_daily + total_credit + total_loans

    table = Table(title="[bold green]Financial Summary[/bold green]")
    table.add_column("Category", justify="right", style="cyan", no_wrap=True)
    table.add_column("Total Amount", justify="right", style="magenta")

    table.add_row("Total Daily Expenses", format_amount(total_daily))
    table.add_row("Total Credit Bills", format_amount(total_credit))
    table.add_row("Total Loans", format_amount(total_loans))
    table.add_row("[bold]Grand Total[/bold]", f"[bold]{format_amount(grand_total)}[/bold]")

    console.print(table)


def main_menu():
    display_banner()
    while True:
        console.print('''[bold blue]
======== MONEY TRACKER MENU ========[/bold blue]
''')
        console.print("[bold cyan]1.[/bold cyan] Add Daily Expense")
        console.print("[bold cyan]2.[/bold cyan] View Daily Expenses")
        console.print("[bold cyan]3.[/bold cyan] Add Credit Expense")
        console.print("[bold cyan]4.[/bold cyan] View Credit Expenses")
        console.print("[bold cyan]5.[/bold cyan] Add Borrowed Money (you borrowed)")
        console.print("[bold cyan]6.[/bold cyan] View Borrowed Records")
        console.print("[bold cyan]7.[/bold cyan] Add Lent Money (you gave)")
        console.print("[bold cyan]8.[/bold cyan] View Lent Records")
        console.print("[bold cyan]9.[/bold cyan] Add Monthly Loan")
        console.print("[bold cyan]10.[/bold cyan] View Monthly Loans")
        console.print("[bold cyan]11.[/bold cyan] Generate Totals")
        console.print("[bold cyan]12.[/bold cyan] Exit")
        console.print("[bold blue]====================================[/bold blue]")

        choice = Prompt.ask("[bold magenta]Choose an option (1-12)[/bold magenta]", default="12")

        if choice == "1":
            add_record(daily_expenses, "Daily Expense")
        elif choice == "2":
            view_timeline(daily_expenses, "Daily Expenses", "🛒", editable=True)
        elif choice == "3":
            add_record(credit_expenses, "Credit Expense")
        elif choice == "4":
            view_timeline(credit_expenses, "Credit Expenses", "🛍️", editable=True)
        elif choice == "5":
            add_record(borrowed_records, "Borrowed Money")
        elif choice == "6":
            view_timeline(borrowed_records, "Borrowed Records", "📤", editable=True, show_status=True)
        elif choice == "7":
            add_record(lent_records, "Lent Money")
        elif choice == "8":
            view_timeline(lent_records, "Lent Records", "📥", editable=True, show_status=True)
        elif choice == "9":
            add_loan_record()
        elif choice == "10":
            view_loans_timeline()
        elif choice == "11":
            generate_totals()
        elif choice == "12":
            save_data()
            console.print("[bold magenta]Goodbye! Stay financially smart! 💸[/bold magenta]")
            break
        else:
            console.print("[red]Invalid choice. Please select from 1 to 12.[/red]")


if __name__ == "__main__":
    main_menu()
