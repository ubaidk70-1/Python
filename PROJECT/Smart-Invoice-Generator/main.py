# main.py
import os
import time
from datetime import datetime
from decimal import Decimal

from invoice_types import ProductInvoice, ServiceInvoice
from client import Client
from item import Item
from storage import Storage
from utils import (
    get_valid_input,
    format_currency,
    log_action,
    clear_screen,
    colorize,
    FileLockError
)


def create_new_invoice(storage: Storage):
    """Guides the user through creating a new invoice, with cancellation."""
    clear_screen()
    print(colorize("--- Create New Invoice ---", "cyan"))
    
    try:
        # Get Client Details
        client_name = get_valid_input("Enter client's full name", allow_cancel=True)
        client_email = get_valid_input("Enter client's email", "email", allow_cancel=True)
        client_phone = get_valid_input("Enter client's phone number", "phone", allow_cancel=True)
        client = Client(name=client_name, email=client_email, phone=client_phone)

        # Get Invoice Type
        invoice_type = get_valid_input(
            "Is this for 'products' or 'services'?",
            "invoice_type",
            ["products", "services"],
            allow_cancel=True
        ).lower()

        # Get Items/Services
        items = []
        item_class = ProductInvoice if invoice_type == "products" else ServiceInvoice
        
        while True:
            item_prompt = "product name" if invoice_type == "products" else "service name"
            item_name = get_valid_input(f"Enter {item_prompt} (or 'done' to finish)", allow_cancel=True)
            if item_name.lower() == "done":
                if not items:
                    print(colorize("You must add at least one item to create an invoice.", "red"))
                    continue # Ask again
                break

            qty_prompt = "quantity" if invoice_type == "products" else "hours worked"
            price_prompt = "price per item" if invoice_type == "products" else "hourly rate"
            
            quantity_str = get_valid_input(f"Enter {qty_prompt}", "decimal", allow_cancel=True)
            price_str = get_valid_input(f"Enter {price_prompt}", "decimal", allow_cancel=True)
            items.append(Item(name=item_name, quantity=Decimal(quantity_str), price=Decimal(price_str)))

        # Get Tax and Discount
        tax_rate_str = get_valid_input("Enter tax rate (e.g., 5 for 5%)", "decimal", default="5.0", allow_cancel=True)
        discount_str = get_valid_input("Enter discount amount (e.g., 10 for ₹10.00)", "decimal", default="0.0", allow_cancel=True)

        # Create and Save Invoice
        invoice = item_class(
            client=client, items=items, tax_rate=Decimal(tax_rate_str), discount=Decimal(discount_str)
        )
        storage.save_invoice(invoice)
        log_action(f"Created Invoice: {invoice.invoice_id} for Client: {client.name}")

        print("\n" + "=" * 50)
        print(colorize("Invoice Created Successfully!", "green"))
        print(invoice)
        print("=" * 50)

    except KeyboardInterrupt:
        print(colorize("\n\nInvoice creation cancelled. Returning to main menu.", "yellow"))
    except (ValueError, FileLockError) as e:
        print(colorize(f"\nError creating invoice: {e}", "red"))
    
    get_valid_input("\nPress Enter to return to the main menu...")


def view_past_invoices(storage: Storage):
    """Displays a list of past invoices and allows viewing details."""
    clear_screen()
    print(colorize("--- Past Invoices ---", "cyan"))
    invoices = storage.load_invoices()

    if not invoices:
        print(colorize("No invoices found.", "yellow"))
        get_valid_input("\nPress Enter to return to the main menu...")
        return

    while True:
        clear_screen()
        print(colorize("--- Past Invoices ---", "cyan"))
        # Re-fetch and display list each time in case it changed
        invoices = storage.load_invoices()
        if not invoices:
            print(colorize("No invoices found.", "yellow"))
            break

        for i, inv in enumerate(invoices):
            status_color = "green" if inv.is_paid else "yellow"
            print(
                f"{i + 1}. {inv.invoice_id} - {inv.client.name} - "
                f"Total: {format_currency(inv.total)} - "
                f"Status: {colorize(inv.status, status_color)}"
            )

        choice = get_valid_input(
            "\nEnter invoice number to view details (or 'back'): "
        )
        if choice.lower() == "back":
            break
        try:
            index = int(choice) - 1
            if 0 <= index < len(invoices):
                clear_screen()
                print(colorize("--- Invoice Details ---", "cyan"))
                print(invoices[index])
                print("=" * 70)
                get_valid_input("\nPress Enter to return to the list...")
            else:
                print(colorize("Invalid invoice number.", "red"))
                time.sleep(1)
        except ValueError:
            print(colorize("Invalid input. Please enter a number.", "red"))
            time.sleep(1)


