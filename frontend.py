# This program simulates a banking system front end that processes transactions.
# Input files: current_user_accounts_file.txt
# Output file: daily_transaction_file.txt
# The program processes a stream of transactions and writes the results to the output file.

class Account:
    """
    Represents a bank account for an individual user with details such as account number,
    balance, and transaction plan.
    Attributes:
        account_number (str): Unique identifier for the account.
        account_name (str): Account holder's name.
        status (str): Account status ("A" for active, "D" for disabled).
        balance (float): Current balance in the account.
        transaction_plan (str): Transaction plan type ("SP" for student, "NP" for non-student).
        current_accounts_file (str): Current accounts file.
        daily_transaction_file (str): Daily transactions file.
    """
    def __init__(self, account_number, account_name, status, balance, transaction_plan):
        self.account_number = account_number
        self.account_name = account_name
        self.status = status
        self.balance = balance
        self.transaction_plan = transaction_plan
        self.current_accounts_file = "current_accounts_file.txt"
        self.daily_transaction_file = "daily_transaction_file.txt"

    def select_transaction(self, transaction_type, amount):
        """
        Processes a user transaction (withdrawal, transfer, pay bill, or deposit).
        Returns: Transaction result message.
        """
        if self.validate_transaction(transaction_type, amount):
            if transaction_type == 1:  # Withdrawal
                self.balance -= amount
                return f"Withdrew ${amount} from account {self.account_number}"
            elif transaction_type == 2:  # Transfer
                self.balance -= amount
                return f"Transferred ${amount} from account {self.account_number}"
            elif transaction_type == 3:  # Pay bill
                self.balance -= amount
                return f"Paid ${amount} from account {self.account_number}"
            elif transaction_type == 4:  # Deposit
                self.balance += amount
                return f"Deposited ${amount} into account {self.account_number}"
        else:
            return "Transaction failed due to validation error."

    def select_maintenance(self, option):
        """
        Performs maintenance tasks (disable, delete, change plan) on the account.
        Returns: Maintenance result message.
        """
        if option == "disable":
            self.status = "D"
            return f"Account {self.account_number} disabled."
        elif option == "delete":
            return f"Account {self.account_number} deleted."
        elif option == "change_plan":
            return f"Account {self.account_number} plan changed."
        else:
            return "Invalid maintenance option."

    def validate_transaction(self, transaction_code, amount):
        """
        Validates the transaction based on account status and transaction limits.
        Returns: Whether the transaction is valid.
        """
        if self.status == "D":
            print(f"Account {self.account_number} is disabled. Transaction cannot proceed.")
            return False

        if transaction_code == 1:  # Withdrawal
            if self.balance >= amount:
                return True
            else:
                print("Insufficient balance for withdrawal.")
                return False
        elif transaction_code == 2:  # Transfer
            if self.balance >= amount:
                return True
            else:
                print("Insufficient balance for transfer.")
                return False
        elif transaction_code == 3:  # Pay bill
            if self.balance >= amount:
                return True
            else:
                print("Insufficient balance for bill payment.")
                return False
        elif transaction_code == 4:  # Deposit
            return True  # No constraint on deposits
        else:
            return False  # Invalid transaction code


