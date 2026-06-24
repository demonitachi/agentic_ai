# accounts.py

import datetime

def get_share_price(symbol: str) -> float:
    """Return a fixed share price for testing purposes."""
    prices = {
        'AAPL': 150.0,
        'TSLA': 700.0,
        'GOOGL': 2500.0
    }
    return prices.get(symbol.upper(), 0.0)

class Account:
    def __init__(self, username: str):
        self.username = username
        self.cash_balance = 0.0
        self.holdings = {}  # symbol -> number of shares
        self.transactions = []  # list of transaction dicts
        self.total_deposited_funds = 0.0

    def deposit_funds(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.cash_balance += amount
        self.total_deposited_funds += amount
        self.transactions.append({
            'type': 'deposit',
            'symbol': None,
            'quantity': None,
            'amount': amount,
            'price_per_share': None,
            'timestamp': datetime.datetime.now()
        })

    def withdraw_funds(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.cash_balance:
            raise ValueError("Insufficient funds to withdraw.")
        self.cash_balance -= amount
        self.transactions.append({
            'type': 'withdrawal',
            'symbol': None,
            'quantity': None,
            'amount': amount,
            'price_per_share': None,
            'timestamp': datetime.datetime.now()
        })

    def buy_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        price = get_share_price(symbol)
        total_cost = price * quantity
        if total_cost > self.cash_balance:
            raise ValueError("Insufficient cash to buy shares.")
        self.cash_balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append({
            'type': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'amount': total_cost,
            'price_per_share': price,
            'timestamp': datetime.datetime.now()
        })

    def sell_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        current_shares = self.holdings.get(symbol, 0)
        if quantity > current_shares:
            raise ValueError("Not enough shares to sell.")
        price = get_share_price(symbol)
        total_proceeds = price * quantity
        self.holdings[symbol] = current_shares - quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.cash_balance += total_proceeds
        self.transactions.append({
            'type': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'amount': total_proceeds,
            'price_per_share': price,
            'timestamp': datetime.datetime.now()
        })

    def get_holdings(self) -> dict:
        # Return a copy without zero quantity holdings
        return {symbol: qty for symbol, qty in self.holdings.items() if qty > 0}

    def get_portfolio_value(self) -> float:
        total = 0.0
        for symbol, qty in self.holdings.items():
            price = get_share_price(symbol)
            total += price * qty
        return total

    def get_cash_balance(self) -> float:
        return self.cash_balance

    def get_total_account_value(self) -> float:
        return self.cash_balance + self.get_portfolio_value()

    def get_profit_or_loss(self) -> float:
        return self.get_total_account_value() - self.total_deposited_funds

    def get_transaction_history(self) -> list:
        return self.transactions.copy()