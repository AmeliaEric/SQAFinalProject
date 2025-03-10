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
    def __init__(self, account_number, account_name, status, balance, transaction_plan, current_accounts_file, daily_transaction_file):
        self.account_number = account_number
        self.account_name = account_name
        self.status = status
        self.balance = balance
        self.transaction_plan = transaction_plan
        self.current_accounts_file = current_accounts_file
        self.daily_transaction_file = daily_transaction_file
       


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
        #print(f"Logged in as {username} in {session_type} mode.")


    def logout(self):
        """
        Logs the user out of the banking system.
        """
        if not self.is_logged_in:
            print("Error: No active session. Please login first.")
            return
        self.write_transaction_file()
        self.is_logged_in = False
        print("Session terminated.")


    def read_accounts_file(self):
        try:
            with open(self.current_accounts_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line.startswith("END_OF_FILE"):
                        break  # Stop reading when end marker is reached

                    # Extract fields based on fixed positions
                    account_number = line[:5].strip()
                    account_name = line[6:26].replace("_", " ").strip()  # Replace underscores with spaces
                    status = line[27].strip()
                    balance = float(line[29:38].strip())
                    transaction_plan = line[39:].strip()

                    account = Account(account_number, account_name, status, balance, transaction_plan, self.current_accounts_file, self.transaction_file)
                    self.accounts.append(account)
        except FileNotFoundError:
            print("Current user accounts file not found.")


    def write_transaction_file(self):
        # Write transaction logs to the daily transaction file
        with open(self.transaction_file, "a") as transaction_file:
            for transaction in self.transactions:
                transaction_file.write(transaction + "\n")
            transaction_file.write("00 00000 00000.00\n")  # End of transactions marker
        print("Transaction file updated.")

        # Update the current accounts file with the latest account details
        with open(self.current_accounts_file, "w") as accounts_file:
            for account in self.accounts:
                accounts_file.write(
                    f"{account.account_number:<5} {account.account_name:<20} {account.status} {account.balance:>9.2f} {account.transaction_plan}\n"
                )
            accounts_file.write("END_OF_FILE\n")  # End of accounts marker
        print("Accounts file updated.")


    def find_account(self, account_num, account_name=None):
        """
        Finds an account by account number and optionally by account name.
        Ignores underscores in the account name during comparison.
        Returns: The matching account, or None if not found.
        """
        for account in self.accounts:
            if account.account_number == account_num:
                if account_name:
                    # Strip underscores from both names before comparison
                    stored_name = account.account_name.replace("_", "").strip()
                    input_name = account_name.replace("_", "").strip()
                    if stored_name == input_name:
                        return account
                else:
                    return account
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
        self.max_deposit_limit = 1000.0
        self.max_paybill_limit = 2000.0


    def withdrawal(self, account_num, amount, account_name):
        """
        Processes a withdrawal transaction for a standard user.
        """
        if not self.is_logged_in:
            print("Error: No active session. Please login first.")
            return
        account = self.find_account(account_num)
        if account == None:
            print("Error: Account does not exist.")
            return
        if account.account_name != account_name:
            print("Error: Account holder name does not match account number.")
            return
        if account:
            if amount > self.max_withdrawal_limit:
                print(f"Error: Withdrawal amount exceeds the ${self.max_withdrawal_limit} limit.")
                return
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
                print(account.balance)
                account.balance -= amount
                print(account.balance)
                transaction = f"WITHDRAWAL {account_num} {amount:.2f}"
                self.transactions.append(transaction)
                print(account.balance)
                transaction_msg = account.select_transaction(1, amount)
                print(transaction_msg)


    def transfer(self, from_acc, to_acc, amount, account_name):
        """
        Processes a transfer transaction for a standard user.
        """
        if not self.is_logged_in:
            print("Error: No active session. Please login first.")
            return
        from_account = self.find_account(from_acc)
        if not from_account:
            print("Error: Invalid account number.")
            return
        if from_account.account_name != account_name:
            print("Error: Account holder name does not match account number.")
            return
        to_account = self.find_account(to_acc)
        if not to_account:
            print("Error: Invalid recipient account number.")
            return
        if from_account.status == "D":
            print("Error: Cannot transfer from a disabled account.")
            return
        if amount > self.max_transfer_limit:
            print(f"Error: Transfer amount exceeds the ${self.max_transfer_limit:.2f} limit.")
            return
        if from_account.balance < amount:
            print("Error: Insufficient funds.")
            return
        if from_account.account_number == to_account.account_number:
            print("Error: Cannot transfer to the same account.")
            return
        if amount < 0:
            print("Error: Transfer amount must be positive.")
            return
        if amount == 0:
            print("Error: Transfer amount must be greater than zero.")
            return
        from_account.balance -= amount
        to_account.balance += amount
        transaction = f"TRANSFER {from_acc} {to_acc} {amount:.2f}"
        self.transactions.append(transaction)
        print("Transfer successful.")


    def deposit(self, account_num, amount, account_name):
        """
        Processes a deposit transaction for a standard user.
        """
        if not self.is_logged_in:
            print("Error: No active session. Please login first.")
            return
        account = self.find_account(account_num)
        if not account:
            print("Error: Invalid account number.")
            return
        if account.account_name != account_name:
            print("Error: Account holder name does not match account number.")
            return
        if account.status == "D":
            print("Error: Cannot deposit into a disabled account.")
            return
        if amount > self.max_deposit_limit:
            print(f"Error: Deposit amount exceeds the ${self.max_deposit_limit:.2f} limit.")
            return
        if amount < 0:
            print("Error: Deposit amount must be positive.")
            return
        if amount == 0:
            print("Error: Deposit amount must be greater than zero.")
            return
        account.balance += amount
        transaction = f"DEPOSIT {account.account_number} {amount:.2f}"
        self.transactions.append(transaction)
        print("Deposit successful.")

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
        if account.status == "D":
            print("Error: Cannot pay a bill from a disabled account.")
            return
        if account.account_name != account_name:
            print("Error: Account holder name does not match account number.")
            return
        if account:
            if amount > self.max_paybill_limit:
                print("Payment amount exceeds limit.")
                return
            if account:
                transaction = f"03 {account_name:<20} {int(account_num):05d} {amount:08.2f} --"
                self.transactions.append(transaction)
                transaction_msg = account.select_transaction(3, amount)
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
        new_account = Account(account_num, account_name, "A", balance, transaction_plan, self.current_accounts_file, self.transaction_file)
        self.accounts.append(new_account)
        self.transactions.append(f"05 {account_name:<20} {int(account_num):05d} {balance:08.2f} {transaction_plan}")
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
            print("Error: Account holder name does not match account number.")
            return

        # Remove the account from the accounts list
        self.accounts.remove(account)

        # Log the transaction
        transaction = f"06 {account_name:<20} {int(account_num):05d} 0.00 DA"
        self.transactions.append(transaction)
        print(f"Deleted account {account_num} for {account_name}")

    def disable_account(self, account_name, account_num):
        """
        Disables an account for an admin.
        """
        if not self.is_logged_in or self.session_type != "admin":
            print("Error: Admin access required.")
            return

        # Find the account, ignoring underscores in the account name
        account = self.find_account(account_num, account_name)
        if not account:
            print("Error: Account does not exist or name mismatch.")
            return
        if account.status == "D":
            print("Error: Account already disabled.")
            return

        # Disable the account
        account.status = "D"

        # Log the transaction in the correct format
        transaction = f"04 {account_name:<20} {int(account_num):05d} {account.balance:08.2f} {account.transaction_plan}"
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

        # Find the account, ignoring underscores in the account name
        account = self.find_account(account_num, account_name)
        if not account:
            print("Error: Account does not exist.")
            return
        if account.status == "D":
            print("Error: Cannot change plan for a disabled account.")
            return

        if account.transaction_plan == "SP":
            account.transaction_plan = "NP"
            # Log the transaction with the correct format
            transaction = f"08 {account_name:<20} {int(account_num):05d} {account.balance:08.2f} {account.transaction_plan}"
            self.transactions.append(transaction)
            print(f"Changed plan for account {account_num} for {account_name}")
            print("Account plan updated successfully.")
        else:
            print("Error: Account is already on the non-student plan.")
            return
        

def main():
    if len(sys.argv) < 3:
        print("Usage: python TellerSystem.py <current_accounts_file> <transaction_file>")
        sys.exit(1)

    current_accounts_file = sys.argv[1]
    transaction_file = sys.argv[2]

    # Clear the transaction file before processing
    open(transaction_file, 'w').close()

    # Read all non-empty lines from input (provided via the .inp file)
    lines = [line.strip() for line in sys.stdin if line.strip() != '']
    if not lines:
        print("No input provided.")
        return
    
    index = 0
    while index < len(lines):  
        # Always print the welcome message and prompt
        print("Welcome to the banking system.")
        print("Enter session type: standard or admin.")

        # Ensure first command is 'login'
        if lines[index].lower() != "login":
            print("Error: No active session. Please login first.")
            with open(transaction_file, "w") as tf:
                tf.write("00 00000 00000.00")
            return
        
        index += 1
        if index >= len(lines):
            print("Error: Missing session type after login.")
            with open(transaction_file, "w") as tf:
                tf.write("00 00000 00000.00")
            return

        session_type = lines[index].lower()
        if session_type not in ["admin", "standard"]:
            print("Error: Invalid session type. Must be 'admin' or 'standard'.")
            return
        
        index += 1
        if session_type == "admin":
            user = Admin(current_accounts_file, transaction_file)
            user.login("admin", "admin")
        else:
            if index >= len(lines):
                print("Error: Missing account name for standard session.")
                with open(transaction_file, "w") as tf:
                    tf.write("00 00000 00000.00")
                return
            account_name = lines[index]
            index += 1
            user = StandardUser(current_accounts_file, transaction_file)
            user.login(account_name, "standard")

        # Process transactions until logout or end of file
        while index < len(lines) and lines[index].lower() != "logout":
            command = lines[index].lower()
            index += 1

            if command == "create" and session_type == "admin":
                if index + 3 >= len(lines):
                    print("Error: Insufficient arguments for create command.")
                    break  # Exit the loop on error
                account_name = lines[index]
                account_num = int(lines[index + 1])
                try:
                    balance = float(lines[index + 2])
                except ValueError:
                    print("Error: Invalid balance value.")
                    break  # Exit the loop on error
                transaction_plan = lines[index + 3].upper()
                if transaction_plan not in ["NP", "SP"]:
                    print("Error: Invalid transaction plan. Must be 'NP' or 'SP'.")
                    break  # Exit the loop on error
                index += 4
                user.create_account(account_name, account_num, balance, transaction_plan)

            elif command == "changeplan" and session_type == "admin":
                if index + 1 >= len(lines):
                    print("Error: Insufficient arguments for changeplan command.")
                    break  # Exit the loop on error
                account_name = lines[index]
                account_num = lines[index + 1]
                index += 2
                user.change_plan(account_name, account_num)

            elif command == "delete" and session_type == "admin":
                if index + 1 >= len(lines):
                    print("Error: Insufficient arguments for delete command.")
                    break  # Exit the loop on error
                account_name = lines[index]
                account_num = lines[index + 1]
                index += 2
                user.delete_account(account_name, account_num)

            elif command == "disable" and session_type == "admin":
                if index + 1 >= len(lines):
                    print("Error: Insufficient arguments for disable command.")
                    break  # Exit the loop on error
                account_name = lines[index]
                account_num = lines[index + 1]
                index += 2
                user.disable_account(account_name, account_num)

            elif session_type == "admin" and command in ["deposit", "withdraw", "transfer", "paybill"]:
                print("Error: Admin users are not permitted to perform transaction commands.")
                index += 2 if command in ["deposit", "withdraw"] else 3  # Skip extra arguments

            elif command == "deposit" and session_type == "standard":
                if index + 1 >= len(lines):
                    print("Error: Insufficient arguments for deposit command.")
                    break  # Exit the loop on error
                account_num = lines[index]
                index += 1
                try:
                    amount = float(lines[index])
                except ValueError:
                    print("Error: Invalid deposit amount format.")
                    break  # Exit the loop on error
                index += 1
                user.deposit(account_num, amount, account_name)

            elif command == "withdraw" and session_type == "standard":
                if index + 1 >= len(lines):
                    print("Error: Insufficient arguments for withdrawal command.")
                    break  # Exit the loop on error
                account_num = lines[index]
                index += 1
                try:
                    amount = float(lines[index])
                except ValueError:
                    print("Error: Invalid amount for withdrawal.")
                    break  # Exit the loop on error
                index += 1
                user.withdrawal(account_num, amount, account_name)

            elif command == "transfer" and session_type == "standard":
                if index + 2 >= len(lines):
                    print("Error: Insufficient arguments for transfer command.")
                    break  # Exit the loop on error
                from_acc = lines[index]
                to_acc = lines[index + 1]
                try:
                    amount = float(lines[index + 2])
                except ValueError:
                    print("Error: Invalid amount for transfer.")
                    break  # Exit the loop on error
                index += 3
                user.transfer(from_acc, to_acc, amount, account_name)
            
            elif command == "paybill" and session_type == "standard":
                if index + 3 >= len(lines):
                    print("Error: Insufficient arguments for paybill command.")
                    break  # Exit the loop on error
                account_name_paybill = lines[index]
                index += 1
                account_num = lines[index]
                index += 1
                try:
                    amount = float(lines[index])
                except ValueError:
                    print("Error: Invalid amount for paybill.")
                    break  # Exit the loop on error
                index += 1

                if index >= len(lines):
                    print("Error: Missing company name for paybill command.")
                    break  # Exit the loop on error

                company = lines[index]
                index += 1
                user.pay_bill(account_num, amount, company, account_name_paybill)

            elif command == "logout":
                user.logout()
                session_type = None
                user = None

            else:
                print(f"Unknown command: {command}")
                break  # Exit the loop on unknown command

        # Log out the user if the loop exits due to an error
        if user and user.is_logged_in:
            user.logout()

        # Skip remaining input for the current session
        while index < len(lines) and lines[index].lower() != "logout":
            index += 1

        # Move past "logout" and check for the next session
        if index < len(lines) and lines[index].lower() == "logout":
            index += 1

if __name__ == "__main__":
    main()