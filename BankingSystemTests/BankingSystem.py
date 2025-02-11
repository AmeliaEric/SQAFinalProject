class BankSystem:
    def __init__(self):
        self.accounts = {}
        self.current_user = None
    
    def create_account(self, account_number, name, balance=0.0):
        if account_number in self.accounts:
            return "Account already exists."
        self.accounts[account_number] = {"name": name, "balance": balance, "status": "ACTIVE"}
        return "Account created successfully."
    
    def login(self, account_number):
        if account_number in self.accounts and self.accounts[account_number]["status"] == "ACTIVE":
            self.current_user = account_number
            return f"Welcome, {self.accounts[account_number]['name']}!"
        return "Invalid account or account disabled."
    
    def logout(self):
        self.current_user = None
        return "Logged out successfully."
    
    def get_balance(self):
        if not self.current_user:
            return "Error: No user logged in."
        return f"Balance: ${self.accounts[self.current_user]['balance']:.2f}"
    
    def deposit(self, amount):
        if not self.current_user:
            return "Error: No user logged in."
        if amount == 0:
            return "Error: Deposit amount must be greater than zero."
        if amount < 0:
            return "Error: Deposit amount must be positive."
        if amount > 1000.00:
            return "Error: Deposit amount exceeds the $1000.00 limit"
        self.accounts[self.current_user]['balance'] += amount
        return f"Deposit successful. New balance: ${self.accounts[self.current_user]['balance']:.2f}"
    
    def withdraw(self, amount):
        if not self.current_user:
            return "Error: No active session. Please login first."
        if self.accounts[self.current_user]['status'] == "DISABLED":
            return "Error: Cannot withdraw from a disabled account."
        if amount == 0:
            return "Error: Withdrawal amount must be greater than zero."
        if amount < 0:
            return "Error: Withdrawal amount must be positive."
        if amount > 1000.00:
            return "Error: Withdrawal amount exceeds the $1000.00 limit"
        if self.accounts[self.current_user]['balance'] < amount:
            return "Error: Insufficient funds."
        self.accounts[self.current_user]['balance'] -= amount
        return f"Withdrawal successful. New balance: ${self.accounts[self.current_user]['balance']:.2f}"
    
    def transfer(self, target_account, amount):
        if not self.current_user:
            return "Error: No active session. Please login first."
        if target_account not in self.accounts:
            return "Error: Invalid recipient account number."
        if self.accounts[self.current_user]['status'] == "DISABLED":
            return "Error: Cannot transfer from a disabled account."
        if target_account == self.current_user:
            return "Error: Cannot transfer to the same account."
        if amount == 0:
            return "Error: Transfer amount must be greater than zero."
        if amount < 0:
            return "Error: Transfer amount must be positive."
        if amount > 1000.00:
            return "Error: Transfer amount exceeds the $1000.00 limit"
        if self.accounts[self.current_user]['balance'] < amount:
            return "Error: Insufficient funds."
        
        self.accounts[self.current_user]['balance'] -= amount
        self.accounts[target_account]['balance'] += amount
        return f"Transfer successful. New balance: ${self.accounts[self.current_user]['balance']:.2f}"
    
# Finish filling in Deposit, and double check withdrawal fits all perameters!
# Example usage:
bank = BankSystem()
bank.create_account("12345", "John Doe", 1000)
bank.create_account("67890", "Jane Doe", 500)
print(bank.login("12345"))
print(bank.deposit(200))
print(bank.withdraw(100))
print(bank.transfer("67890", 300))
print(bank.logout())
