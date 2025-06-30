# invoice.py
from datetime import date, timedelta
from typing import List, Optional
import uuid
from decimal import Decimal, InvalidOperation

from client import Client
from item import Item
from utils import format_currency, colorize

class Invoice:
    """
    Represents a standard invoice, using Decimal for financial precision.
    """
    def __init__(
        self,
        client: Client,
        items: List[Item],
        issue_date: Optional[date] = None,
        due_days: int = 30,
        discount: Decimal = Decimal("0.0"),
        tax_rate: Decimal = Decimal("5.0"),
        status: str = "Unpaid",
        invoice_id: Optional[str] = None
    ):
        if not items:
            raise ValueError("An invoice must have at least one line item.")
        
        self.client = client
        self.items = items
        self.issue_date = issue_date or date.today()
        self.due_date = self.issue_date + timedelta(days=due_days)
        
        if discount < Decimal(0):
            raise ValueError("Discount cannot be negative.")
        self.discount = discount

        if tax_rate < Decimal(0):
            raise ValueError("Tax rate cannot be negative.")
        self.tax_rate = tax_rate
        
        self.status = status
        self.invoice_id = invoice_id or f"INV-{str(uuid.uuid4())[:8].upper()}"

    @property
    def is_paid(self) -> bool:
        """Returns True if the invoice status is 'Paid'."""
        return self.status.lower() == "paid"

    def mark_as_paid(self):
        """Sets the invoice status to 'Paid'."""
        self.status = "Paid"

    @property
    def due_in_days(self) -> int:
        """Calculates the number of days until the invoice is due."""
        if self.is_paid:
            return 0
        days_diff = (self.due_date - date.today()).days
        return max(0, days_diff)

    @property
    def subtotal(self) -> Decimal:
        """Calculates the total cost of all items before tax and discount."""
        return sum(item.total for item in self.items)

    @property
    def tax_amount(self) -> Decimal:
        """Calculates the tax amount based on the subtotal."""
        return self.subtotal * (self.tax_rate / Decimal(100))

    @property
    def total(self) -> Decimal:
        """Calculates the final total after tax and discount."""
        final_total = self.subtotal + self.tax_amount - self.discount
        return max(Decimal(0), final_total) # Ensure total is not negative

    def to_dict(self) -> dict:
        """Serializes the invoice object to a dictionary for JSON storage."""
        return {
            "invoice_id": self.invoice_id,
            "invoice_type": self.__class__.__name__,
            "client": self.client.to_dict(),
            "items": [item.to_dict() for item in self.items],
            "issue_date": self.issue_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "tax_rate": str(self.tax_rate),
            "discount": str(self.discount),
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> 'Invoice':
        """Creates an Invoice instance from a dictionary."""
        raise NotImplementedError("This method must be implemented by subclasses.")

    def __str__(self) -> str:
        """Provides a user-friendly string representation of the invoice."""
        due_text = f"PAID" if self.is_paid else f"Due in {self.due_in_days} days"
        status_color = "green" if self.is_paid else "yellow"
        header = f"--- INVOICE {self.invoice_id} ---\n"
        status_line = f"Status: {self.status.upper()} ({colorize(due_text, status_color)})\n"
        
        client_info = f"Bill To:\n{self.client}\n"
        dates = f"Issued: {self.issue_date.strftime('%B %d, %Y')}\nDue:    {self.due_date.strftime('%B %d, %Y')}\n"
        
        items_header = "\n--- Line Items ---\n"
        items_table = "{:<25} {:>10} {:>15} {:>15}\n".format("Description", "Qty/Hrs", "Unit Price", "Total")
        items_table += "-" * 70 + "\n"
        for item in self.items:
            items_table += f"{item.name:<25.25} {str(item.quantity):>10} {format_currency(item.price):>15} {format_currency(item.total):>15}\n"
            
        summary = "\n--- Summary ---\n"
        summary += f"{'Subtotal:':<15} {format_currency(self.subtotal):>15}\n"
        summary += f"{'Tax ({self.tax_rate}%):':<15} {format_currency(self.tax_amount):>15}\n"
        if self.discount > 0:
            summary += f"{'Discount:':<15} {format_currency(-self.discount):>15}\n"
        summary += "-" * 31 + "\n"
        summary += f"{'Total:':<15} {colorize(format_currency(self.total), 'green'):>15}\n"
        
        return header + status_line + client_info + dates + items_header + items_table + summary

    def __repr__(self) -> str:
        """Provides a developer-friendly, unambiguous representation."""
        return f"{self.__class__.__name__}(id='{self.invoice_id}', client='{self.client.name}', total={self.total:.2f})"

    def __eq__(self, other) -> bool:
        """Two invoices are equal if they have the same ID."""
        if not isinstance(other, Invoice):
            return NotImplemented
        return self.invoice_id == other.invoice_id
