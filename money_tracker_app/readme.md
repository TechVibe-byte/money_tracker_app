# 💰 Personal Money Tracker 💰

A feature-rich, command-line tool to help you take control of your personal finances. Track your expenses, manage debts, and get a clear overview of your financial health, all from the comfort of your terminal!

## ✨ Features

*   **📊 Comprehensive Tracking**: Log everything from your daily coffee ☕ to monthly loan payments 🏦.
*   **🗂️ Categorized Expenses**: Assign categories to your daily expenses for better budgeting and analysis.
*   **💳 Credit Management**: Keep a close eye on your credit card spending.
*   **🤝 Debt & Loan Management**: Track money you've borrowed or lent, and manage their status (e.g., Pending, Paid).
*   **🗓️ Timeline View**: A beautiful, date-wise timeline of all your transactions.
*   **✏️ Full CRUD Functionality**: Easily **C**reate, **R**ead, **E**dit, and **D**elete any record.
*   **🧾 Financial Summary**: Generate a neat table summarizing your total expenses and loans.
*   **💾 Local Data Storage**: All your data is securely stored on your local machine in a `money_tracker_data.json` file. You are in control of your data.
*   **🎨 Rich CLI Experience**: A modern and colorful user interface powered by the `rich` library.
*   **🔄 Automatic Data Migration**: Seamlessly updates older data formats to the latest version.

## 🚀 Getting Started

### Prerequisites

1.  You need to have Python 3 installed on your system.
2.  You need to install the required package.

### Installation & Running

1.  **Clone the repository or download the files.**
2.  **Install dependencies:** Open your terminal in the project directory and run:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application:**
    ```bash
    python money_tracker.py
    ```

## 📝 Menu Options

Here's a breakdown of what you can do:

1.  **Add Daily Expense**: Record a new daily expense and assign it to a category.
2.  **View Daily Expenses**: See a timeline of all your daily expenses. You can also edit or delete from this view.
3.  **Add Credit Expense**: Log an expense made on a credit card.
4.  **View Credit Expenses**: See a timeline of your credit expenses. You can edit or delete them.
5.  **Add Borrowed Money**: Record money that you have borrowed from someone.
6.  **View Borrowed Records**: See who you owe money to and the status. You can edit or delete records.
7.  **Add Lent Money**: Record money that you have lent to someone.
8.  **View Lent Records**: See who owes you money and the status. You can edit or delete records.
9.  **Add Monthly Loan**: Add a loan record, like a car or home loan.
10. **View Monthly Loans**: View your loan records.
11. **Generate Totals**: Get a summary of your total daily expenses, credit bills, and loans.
12. **Exit**: Save all changes and exit the application.

## 📁 Data Storage

All your financial data is stored locally in a file named `money_tracker_data.json` in the same directory as the script.

## 🏷️ Expense Categories

The application comes with a pre-defined list of categories for your daily expenses:

- Transport 🚗
- Groceries 🛒
- Personal 🧑
- Food 🍔
- Health 💊
- Tax 🧾
- Housing 🏠
- Gifts & Charity 🎁
- Entertainment & Subscriptions 🎬
- Another Subscription 🔁
- Education Fee 🎓
- Pet Maintenance 🐾
- Gadgets & Electronics 💻
- Plantation 🌱
- Other 🤷