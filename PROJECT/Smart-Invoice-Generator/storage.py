# storage.py
import os
import time
import json
from typing import List, Dict, Any, Optional

from invoice_types import INVOICE_TYPE_MAP, Invoice
from utils import FileLock, FileLockError, colorize

class Storage:
    """
    Handles saving and loading invoices to/from a JSON file with file locking
    and error handling for corrupt data.
    """
    def __init__(self, filepath: str = "Smart-Invoice-Generator/data/invoices.json"):
        self.filepath = filepath
        self.lock_path = f"{filepath}.lock"
        self.directory = os.path.dirname(filepath)
        self._ensure_dir_exists()

    def _ensure_dir_exists(self):
        """Creates the data directory if it doesn't exist, with error handling."""
        try:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
        except OSError as e:
            print(colorize(f"Fatal: Could not create data directory at '{self.directory}'. Please check permissions. Error: {e}", "red"))
            exit(1) # Exit if we can't create the data directory

    def _save_all_invoices(self, invoices: List[Dict]):
        """Internal method to write a list of invoice dicts to the file."""
        try:
            with FileLock(self.lock_path):
                with open(self.filepath, "w") as f:
                    json.dump(invoices, f, indent=4)
        except (IOError, OSError) as e:
            raise IOError(f"Failed to write to data file: {e}")
        except FileLockError as e:
            raise e # Re-raise to be handled by the caller

    def save_invoice(self, invoice: Invoice):
        """Saves a single invoice to the JSON file."""
        all_invoices_raw = self.load_all_raw_invoices()
        all_invoices_raw.append(invoice.to_dict())
        self._save_all_invoices(all_invoices_raw)

    def load_all_raw_invoices(self) -> List[Dict[str, Any]]:
        """Loads the raw list of invoice dictionaries from the file."""
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r") as f:
                # Handle case where file is empty
                content = f.read()
                if not content:
                    return []
                data = json.loads(content)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError):
            print(colorize(f"Warning: The invoice file at '{self.filepath}' is corrupted. A backup will be created.", "red"))
            os.rename(self.filepath, f"{self.filepath}.bak_{int(time.time())}")
            return []
        except (IOError, OSError) as e:
            print(colorize(f"Error reading from data file: {e}", "red"))
            return []

    def load_invoices(self, paid_status: Optional[bool] = None) -> List[Invoice]:
        """
        Loads and deserializes all invoices, skipping any corrupted records.
        """
        raw_invoices = self.load_all_raw_invoices()
        invoices = []
        for inv_data in raw_invoices:
            try:
                invoice_type_str = inv_data.get("invoice_type", "ProductInvoice")
                invoice_class = INVOICE_TYPE_MAP.get(invoice_type_str)
                if invoice_class:
                    invoice = invoice_class.from_dict(inv_data)
                    
                    if paid_status is None or (paid_status and invoice.is_paid) or (not paid_status and not invoice.is_paid):
                        invoices.append(invoice)
                else:
                    print(colorize(f"Warning: Unknown invoice type '{invoice_type_str}' found for invoice ID {inv_data.get('invoice_id')}. Skipping.", "yellow"))
            except (ValueError, TypeError) as e:
                print(colorize(f"Warning: Skipping a corrupt invoice record. Error: {e}", "yellow"))
                continue
        
        invoices.sort(key=lambda inv: inv.issue_date, reverse=True)
        return invoices

    def update_invoice_status(self, invoice_id: str, new_status: str):
        """Updates the status of a specific invoice."""
        raw_invoices = self.load_all_raw_invoices()
        invoice_found = False
        for inv_data in raw_invoices:
            if inv_data["invoice_id"] == invoice_id:
                inv_data["status"] = new_status
                invoice_found = True
                break
        
        if invoice_found:
            self._save_all_invoices(raw_invoices)
        else:
            raise ValueError(f"Invoice with ID {invoice_id} not found.")
            
    def get_summary_report(self) -> Dict[str, Any]:
        """Generates a financial summary from all invoices."""
        invoices = self.load_invoices()
        paid_invoices = [inv for inv in invoices if inv.is_paid]
        unpaid_invoices = [inv for inv in invoices if not inv.is_paid]
        return {
            "total_invoices": len(invoices),
            "paid_invoices": len(paid_invoices),
            "unpaid_invoices": len(unpaid_invoices),
            "total_revenue": sum(inv.total for inv in paid_invoices),
            "pending_revenue": sum(inv.total for inv in unpaid_invoices),
        }
