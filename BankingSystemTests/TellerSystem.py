# This program simulates a banking system front end that processes transactions.
# Input files: "current_accounts_file.txt"
# Output file: daily_transaction_file.txt
# The program processes a stream of transactions and writes the results to the output file.
import sys
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
        Stores transaction in a structured format for logging.
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
            return False


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
    def __init__(self, current_accounts_file, transaction_file):
        self.username = None
        self.session_type = None
        self.is_logged_in = False
        self.accounts = []
        self.transactions = []
        self.current_accounts_file = current_accounts_file
        self.transaction_file = transaction_file

    def login(self, username, session_type):
        """
        Logs the user into the banking system.
        """
        if self.is_logged_in:
            print("Already logged in. Please logout first.")
            return
        if not username or not session_type:
            print("Error: Username and session type are required.")
            return
        self.username = username
        self.session_type = session_type
        self.is_logged_in = True
        self.read_accounts_file()
        print(f"Logged in as {username} in {session_type} mode.")


    class User:
        def logout(self):
            if not self.is_logged_in:
                print("Error: No active session. Please login first.")
            return
            self.write_transaction_file()
            self.transactions.clear()  # Ensure transactions are cleared before logout
            self.is_logged_in = False
            print("Session terminated.")
            print("Session terminated. No further transactions are allowed.")




    def read_accounts_file(self):
        """
        Reads the current accounts file and loads accounts for the user.
        """
        try:
            with open(self.current_accounts_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line.startswith("END_OF_FILE"):
                        break  # Stop reading when end marker is reached
                    
                    # Extract fields based on fixed positions
                    account_number = line[:5].strip()
                    account_name = line[6:26].strip()
                    status = line[27].strip()
                    balance = float(line[29:38].strip())

                    account = Account(account_number, account_name, status, balance, "NP")
                    self.accounts.append(account)
        except FileNotFoundError:
            print("Current user accounts file not found.")


    def write_transaction_file(self):
        """
        Writes the transaction history to the daily transaction file and updates the current accounts file.
        """
        # Writing to daily transaction file
        with open(self.transaction_file, "a") as transaction_file:
            for transaction in self.transactions:
                transaction_code, account_name, account_number, amount, misc = transaction.split()
                # Formatting each field properly
                formatted_transaction = (
                    f"{transaction_code:<2}"
                    f"{account_name:<20}"
                    f"{int(account_number):05d}"
                    f"{float(amount):08f}.00"
                    f"{misc:2}"
                )
                transaction_file.write(formatted_transaction + "\n")
            # Append the end-of-session transaction
            transaction_file.write("00" + " " * 20 + "00000" + "00000000.00" + "  \n")
        print("Transaction file updated.")

        # Writing to current accounts file
        with open(self.current_accounts_file, "w") as accounts_file:
            for account in self.accounts:
                accounts_file.write(f"{account.account_number:<5} {account.account_name:<20} {account.status} {account.balance:>9.2f} {account.transaction_plan}\n")
            accounts_file.write("END_OF_FILE\n")
        print("Accounts file updated.")


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


class StandardUser(User):
    """
    Represents a standard user with transaction limits.
    Attributes:
        max_withdrawal_limit (float): Maximum withdrawal limit for standard users.
        max_transfer_limit (float): Maximum transfer limit for standard users.
        max_paybill_limit (float): Maximum pay bill limit for standard users.
    """
    def __init__(self, current_accounts_file, transaction_file):
        super().__init__(current_accounts_file, transaction_file)
        self.max_withdrawal_limit = 1000.0
        self.max_transfer_limit = 1000.0
        self.max_paybill_limit = 2000.0

    def withdrawal(self, account_num, amount, account_name):
        """
        Processes a withdrawal transaction for a standard user.
        """
        if not self.is_logged_in:
            print("Error: No active session. Please login first.")
            return
        account = self.find_account(account_num)
        if not account:
            print("Error: Account does not exist.")
            return
        if account.account_name != account_name:
            print("Account name for the account number given: " + account.account_name)
            print("Account name inputed: " + account_name)
            print("Error: Account holder name does not match account number.")
            return
        if account:
            if amount > self.max_withdrawal_limit:
                print(f"Error: Withdrawal amount exceeds the ${self.max_withdrawal_limit} limit.")
                return
            account = self.find_account(account_num)
            if account.status == "D":
                print("Error: Cannot withdraw from a disabled account.")
                return
            if account.balance < amount:
                print("Error: Insufficient funds.")
                return
            if amount <= 0:
                print("Error: Withdrawal amount must be positive.")
                return
            if account:
                transaction = f"01 {account_name:<20} {int(account_num):05d} {amount:08.2f} --"
                self.transactions.append(transaction)
                transaction_msg = account.select_transaction(1, amount)
                print(transaction_msg)

    def transfer(self, from_acc, to_acc, amount, account_name):
        """
        Processes a transfer transaction for a standard user.
        """
        if not self.is_logged_in:
            print("Error: No active session. Please login first.")
            return
        account = self.find_account(from_acc)
        if not account:
            print("Error: Account does not exist.")
            return
        if account.account_name != account_name:
            print("Account name for the account number given: " + account.account_name)
            print("Account name inputed: " + account_name)
            print("Error: Account holder name does not match account number.")
            return
        if account:
            if amount > self.max_transfer_limit:
                print("Error: Transfer amount exceeds ${self.max_transfer_limit} limit.")
                return
            from_account = self.find_account(from_acc)
            to_account = self.find_account(to_acc)
            if from_account.status == "D":
                print("Error: Cannot transfer from a disabled account.")
                return
            if from_account.balance < amount:
                print("Error: Insufficient funds.")
                return
            if from_account.account_number == to_account.account_number:
                print("Error: Cannot transfer to the same account.")
                return
            if amount == 0:
                print("Error: Transfer amount must be greater than zero.")
                return
            if amount < 0:
                print("Error: Transfer amount must be positive.")
                return
            if from_account and to_account:
                transaction = f"02 {account_name:<20} {int(from_acc):05d} {amount:08.2f} --"
                self.transactions.append(transaction)
                transaction_msg = from_account.select_transaction(2, amount)
                print(transaction_msg)

    def pay_bill(self, account_num, amount, company, account_name):
        """
        Processes a bill payment transaction for a standard user.
        """
        if not self.is_logged_in:
            print("Error: No active session. Please login first.")
            return
        account = self.find_account(account_num)
        if not account:
            print("Error: Account does not exist.")
            return
        if account.account_name != account_name:
            print("Account name for the account number given: " + account.account_name)
            print("Account name inputed: " + account_name)
            print("Error: Account holder name does not match account number.")
            return
        if account:
            if amount > self.max_paybill_limit:
                print("Payment amount exceeds limit.")
                return
            account = self.find_account(account_num)
            if account:
                transaction = f"03 {account_name:<20} {int(account_num):05d} {amount:08.2f} --"
                self.transactions.append(transaction)
                transaction_msg = account.select_transaction(3, amount)
                print(transaction_msg)

    def deposit(self, account_num, amount, account_name):
        """
        Processes a deposit transaction for a standard user.
        """
        if not self.is_logged_in:
            print("Error: No active session. Please login first.")
            return
        account = self.find_account(account_num)
        if not account:
            print("Error: Account does not exist.")
            return
        if account.account_name != account_name:
            print("Account name for the account number given: " + account.account_name)
            print("Account name inputed: " + account_name)
            print("Error: Account holder name does not match account number.")
            return
        if account:
            if account.status == "D":
                print("Error: Cannot deposit into a disabled account.")
                return
            if amount == 0:
                print("Error: Deposit amount must be greater than zero.")
                return
            if amount < 0:
                print("Error: Deposit amount must be positive.")
                return
            if account:
                transaction = f"04 {account_name:<20} {int(account_num):05d} {amount:08.2f} --"
                self.transactions.append(transaction)
                transaction_msg = account.select_transaction(4, amount)
                print(transaction_msg)


class Admin(User):
    """
    Represents an admin user with full account management privileges.
    Methods:
        create_account: Creates a new account.
        delete_account: Deletes an existing account.
        disable_account: Disables an existing account.
        change_plan: Changes the transaction plan of an account.
    """
    def __init__(self, current_accounts_file, transaction_file):
        super().__init__(current_accounts_file, transaction_file)

    def create_account(self, account_name, account_num, balance, transaction_plan):
        """
        Creates a new account for an admin.
        """
        if not self.is_logged_in or self.session_type != "admin":
            print("Error: This transaction requires admin access.")
            return
        if len(account_name) > 20:
            print("Error: Account holder name must be 20 characters or less.")
            return
        if balance < 0:
            print("Error: Initial balance must be at least $0.00.")
            return
        if balance > 99999.99:
            print("Error: Initial balance cannot exceed $99999.99.")
            return
        account = self.find_account(account_num)
        if account != None:
            print("Error: Account number already in use.")
            return
        new_account = Account(account_num, account_name, "A", balance, transaction_plan)
        self.accounts.append(new_account)
        transaction = f"05 {account_name:<20} {int(account_num):05d} {balance:08.2f} CA"
        self.transactions.append(transaction)
        print(f"Created account for {account_name} with account number {account_num} and balance ${balance}")

    def delete_account(self, account_name, account_num):
        """
        Deletes an account for an admin.
        """
        if not self.is_logged_in or self.session_type != "admin":
            print("Error: This transaction requires admin access.")
            return
        if not account_name:
            print("Error: Account holder name cannot be empty.")
            return
        if not account_num:
            print("Error: Account number cannot be empty.")
            return 
        account = self.find_account(account_num)
        if not account:
            print("Error: Account does not exist.")
            return
        if account.account_name != account_name:
            print("Account name for the account number given: " + account.account_name)
            print("Account name inputed: " + account_name)
            print("Error: Account holder name does not match account number.")
            return
        if account:
            self.accounts.remove(account)
            transaction = f"06 {account_name:<20} {int(account_num):05d} 0.00 DA"
            self.transactions.append(transaction)
            print(f"Deleted account {account_num} for {account_name}")

    def disable_account(self, account_name, account_num):
        """
        Disables an account for an admin.
        """
        if not self.is_logged_in or self.session_type != "admin":
            print("Error: This transaction requires admin access.")
            return
        if not account_name:
            print("Error: Account holder name cannot be empty.")
            return
        if not account_num:
            print("Error: Account number cannot be empty.")
            return 
        account = self.find_account(account_num)
        if not account:
            print("Error: Account does not exist.")
            return
        if account.account_name != account_name:
            print("Error: Account holder name does not match account number.")
            return
        if account.status == "D":
            print("Error: Account already disabled.")
            return
        if account:
            account.select_maintenance("disable")
            transaction = f"07 {account_name:<20} {int(account_num):05d} 0.00 DA"
            self.transactions.append(transaction)
            print(f"Disabled account {account_num} for {account_name}")

    def change_plan(self, account_name, account_num):
        """
        Changes the transaction plan for an account.
        """
        if not self.is_logged_in or self.session_type != "admin":
            print("Error: This transaction requires admin access.")
            return
        if not account_name:
            print("Error: Account holder name cannot be empty.")
            return
        if not account_num:
            print("Error: Account number cannot be empty.")
            return 
        account = self.find_account(account_num)
        if not account:
            print("Error: Account does not exist.")
            return
        if account.account_name != account_name:
            print("Error: Account holder name does not match account number.")
            return
        if account.status == "D":
            print("Error: Cannot change plan for a disabled account.")
            return
        if account.transaction_plan == "NP":
            print("Account is already on the non-student plan.")
            return
        if account:
            account.select_maintenance("change_plan")
            transaction = f"08 {account_name:<20} {int(account_num):05d} 0.00 CP"
            self.transactions.append(transaction)
            print(f"Changed plan for account {account_num} for {account_name}")
            

# Extra Test Functions
#def valid_deposit():
#    print("=== Test: Valid Deposit ===")
#    user = StandardUser("current_accounts_file.txt", "daily_transaction_file.txt")
#    user.login("john_doe", "standard")
#    user.logout()
#    print("\n")

#def withdrawal_insufficient_funds():
#    print("=== Test: Withdrawal with Insufficient Funds ===")
#    user = StandardUser("current_accounts_file.txt", "daily_transaction_file.txt")
#    user.login("john_doe", "standard")
#    # Assuming account 12345 has less than 10000 available
#    user.withdrawal("12345", 10000, "JohnDoe_____________")
#    user.logout()
#    print("\n")

#def transfer_same_account():
#    print("=== Test: Transfer to Same Account ===")
#    user = StandardUser("current_accounts_file.txt", "daily_transaction_file.txt")
#    user.login("john_doe", "standard")
#    user.transfer("12345", "12345", 100, "JohnDoe_____________")
#    user.logout()
#    print("\n")

#def delete_account_wrong_name():
#    print("=== Test: Delete Account with Mismatched Account Name ===")
#    admin = Admin("current_accounts_file.txt", "daily_transaction_file.txt")
#    admin.login("admin_user", "admin")
#    # Provide an incorrect account name to trigger an error
#    admin.delete_account("WrongName", "12345")
#    admin.logout()
#    print("\n")

#def disable_account_wrong_name():
#    print("=== Test: Disable Account with Mismatched Account Name ===")
#    admin = Admin("current_accounts_file.txt", "daily_transaction_file.txt")
#    admin.login("admin_user", "admin")
#    # Provide an incorrect account name to trigger an error
#    admin.disable_account("WrongName", "12345")
#    admin.logout()
#    print("\n")

#def valid_transfer():
#    print("=== Test: Valid Transfer ===")
#    user = StandardUser("current_accounts_file.txt", "daily_transaction_file.txt")
#    user.login("john_doe", "standard")
#    user.transfer("12345", "67890", 300, "JohnDoe_____________")
#    user.logout()
#    print("\n")

#def run_tests():
#    valid_deposit()
#    withdrawal_insufficient_funds()
#    transfer_same_account()
#    delete_account_wrong_name()
#    disable_account_wrong_name()
#    valid_transfer()


# Main program
#if __name__ == "__main__":
#    """
#    The main program simulates a banking system with user and admin functionalities.
#    It allows users to perform transactions like withdrawal, transfer, bill payment,
#    and deposits. Admins can create, delete, disable accounts and change transaction plans.
#    Input: User actions (login, transactions)
#    Output: Transaction records written to daily_transaction_file.txt
#    """

#    # Example
#    #standard_user = StandardUser("current_accounts_file.txt", "daily_transaction_file.txt")
#    #standard_user.login("JohnDoe_____________", "standard")
#    #standard_user.withdrawal("12345", 200, "JohnDoe_____________")
#    #standard_user.transfer("12345", "67890", 200, "JohnDoe_____________")
#    #standard_user.pay_bill("12345", 100, "EC", "JohnDoe_____________")
#    #standard_user.deposit("12345", 600, "JohnDoe_____________")
#    #standard_user.pay_bill("12345", 800, "EC", "JohnDoe_____________")
#    #standard_user.logout()

#    #admin = Admin("current_accounts_file.txt", "daily_transaction_file.txt")
#    #admin.login("admin_user", "admin")
#    #admin.create_account("EishaRizvi__________", "05452", 900, "NP")
#    #admin.delete_account("JaneDoe_____________" , "67890")
#    #admin.change_plan("JohnDoe_____________", "12345")
#    #admin.disable_account("JohnDoe_____________", "12345")
#    #admin.disable_account("EishaRizvi__________", "12345")
#    #admin.change_plan("JaneDoe_____________" , "67890")
#    #admin.logout()

#    #print("\nExtra Tests: \n")
#    #run_tests()
