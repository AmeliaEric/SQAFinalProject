class BankSystem:
    def __init__(self):
        self.accounts = {}
        self.current_user = None
        self.is_admin = False
    
    def create_account(self, account_number, name, balance=0.0, plan="SP"):
        if account_number in self.accounts:
            return "Error: Account number already in use."
        self.accounts[account_number] = {"name": name, "balance": balance, "status": "ACTIVE", "plan": plan}
        return "Account created successfully."
    
    def login(self, account_number, is_admin=False):
        if account_number in self.accounts and self.accounts[account_number]["status"] == "ACTIVE":
            self.current_user = account_number
            self.is_admin = is_admin
            return f"Welcome, {self.accounts[account_number]['name']}!"
        return "Error: Invalid account or account disabled."
    
    def logout(self):
        self.current_user = None
        self.is_admin = False
        return "Logged out successfully."
    
    def get_balance(self):
        if not self.current_user:
            return "Error: No user logged in."
        return f"Balance: ${self.accounts[self.current_user]['balance']:.2f}"
    
    def deposit(self, amount):
        if not self.current_user:
            return "Error: No user logged in."
        if amount <= 0:
            return "Error: Deposit amount must be positive."
        if amount > 1000.00:
            return "Error: Deposit amount exceeds the $1000.00 limit."
        self.accounts[self.current_user]['balance'] += amount
        return f"Deposit successful. New balance: ${self.accounts[self.current_user]['balance']:.2f}"
    
    def withdraw(self, amount):
        if not self.current_user:
            return "Error: No active session. Please login first."
        if self.accounts[self.current_user]['status'] == "DISABLED":
            return "Error: Cannot withdraw from a disabled account."
        if amount <= 0:
            return "Error: Withdrawal amount must be positive."
        if amount > 1000.00:
            return "Error: Withdrawal amount exceeds the $1000.00 limit."
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
        if amount <= 0:
            return "Error: Transfer amount must be positive."
        if amount > 1000.00:
            return "Error: Transfer amount exceeds the $1000.00 limit."
        if self.accounts[self.current_user]['balance'] < amount:
            return "Error: Insufficient funds."
        
        self.accounts[self.current_user]['balance'] -= amount
        self.accounts[target_account]['balance'] += amount
        return f"Transfer successful. New balance: ${self.accounts[self.current_user]['balance']:.2f}"
    
    def change_plan(self, account_number):
        if not self.is_admin:
            return "Error: Only admins can change account plans."
        if account_number not in self.accounts:
            return "Error: Account does not exist."
        if self.accounts[account_number]["status"] == "DISABLED":
            return "Error: Cannot change plan for a disabled account."
        
        current_plan = self.accounts[account_number]["plan"]
        new_plan = "NP" if current_plan == "SP" else "SP"
        self.accounts[account_number]["plan"] = new_plan
        return f"Account {account_number} plan changed to {new_plan}."
    
    def pay_bill(self, company, amount):
        allowed_companies = {"EC": "The Bright Light Electric Company", "CQ": "Credit Card Company Q", "FI": "Fast Internet, Inc."}
        if not self.current_user:
            return "Error: No active session. Please login first."
        if self.accounts[self.current_user]["status"] == "DISABLED":
            return "Error: Cannot pay bills from a disabled account."
        if company not in allowed_companies:
            return "Error: Invalid company."
        if amount <= 0:
            return "Error: Bill amount must be positive."
        if amount > 2000.00:
            return "Error: Bill amount exceeds the $2000.00 limit."
        if self.accounts[self.current_user]["balance"] < amount:
            return "Error: Insufficient funds."
        
        self.accounts[self.current_user]["balance"] -= amount
        return f"Bill payment of ${amount:.2f} to {allowed_companies[company]} successful. New balance: ${self.accounts[self.current_user]['balance']:.2f}"

# Example usage:
bank = BankSystem()
bank.create_account("12345", "John Doe", 1000)
bank.create_account("67890", "Jane Doe", 500)
print(bank.login("12345"))
print(bank.deposit(200))
print(bank.withdraw(100))
print(bank.transfer("67890", 300))
print(bank.pay_bill("EC", 150))
print(bank.logout())