def mark_invoice_as_paid(storage: Storage):
    """Marks a specific invoice as paid."""
    clear_screen()
    print(colorize("--- Mark Invoice as Paid ---", "cyan"))
    
    while True:
        # Load only unpaid invoices
        unpaid_invoices = storage.load_invoices(paid_status=False) 

        if not unpaid_invoices:
            print(colorize("No unpaid invoices found.", "yellow"))
            get_valid_input("\nPress Enter to return to the main menu...")
            return

        for i, inv in enumerate(unpaid_invoices):
            print(f"{i + 1}. {inv.invoice_id} - {inv.client.name} - Due: {inv.due_date.strftime('%Y-%m-%d')}")

        choice = get_valid_input(
            "\nEnter invoice number to mark as paid (or 'back'): "
        )
        if choice.lower() == "back":
            break
        try:
            index = int(choice) - 1
            if 0 <= index < len(unpaid_invoices):
                invoice_to_mark = unpaid_invoices[index]
                storage.update_invoice_status(invoice_to_mark.invoice_id, "Paid")
                log_action(f"Marked as Paid: {invoice_to_mark.invoice_id}")
                print(colorize(f"Invoice {invoice_to_mark.invoice_id} has been marked as paid.", "green"))
                get_valid_input("\nPress Enter to return to the main menu...")
                break # Exit after successfully marking one
            else:
                print(colorize("Invalid invoice number.", "red"))
        except (ValueError, FileLockError) as e:
            print(colorize(f"Error updating invoice: {e}", "red"))
        except IndexError:
             print(colorize("Invalid invoice number.", "red"))


def show_summary_report(storage: Storage):
    """Displays a summary report of all invoices."""
    clear_screen()
    print(colorize("--- Financial Summary Report ---", "cyan"))
    try:
        summary = storage.get_summary_report()
        print(f"Total Invoices: {summary['total_invoices']}")
        print(f"Paid Invoices: {summary['paid_invoices']}")
        print(f"Unpaid Invoices: {summary['unpaid_invoices']}")
        print("-" * 45)
        print(f"Total Revenue (from paid invoices): {colorize(format_currency(summary['total_revenue']), 'green')}")
        print(f"Pending Revenue (from unpaid invoices): {colorize(format_currency(summary['pending_revenue']), 'yellow')}")
        print("=" * 45)
    except Exception as e:
        print(colorize(f"Could not generate report. Error: {e}", "red"))

    get_valid_input("\nPress Enter to return to the main menu...")


def main():
    """Main application loop."""
    try:
        storage = Storage()
    except Exception as e:
        print(colorize(f"A critical error occurred on startup: {e}", "red"))
        return # Exit if storage can't be initialized

    menu_options = {
        "1": "Create New Invoice",
        "2": "View Past Invoices",
        "3": "Mark Invoice as Paid",
        "4": "Show Summary Report",
        "5": "Exit",
    }

    while True:
        clear_screen()
        print(colorize("\n=== Smart Invoice Generator ===", "blue"))
        for key, value in menu_options.items():
            print(f"{key}. {value}")
        print("=" * 30)

        choice = get_valid_input("Choose an option: ", "menu", menu_options.keys())

        if choice == "1":
            create_new_invoice(storage)
        elif choice == "2":
            view_past_invoices(storage)
        elif choice == "3":
            mark_invoice_as_paid(storage)
        elif choice == "4":
            show_summary_report(storage)
        elif choice == "5":
            print(colorize("Exiting. Goodbye!", "blue"))
            break


if __name__ == "__main__":
    main()
