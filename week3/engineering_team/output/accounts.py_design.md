```markdown
# Module: accounts.py

## Description
This module implements a simple account management system for a trading simulation platform. It allows a user to create an account, deposit and withdraw funds, buy and sell shares, track portfolio holdings and transaction history, and calculate profit/loss. The system enforces constraints to prevent invalid operations such as overdrawing the cash balance or selling more shares than owned.

The module also includes a provided test implementation of `get_share_price(symbol)` which returns fixed prices for the symbols AAPL, TSLA, and GOOGL.

---

## Classes and Functions

### Function: `get_share_price(symbol: str) -> float`
- **Description**: Returns the current price of a share for the given symbol.
- **Test Implementation**: Fixed prices:
  - AAPL: 150.0
  - TSLA: 700.0
  - GOOGL: 2500.0
- **Parameters**:
  - `symbol`: Stock ticker symbol (string).
- **Returns**: Current price as a float.
- **Usage**: Used internally by `Account` methods to determine share prices.

---

### Class: `Account`

Represents a trading simulation account that tracks cash balance, holdings of shares, transactions, and provides portfolio valuation and profit/loss reporting.

#### Initialization:
```python
__init__(self, username: str)
```
- Creates a new account associated with `username`.
- Initializes cash balance at zero.
- Initializes empty holdings and transactions list.
- Tracks initial deposit for profit/loss calculations.

---

#### Methods:

1. **create_account (constructor)**  
   - See `__init__`

2. **deposit_funds**
   ```python
   deposit_funds(self, amount: float) -> None
   ```
   - Adds funds to the cash balance.
   - Updates the record of total deposited funds for profit/loss baseline.
   - Parameters:
     - `amount`: positive float representing the deposit amount.
   - Raises `ValueError` for non-positive amount.

3. **withdraw_funds**
   ```python
   withdraw_funds(self, amount: float) -> None
   ```
   - Withdraws funds from cash balance.
   - Validates that withdrawal does not cause negative cash balance.
   - Parameters:
     - `amount`: positive float representing the withdrawal amount.
   - Raises `ValueError` if withdrawal amount causes negative balance or is not positive.

4. **buy_shares**
   ```python
   buy_shares(self, symbol: str, quantity: int) -> None
   ```
   - Records a purchase of `quantity` shares of `symbol`.
   - Checks that the user has enough cash to afford the purchase at current share price.
   - Deducts total cost from cash balance.
   - Updates share holdings by increasing quantity.
   - Records transaction.
   - Parameters:
     - `symbol`: string ticker.
     - `quantity`: positive integer number of shares to buy.
   - Raises `ValueError` if quantity is non-positive or insufficient funds.

5. **sell_shares**
   ```python
   sell_shares(self, symbol: str, quantity: int) -> None
   ```
   - Records a sale of `quantity` shares of `symbol`.
   - Checks that user has enough shares to sell.
   - Adds proceeds to cash balance.
   - Updates share holdings by decreasing quantity.
   - Records transaction.
   - Parameters:
     - `symbol`: string ticker.
     - `quantity`: positive integer number of shares to sell.
   - Raises `ValueError` if quantity is non-positive or insufficient shares.

6. **get_holdings**
   ```python
   get_holdings(self) -> dict[str, int]
   ```
   - Returns current share holdings as a dictionary:
     `{'AAPL': 10, 'TSLA': 5, ...}`
   - Holdings with zero quantity shares are excluded.

7. **get_portfolio_value**
   ```python
   get_portfolio_value(self) -> float
   ```
   - Calculates total current market value of all shares owned.
   - Uses `get_share_price(symbol)` for pricing.
   - Returns float total portfolio value.

8. **get_cash_balance**
   ```python
   get_cash_balance(self) -> float
   ```
   - Returns current cash balance as float.

9. **get_total_account_value**
   ```python
   get_total_account_value(self) -> float
   ```
   - Returns combined cash balance + portfolio value.

10. **get_profit_or_loss**
    ```python
    get_profit_or_loss(self) -> float
    ```
    - Calculates profit or loss compared to initial total deposited funds.
    - Computed as `(total_account_value - total_deposited_funds)`
    - Returns float P/L value.

11. **get_transaction_history**
    ```python
    get_transaction_history(self) -> list[dict]
    ```
    - Returns a list of all transactions made by the user.
    - Transaction dict records:
      - `type`: 'deposit', 'withdrawal', 'buy', or 'sell'
      - `symbol`: for buy/sell transactions; None otherwise
      - `quantity`: for buy/sell transactions; None otherwise
      - `amount`: cash amount involved
      - `price_per_share`: price at time of transaction for buy/sell; None otherwise
      - `timestamp`: datetime object recording time of transaction

---

## Data Structures Inside Account

- **cash_balance** (`float`): Current available cash.
- **holdings** (`dict[str, int]`): Maps symbol to number of shares owned.
- **transactions** (`list[dict]`): Chronological list of transactions.
- **total_deposited_funds** (`float`): Sum of all deposits made into account (used as investment baseline).

---

## Notes

- All monetary values handled as floats; consider rounding as needed for display/UI.
- Quantity of shares is always an integer, must be > 0 for buy/sell operations.
- The class is designed to be self-contained; no external database or persistent storage.
- Since the module is backend focused, colorful UI is not part of this module but can be implemented on top of these APIs.
- The module can be imported and the `Account` class instantiated for unit testing or UI integration.

---

# Summary

The module `accounts.py` exposes:

- The function `get_share_price(symbol: str) -> float`
- The class `Account` with:
  - Constructor: `__init__(username: str)`
  - User actions: `deposit_funds()`, `withdraw_funds()`, `buy_shares()`, `sell_shares()`
  - Reporting: `get_holdings()`, `get_portfolio_value()`, `get_cash_balance()`, `get_total_account_value()`, `get_profit_or_loss()`, `get_transaction_history()`

This design cleanly encapsulates trading account management with all checks and reporting required by the specification.
```
