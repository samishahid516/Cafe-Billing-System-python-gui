# ☕ Smart Cafe Billing System

A modern, desktop-based graphical user interface (GUI) application for cafe billing, developed using **Python's Tkinter**. This system integrates **AI-inspired decision rules** to automatically apply discounts and suggest related products based on customer orders.

## 🚀 Features

-   **Modern UI:** Sleek, dark-themed interface built with the `Tkinter` library.
-   **Intelligent Discount Rules:** Automatically applies discounts based on:
    -   Total order amount (Big Spender Reward).
    -   Bulk quantities (Multi-Item/Bulk Discount).
-   **Smart Suggestions:** Uses AI-inspired logic to suggest items that pair well with the customer's current selection.
-   **Input Validation:** Ensures data integrity for customer names, contact numbers (11 digits), and quantities.
-   **Professional Receipt Generation:** Generates a structured digital receipt in the application and saves a timestamped text file.
-   **Live Clock:** Displays real-time date and time.
-   **Quick Actions:** Features to clear the form or exit with confirmation.

## 🛠️ Built With

-   **Language:** [Python 3.x](https://www.python.org/)
-   **GUI Framework:** [Tkinter](https://docs.python.org/3/library/tkinter.html)
-   **Styling:** Custom themed widgets and color palette.

## 📸 Screenshots

### 🖥️ Dashboard View
<p align="center">
  <img src="https://github.com/user-attachments/assets/0c87db9f-0631-484f-98f8-366688bcb02b" alt="Application Dashboard" width="800">
</p>

### 📄 Receipt Generated
<p align="center">
  <img src="https://github.com/user-attachments/assets/d8593afc-3685-464f-afe9-2584e952b256" alt="Receipt Generation" width="800">
</p>

## 📦 Project Structure

```bash
├── Smart Billing System.py    # Main application source code
├── README.md                  # Project documentation
├── screenshots/               # Folder containing application images (backup)
└── receipts/                  # (Auto-generated) Folder for saved bill records
```

## ⚙️ How to Run

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/samishahid516/Cafe-Billing-System-python-gui.git
    cd Cafe-Billing-System-python-gui
    ```

2.  **Prerequisites:**
    -   Python 3.x installed on your machine.
    -   Tkinter is usually included with Python standard installations.

3.  **Launch the App:**
    ```bash
    python "Smart Billing System.py"
    ```

## 🤖 AI Logic Implemented

-   **Dynamic Discounts:**
    -   `> 1000 Rs`: 15% Discount
    -   `> 500 Rs`: 10% Discount
    -   `Qty ≥ 5`: 8% Discount
-   **Association Suggestions:** If a user selects "Coffee", the system suggests "Cake Slice or Sandwich".

---
*Developed for Python Lab 10 by **Sami***
