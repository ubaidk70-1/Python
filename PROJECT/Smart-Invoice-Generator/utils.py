# utils.py
import os
import re
# fcntl will be imported conditionally later
import time
from datetime import datetime
from decimal import Decimal, InvalidOperation

# --- Custom Exceptions ---
class InvalidInputError(Exception):
    """Custom exception for invalid user input."""
    pass

class FileLockError(Exception):
    """Custom exception for file locking issues."""
    pass


# --- ANSI Color Codes for CLI Output ---
COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "endc": "\033[0m",
}

def colorize(text: str, color: str) -> str:
    """Wraps text in ANSI color codes."""
    return f"{COLORS.get(color, '')}{text}{COLORS['endc']}"


# --- Logging ---
LOG_FILE = "Smart-Invoice-Generator/logs/actions.log"

def log_action(log_message: str):
    """Logs actions like invoice creation or updates."""
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {log_message}\n")
    except (IOError, OSError) as e:
        print(colorize(f"Warning: Could not write to log file: {e}", "red"))

# --- Input Validation and Formatting ---
def get_valid_input(
    prompt: str,
    validation_type: str = "text",
    options: list = None,
    default: str = None,
    allow_cancel: bool = False
) -> str:
    """
    Prompts the user for input and validates it based on the specified type.
    Now supports cancellation.
    """
    prompt_suffix = " (or type 'cancel' to abort)" if allow_cancel else ""
    while True:
        user_input = input(colorize(f"{prompt}{prompt_suffix}: ", "yellow")).strip()
        
        if allow_cancel and user_input.lower() == 'cancel':
            raise KeyboardInterrupt # Use KeyboardInterrupt to signal cancellation

        if not user_input and default is not None:
            user_input = default

        try:
            if validation_type == "text":
                if not user_input:
                    raise InvalidInputError("Input cannot be empty.")
            elif validation_type == "email":
                if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user_input):
                    raise InvalidInputError("Invalid email format.")
            elif validation_type == "phone":
                if not re.match(r"^\+?1?\d{9,15}$", user_input):
                    raise InvalidInputError("Invalid phone format (e.g., 1234567890).")
            elif validation_type == "decimal":
                value = Decimal(user_input)
                if value < 0:
                    raise InvalidInputError("Value cannot be negative.")
            elif validation_type in ["menu", "invoice_type"]:
                if user_input.lower() not in [str(opt).lower() for opt in options]:
                    raise InvalidInputError(f"Invalid choice. Please select from: {', '.join(map(str, options))}")
            
            return user_input
        except (ValueError, InvalidInputError, InvalidOperation) as e:
            print(colorize(f"Error: {e}. Please try again.", "red"))

def format_currency(amount: Decimal) -> str:
    """Formats a Decimal as a currency string (e.g., $1,234.56)."""
    return f"${amount:,.2f}"

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- File Locking Context Manager ---
class FileLock:
    """
    A context manager for locking a file to prevent race conditions.
    Uses fcntl on Unix-like systems. A simpler check is used for Windows.
    """
    def __init__(self, lock_file_path):
        self.lock_file_path = lock_file_path
        self.lock_file = None
        # Conditionally import fcntl only on POSIX systems
        if os.name == 'posix':
            global fcntl
            import fcntl

    def __enter__(self):
        if os.name != 'posix':
            # Basic check for Windows: create a .lock file
            if os.path.exists(self.lock_file_path):
                raise FileLockError(f"Another process may be using the data file.")
            try:
                self.lock_file = open(self.lock_file_path, 'w')
            except IOError as e:
                raise FileLockError(f"Could not create lock file: {e}")
        else:
            # Robust locking for Unix-like systems
            self.lock_file = open(self.lock_file_path, 'w')
            try:
                fcntl.flock(self.lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except (IOError, BlockingIOError):
                raise FileLockError("Could not acquire lock on data file. Is another instance running?")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.lock_file:
            if os.name == 'posix':
                fcntl.flock(self.lock_file, fcntl.LOCK_UN)
            self.lock_file.close()
            # Clean up the lock file
            if os.path.exists(self.lock_file_path):
                try:
                    os.remove(self.lock_file_path)
                except OSError:
                    pass # Ignore errors on lock file removal
