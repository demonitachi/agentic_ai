import gradio as gr
from accounts import Account, get_share_price

# Instantiate a single user account for demonstration
user_account = Account("demo_user")

def create_account():
    global user_account
    user_account = Account("demo_user")
    return "Account created."

def deposit(amount):
    try:
        amt = float(amount)
        user_account.deposit_funds(amt)
        return f"Deposited ${amt:.2f}"
    except Exception as e:
        return str(e)

def withdraw(amount):
    try:
        amt = float(amount)
        user_account.withdraw_funds(amt)
        return f"Withdrew ${amt:.2f}"
    except Exception as e:
        return str(e)

def buy_share(symbol, quantity):
    try:
        qty = int(quantity)
        user_account.buy_shares(symbol.upper(), qty)
        return f"Bought {qty} shares of {symbol.upper()}"
    except Exception as e:
        return str(e)

def sell_share(symbol, quantity):
    try:
        qty = int(quantity)
        user_account.sell_shares(symbol.upper(), qty)
        return f"Sold {qty} shares of {symbol.upper()}"
    except Exception as e:
        return str(e)

def get_portfolio_value():
    total_value = user_account.get_portfolio_value()
    total_value_str = f"${total_value:.2f}"
    profit_loss = user_account.get_profit_or_loss()
    profit_loss_str = f"${profit_loss:.2f}"
    return total_value_str, profit_loss_str

def get_holdings():
    holdings = user_account.get_holdings()
    if holdings:
        return "\n".join([f"{symbol}: {qty} shares" for symbol, qty in holdings.items()])
    else:
        return "No holdings."

def get_transaction_history():
    transactions = user_account.get_transaction_history()
    if not transactions:
        return "No transactions made."
    lines = []
    for t in transactions:
        timestamp = t['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        t_type = t['type'].capitalize()
        symbol = t['symbol'] if t['symbol'] else ''
        qty = t['quantity'] if t['quantity'] else ''
        amount = t['amount']
        line = f"{timestamp} | {t_type} | {symbol} {qty} | ${amount:.2f}"
        lines.append(line)
    return "\n".join(lines)

custom_css = """
#btn_create { background-color: #4CAF50; color: white; }
#btn_deposit { background-color: #2196F3; color: white; }
#btn_withdraw { background-color: #f44336; color: white; }
#btn_buy { background-color: #FF9800; color: white; }
#btn_sell { background-color: #009688; color: white; }
#btn_portfolio { background-color: #3F51B5; color: white; }
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("<h1 style='color:blue;'>Trading Simulation Account Demo</h1>")
    
    with gr.Row():
        btn_create = gr.Button("Create Account", elem_id="btn_create")
        deposit_input = gr.Number(label="Deposit Amount ($)", value=0, minimum=0)
        btn_deposit = gr.Button("Deposit", elem_id="btn_deposit")
        withdraw_input = gr.Number(label="Withdraw Amount ($)", value=0, minimum=0)
        btn_withdraw = gr.Button("Withdraw", elem_id="btn_withdraw")
        
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Buy Shares")
            symbol_buy = gr.Textbox(label="Symbol", placeholder="e.g., AAPL")
            qty_buy = gr.Number(label="Quantity", value=1, minimum=1)
            btn_buy = gr.Button("Buy", elem_id="btn_buy")
            
        with gr.Column():
            gr.Markdown("### Sell Shares")
            symbol_sell = gr.Textbox(label="Symbol", placeholder="e.g., AAPL")
            qty_sell = gr.Number(label="Quantity", value=1, minimum=1)
            btn_sell = gr.Button("Sell", elem_id="btn_sell")
            
    with gr.Row():
        # Removed 'period' and fixed click mapping
        btn_portfolio = gr.Button("Get Portfolio Value / Profit", elem_id="btn_portfolio")
        
    with gr.Row():
        holdings_output = gr.Textbox(label="Holdings", lines=4)
        transactions_output = gr.Textbox(label="Transaction History", lines=8)

    # Correct way to link the button click to outputs
    btn_portfolio.click(
        fn=get_portfolio_value, 
        inputs=[], 
        outputs=[holdings_output, transactions_output]
    )

    def refresh_holdings():
        return get_holdings()

    def refresh_transactions():
        return get_transaction_history()

    btn_create.click(create_account)
    btn_deposit.click(deposit, inputs=deposit_input, outputs=None)
    btn_withdraw.click(withdraw, inputs=withdraw_input, outputs=None)
    btn_buy.click(buy_share, inputs=[symbol_buy, qty_buy], outputs=None)
    btn_sell.click(sell_share, inputs=[symbol_sell, qty_sell], outputs=None)
    gr.Button("Refresh Holdings").click(refresh_holdings, outputs=holdings_output)
    gr.Button("Refresh Transactions").click(refresh_transactions, outputs=transactions_output)

demo.launch()