# Smart Invoice Generator

A Python-based terminal application for generating and managing **product** and **service** invoices with tax, discounts, client tracking, and persistent storage.

---

## Features

### Invoice Management
- Create **Product** or **Service** invoices
- Auto-generate invoice IDs (e.g., `INV-XXXX`)
- Add multiple line items (product/service-based)
- Calculate **tax**, **discount**, and **final totals**
- Support for **Paid/Unpaid** status tracking
- View past invoices and search by ID or client

### Financial Accuracy
- Uses `Decimal` for precision in currency calculations
- Supports:
  - Subtotal
  - Tax
  - Discount
  - Total
- Dynamic due date calculation

### Client Management
- Create clients with validated name, email, and phone
- Auto-generate unique client IDs

### Data Storage
- Invoices are saved to `invoices.json` with auto-backups
- Robust error handling for corrupt files
- File locking system to prevent race conditions

### Reports
- View revenue summary:
  - Total invoices
  - Paid vs. unpaid
  - Total revenue & pending payments

### Command-Line Interface
- Menu-based CLI interface
- Colorized outputs for success, warnings, errors
- Type validation for safe inputs

### Testing & Extensibility
- Modular OOP design with:
  - Inheritance, abstraction, polymorphism
  - Class/static methods, dunder methods, property decorators
- Unit tests with `unittest`

---

##  Project Structure

---

Smart-Invoice-Generator/
│
├── main.py # CLI interface
├── client.py # Client model and validation
├── item.py # Item model with pricing logic
├── invoice.py # Abstract base class for all invoices
├── invoice_types.py # ProductInvoice & ServiceInvoice classes
├── storage.py # JSON file save/load with locking
├── utils.py # Helpers: currency, color, file lock
│
├── data/
   └── invoices.json # Saved invoices (auto-created)
│
├──log/
   └──actions.log
│
└── README.md   

---

## Getting Started

### 1. Clone the Repository

git clone https://github.com/your-username/Smart-Invoice-Generator.git

cd Smart-Invoice-Generator

### 2. Run the App

python main.py

### 3.Run Tests

python -m unittest discover -s tests

## Dependencies

Built with Python 3.7+.

No external dependencies required.

**Uses only Python standard libraries:**

  + decimal, datetime, json, os, uuid, re, unittest

## Future Ideas
+ Export to PDF using reportlab

+ Multi-currency support

+ Add GUI with Tkinter or PyQt

+ Email invoice to clients

+ REST API for remote access

Author
Ubaid Khan
A developer on a Python learning journey, building practical, real-world tools with clean code and strong OOP principles.
 
