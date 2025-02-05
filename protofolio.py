import yfinance as yf
import json

# File to store portfolio data
PORTFOLIO_FILE = "portfolio.json"

# Load portfolio from file
def load_portfolio():
    try:
        with open(PORTFOLIO_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save portfolio to file
def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, "w") as file:
        json.dump(portfolio, file, indent=4)

# Add a stock to the portfolio
def add_stock(symbol, quantity, purchase_price):
    portfolio = load_portfolio()
    portfolio[symbol] = {
        "quantity": quantity,
        "purchase_price": purchase_price
    }
    save_portfolio(portfolio)
    print(f"Added {symbol} to portfolio.")

# Remove a stock from the portfolio
def remove_stock(symbol):
    portfolio = load_portfolio()
    if symbol in portfolio:
        del portfolio[symbol]
        save_portfolio(portfolio)
        print(f"Removed {symbol} from portfolio.")
    else:
        print("Stock not found in portfolio.")

# Get real-time stock prices
def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    history = stock.history(period="1d")
    if not history.empty:
        return history["Close"].iloc[-1]
    else:
        print(f"Could not retrieve price for {symbol}.")
        return 0

# Track portfolio performance
def track_performance():
    portfolio = load_portfolio()
    total_value = 0
    print("\nPortfolio Performance:")
    print("-----------------------------------")
    for symbol, data in portfolio.items():
        current_price = get_stock_price(symbol)
        quantity = data["quantity"]
        purchase_price = data["purchase_price"]
        value = quantity * current_price
        total_value += value
        print(f"{symbol}: {quantity} shares | Bought at ${purchase_price} | Current Price: ${current_price:.2f} | Value: ${value:.2f}")
    print(f"\nTotal Portfolio Value: ${total_value:.2f}")

# Main menu
def main():
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Track Performance")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            symbol = input("Enter stock symbol: ").upper()
            try:
                quantity = int(input("Enter quantity: "))
                purchase_price = float(input("Enter purchase price: "))
                add_stock(symbol, quantity, purchase_price)
            except ValueError:
                print("Invalid input. Please enter valid numbers for quantity and purchase price.")
        elif choice == "2":
            symbol = input("Enter stock symbol to remove: ").upper()
            remove_stock(symbol)
        elif choice == "3":
            track_performance()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()