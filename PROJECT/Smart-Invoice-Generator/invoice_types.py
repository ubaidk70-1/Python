# invoice_types.py
from datetime import date
from typing import List, Dict, Any
from decimal import Decimal, InvalidOperation

from invoice import Invoice
from client import Client
from item import Item

class ProductInvoice(Invoice):
    """An invoice specifically for selling products."""
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProductInvoice':
        """Creates a ProductInvoice from a dictionary record with error handling."""
        try:
            client = Client.from_dict(data["client"])
            items = [Item.from_dict(item) for item in data["items"]]
            return cls(
                client=client,
                items=items,
                issue_date=date.fromisoformat(data["issue_date"]),
                discount=Decimal(data.get("discount", "0.0")),
                tax_rate=Decimal(data.get("tax_rate", "5.0")),
                status=data.get("status", "Unpaid"),
                invoice_id=data["invoice_id"]
            )
        except (KeyError, ValueError, InvalidOperation) as e:
            raise ValueError(f"Failed to load ProductInvoice from corrupt data (ID: {data.get('invoice_id')}): {e}")

class ServiceInvoice(Invoice):
    """An invoice specifically for providing services."""
    def __str__(self) -> str:
        base_str = super().__str__()
        return base_str.replace("Qty/Hrs", "Hours").replace("Unit Price", "Hourly Rate")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ServiceInvoice':
        """Creates a ServiceInvoice from a dictionary record with error handling."""
        try:
            client = Client.from_dict(data["client"])
            items = [Item.from_dict(item) for item in data["items"]]
            return cls(
                client=client,
                items=items,
                issue_date=date.fromisoformat(data["issue_date"]),
                discount=Decimal(data.get("discount", "0.0")),
                tax_rate=Decimal(data.get("tax_rate", "5.0")),
                status=data.get("status", "Unpaid"),
                invoice_id=data["invoice_id"]
            )
        except (KeyError, ValueError, InvalidOperation) as e:
            raise ValueError(f"Failed to load ServiceInvoice from corrupt data (ID: {data.get('invoice_id')}): {e}")


# A mapping to dynamically load the correct class from the invoice type string
INVOICE_TYPE_MAP = {
    "ProductInvoice": ProductInvoice,
    "ServiceInvoice": ServiceInvoice,
}