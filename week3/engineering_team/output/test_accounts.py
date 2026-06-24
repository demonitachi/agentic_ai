import unittest
from accounts import Account, get_share_price

class TestAccounts(unittest.TestCase):

    def setUp(self):
        self.account = Account("test_user")

    def test_initial_account_state(self):
        self.assertEqual(self.account.get_cash_balance(), 0.0)
        self.assertEqual(self.account.get_holdings(), {})
        self.assertEqual(self.account.total_deposited_funds, 0.0)

    def test_deposit_funds(self):
        self.account.deposit_funds(100.0)
        self.assertEqual(self.account.get_cash_balance(), 100.0)
        self.assertEqual(self.account.total_deposited_funds, 100.0)

    def test_deposit_funds_negative(self):
        with self.assertRaises(ValueError):
            self.account.deposit_funds(-50.0)

    def test_withdraw_funds(self):
        self.account.deposit_funds(100.0)
        self.account.withdraw_funds(50.0)
        self.assertEqual(self.account.get_cash_balance(), 50.0)

    def test_withdraw_funds_negative(self):
        with self.assertRaises(ValueError):
            self.account.withdraw_funds(-50.0)

    def test_withdraw_funds_insufficient(self):
        with self.assertRaises(ValueError):
            self.account.withdraw_funds(50.0)

    def test_buy_shares(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})
        self.assertEqual(self.account.get_cash_balance(), 700.0)

    def test_buy_shares_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', -1)

    def test_buy_shares_insufficient_funds(self):
        self.account.deposit_funds(100.0)
        with self.assertRaises(ValueError):
            self.account.buy_shares('TSLA', 1)

    def test_sell_shares(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 2)
        self.account.sell_shares('AAPL', 1)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 1})
        self.assertEqual(self.account.get_cash_balance(), 850.0)

    def test_sell_shares_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', -1)

    def test_sell_shares_not_enough(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 1)
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 2)

    def test_get_holdings(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 3)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 3})

    def test_get_portfolio_value(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.get_portfolio_value(), 300.0)

    def test_get_cash_balance(self):
        self.account.deposit_funds(200.0)
        self.assertEqual(self.account.get_cash_balance(), 200.0)

    def test_get_total_account_value(self):
        self.account.deposit_funds(500.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.get_total_account_value(), 800.0)

    def test_get_profit_or_loss(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 2)
        self.account.sell_shares('AAPL', 1)
        self.assertEqual(self.account.get_profit_or_loss(), -200.0)

    def test_transaction_history(self):
        self.account.deposit_funds(500.0)
        self.account.withdraw_funds(100.0)
        self.assertEqual(len(self.account.get_transaction_history()), 2)

if __name__ == '__main__':
    unittest.main()