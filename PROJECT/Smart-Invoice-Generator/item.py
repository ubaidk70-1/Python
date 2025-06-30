# item.py
from typing import Dict, Any
from decimal import Decimal, InvalidOperation

class Item:
    """
    Represents a single line item in an invoice (product or service).
    Uses Decimal for precision in financial calculations.

    Attributes:
        name (str): The name of the item or service.
        quantity (Decimal): The quantity of the item or hours for a service.
        price (Decimal): The price per item or the hourly rate.
    """
    def __init__(self, name: str, quantity: Decimal, price: Decimal):
        if not name or not name.strip():
            raise ValueError("Item name cannot be empty.")
        if not isinstance(quantity, Decimal) or quantity <= Decimal(0):
            raise ValueError("Quantity/hours must be a positive number.")
        if not isinstance(price, Decimal) or price < Decimal(0):
            raise ValueError("Price/rate must be a non-negative number.")
            
        self.name = name.strip()
        self.quantity = quantity
        self.price = price

    @property
    def total(self) -> Decimal:
        """Calculates the total cost for this line item."""
        return self.quantity * self.price

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the item object to a dictionary."""
        return {
            "name": self.name,
            "quantity": str(self.quantity), # Store as string to preserve precision
            "price": str(self.price),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        """Creates an Item instance from a dictionary."""
        try:
            return cls(
                name=data["name"],
                quantity=Decimal(data["quantity"]),
                price=Decimal(data["price"])
            )
        except (KeyError, InvalidOperation) as e:
            raise ValueError(f"Invalid item data provided: {e}")
        
    def __repr__(self) -> str:
        """Provides a developer-friendly representation."""
        return f"Item(name='{self.name}', quantity={self.quantity}, price={self.price})"

    def __eq__(self, other) -> bool:
        """Two items are equal if their attributes are the same."""
        if not isinstance(other, Item):
            return NotImplemented
        return (self.name == other.name and 
                self.quantity == other.quantity and 
                self.price == other.price)
