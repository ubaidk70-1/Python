# client.py
import re
from typing import Dict, Any

class Client:
    """
    Represents a client with contact information.

    Attributes:
        name (str): The client's full name.
        email (str): The client's email address.
        phone (str): The client's phone number.
        client_id (str): A unique identifier for the client.
    """
    def __init__(self, name: str, email: str, phone: str, client_id: str = None):
        if not name or not name.strip():
            raise ValueError("Client name cannot be empty.")
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise ValueError("Invalid email format.")
        
        self.name = name.strip()
        self.email = email
        self.phone = phone
        # A simple, deterministic ID generation for this CLI tool
        self.client_id = client_id or f"CLIENT-{abs(hash(self.name + self.email)) % 10000:04d}"

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the client object to a dictionary."""
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "client_id": self.client_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Client':
        """Creates a Client instance from a dictionary."""
        try:
            return cls(
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                client_id=data.get("client_id")
            )
        except KeyError as e:
            raise ValueError(f"Missing required client data: {e}")

    def __str__(self) -> str:
        """Provides a clean string representation for display."""
        return f"{self.name}\n{self.email}\n{self.phone}"

    def __repr__(self) -> str:
        """Provides a developer-friendly representation."""
        return f"Client(name='{self.name}', email='{self.email}')"