class User:
    """
    Represents a generic user in the banking system.
    Attributes:
        username (str): The user's login username.
        session_type (str): The user's session type ("admin" or "standard").
        is_logged_in (bool): Whether the user is logged in.
        accounts (list): List of accounts associated with the user.
        transactions (list): List of completed transactions during the session.
    """
    def __init__(self):
        self.username = None
        self.session_type = None
        self.is_logged_in = False
        self.accounts = []
        self.transactions = []

    def login(self, username, session_type):
        """
        Logs the user into the banking system.
        """
        if self.is_logged_in:
            print("Already logged in. Please logout first.")
            return
        self.username = username
        self.session_type = session_type
        self.is_logged_in = True
        self.read_accounts_file()
        print(f"Logged in as {username} in {session_type} mode.")

    def logout(self):
        """
        Logs the user out of the banking system.
        """
        if not self.is_logged_in:
            print("Not logged in.")
            return
        self.write_transaction_file()
        self.is_logged_in = False
        print("Logged out.")

    def read_accounts_file(self):
        """
        Reads the current accounts file and loads accounts for the user.
        """
        try:
            with open(self.current_accounts_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    account_data = line.strip().split(',')
                    account = Account(*account_data)
                    self.accounts.append(account)
        except FileNotFoundError:
            print("Current user accounts file not found.")

    def write_transaction_file(self):
        """
        Writes the transaction history to the daily transaction file.
        """
        with open("daily_transaction_file.txt", "w") as file:
            for transaction in self.transactions:
                file.write(transaction + "\n")
            file.write("00_END_OF_FILE_________00000_00000.00__\n")
        print("Transaction file written.")


class StandardUser(User):
    """
    Represents a standard user with transaction limits.
    Attributes:
        max_withdrawal_limit (float): Maximum withdrawal limit for standard users.
        max_transfer_limit (float): Maximum transfer limit for standard users.
        max_paybill_limit (float): Maximum pay bill limit for standard users.
    """
    def __init__(self):
        super().__init__()
        self.max_withdrawal_limit = 1000.0
        self.max_transfer_limit = 1000.0
        self.max_paybill_limit = 2000.0

    def withdrawal(self, account_num, amount):
        """
        Processes a withdrawal transaction for a standard user.
        """
        if not self.is_logged_in:
            print("Error: No active session. Please login first.")
            return
        if amount > self.max_withdrawal_limit:
            print("Error: Withdrawal amount exceeds the $1000.00 limit.")
            return
        account = self.find_account(account_num)
        if account:
            transaction_msg = account.select_transaction(1, amount)
            self.transactions.append(transaction_msg)
            print(transaction_msg)

    def transfer(self, from_acc, to_acc, amount):
        """
        Processes a transfer transaction for a standard user.
        """
        if not self.is_logged_in:
            print("Not logged in.")
            return
        if amount > self.max_transfer_limit:
            print("Transfer amount exceeds limit.")
            return
        from_account = self.find_account(from_acc)
        to_account = self.find_account(to_acc)
        if from_account and to_account:
            transaction_msg = from_account.select_transaction(2, amount)
            self.transactions.append(transaction_msg)
            print(transaction_msg)

    def pay_bill(self, account_num, amount, company):
        """
        Processes a bill payment transaction for a standard user.
        """
        if not self.is_logged_in:
            print("Not logged in.")
            return
        if amount > self.max_paybill_limit:
            print("Payment amount exceeds limit.")
            return
        account = self.find_account(account_num)
        if account:
            transaction_msg = account.select_transaction(3, amount)
            self.transactions.append(transaction_msg)
            print(transaction_msg)

    def deposit(self, account_num, amount):
        """
        Processes a deposit transaction for a standard user.
        """
        if not self.is_logged_in:
            print("Not logged in.")
            return
        account = self.find_account(account_num)
        if account:
            transaction_msg = account.select_transaction(4, amount)
            self.transactions.append(transaction_msg)
            print(transaction_msg)

    def find_account(self, account_num):
        """
        Finds an account by account number.
        Returns: The matching account, or None if not found.
        """
        for account in self.accounts:
            if account.account_number == account_num:
                return account
        print(f"Account {account_num} not found.")
        return None


class Admin(User):
    """
    Represents an admin user with full account management privileges.
    Methods:
        create_account: Creates a new account.
        delete_account: Deletes an existing account.
        disable_account: Disables an existing account.
        change_plan: Changes the transaction plan of an account.
    """
    def __init__(self):
        super().__init__()

    def create_account(self, account_name, account_num, balance, transaction_plan):
        """
        Creates a new account for an admin.
        """
        if not self.is_logged_in or self.session_type != "admin":
            print("Not logged in as admin.")
            return
        if len(account_name) > 20:
            print("Account holder name exceeds 20 characters.")
            return
        if balance > 99999.99:
            print("Balance exceeds maximum limit.")
            return
        new_account = Account(account_num, account_name, "A", balance, transaction_plan)
        self.accounts.append(new_account)
        self.transactions.append(f"Created account for {account_name} with account number {account_num} and balance ${balance}")
        print(f"Created account for {account_name} with account number {account_num} and balance ${balance}")

    def delete_account(self, account_name, account_num):
        """
        Deletes an account for an admin.
        """
        if not self.is_logged_in or self.session_type != "admin":
            print("Not logged in as admin.")
            return
        account = self.find_account(account_num)
        if account:
            self.accounts.remove(account)
            self.transactions.append(f"Deleted account {account_num} for {account_name}")
            print(f"Deleted account {account_num} for {account_name}")

    def disable_account(self, account_name, account_num):
        """
        Disables an account for an admin.
        """
        if not self.is_logged_in or self.session_type != "admin":
            print("Not logged in as admin.")
            return
        account = self.find_account(account_num)
        if account:
            account.select_maintenance("disable")
            self.transactions.append(f"Disabled account {account_num} for {account_name}")
            print(f"Disabled account {account_num} for {account_name}")

    def change_plan(self, account_name, account_num):
        """
        Changes the transaction plan for an account.
        """
        if not self.is_logged_in or self.session_type != "admin":
            print("Not logged in as admin.")
            return
        account = self.find_account(account_num)
        if account:
            account.select_maintenance("change_plan")
            self.transactions.append(f"Changed plan for account {account_num} for {account_name}")
            print(f"Changed plan for account {account_num} for {account_name}")


# Main program
if __name__ == "__main__":
    """
    The main program simulates a banking system with user and admin functionalities.
    It allows users to perform transactions like withdrawal, transfer, bill payment,
    and deposits. Admins can create, delete, disable accounts and change transaction plans.
    Input: User actions (login, transactions)
    Output: Transaction records written to daily_transaction_file.txt
    """
    user = User()
    standard_user = StandardUser()
    admin = Admin()

    # Example transaction stream
    user.login("john_doe", "standard")
    standard_user.withdrawal("12345", 200)
    standard_user.transfer("12345", "67890", 300)
    standard_user.pay_bill("12345", 100, "EC")
    standard_user.deposit("12345", 500)
    user.logout()

    user.login("admin_user", "admin")
    admin.create_account("Jane Doe", "54321", 1000, "NP")
    admin.delete_account("Jane Doe", "54321")
    admin.disable_account("John Doe", "12345")
    admin.change_plan("John Doe", "12345")
    user.logout()
