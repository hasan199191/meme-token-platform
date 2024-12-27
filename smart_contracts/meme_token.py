class MemeToken:
    def __init__(self, name, symbol, initial_supply):
        self.name = name
        self.symbol = symbol
        self.total_supply = initial_supply
        self.balances = {}

    def mint(self, recipient, amount):
        if recipient in self.balances:
            self.balances[recipient] += amount
        else:
            self.balances[recipient] = amount
        self.total_supply += amount

    def transfer(self, sender, recipient, amount):
        if sender not in self.balances or self.balances[sender] < amount:
            raise ValueError("Insufficient balance")
        self.balances[sender] -= amount
        if recipient in self.balances:
            self.balances[recipient] += amount
        else:
            self.balances[recipient] = amount

    def balance_of(self, account):
        return self.balances.get(account, 0)