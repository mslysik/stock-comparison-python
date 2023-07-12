# This program uses the yfinance library to collect stock data based on user input, creates summary tables, and
# uses pyplot to create accompanying graphs.

# import libraries
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Function that checks to see if a given stock symbol appears in the Yahoo Finance API.
def validate_stock_name(symbol):
    stock = yf.Ticker(symbol)
    try:
        data = stock.history(period="1d")
        return not data.empty
    except ValueError:
        return False

# Function takes stock ticker symbol and date range as parameters, storing the stock's
# historical data if the 
def fetch_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    try:
        data = stock.history(start=start_date, end=end_date)
        return data, stock.info
    except ValueError:
        print(f"No data found for stock symbol: {symbol}. Please re-enter.")
        return pd.DataFrame(), {}


# Function creates a graph of the stock prices over time
def plot_stock_data(stock_data):
    for symbol, data in stock_data.items():
        plt.plot(data.index, data['Close'], label=symbol)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Comparison')
    plt.legend()
    plt.show()

# Funtion creates a summary of key stock information, using N/A for missing values
def generate_summary_report(stock_info):
    print("\nStock Summary:")
    for symbol, info in stock_info.items():
        essential_info = {
            'Symbol': info.get('symbol', 'N/A'),
            'Company Name': info.get('longName', 'N/A'),
            'Sector': info.get('sector', 'N/A'),
            'Industry': info.get('industry', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            'Previous Close': info.get('previousClose', 'N/A'),
            'Open': info.get('open', 'N/A'),
            'Day Range': f"{info.get('dayLow', 'N/A')} - {info.get('dayHigh', 'N/A')}",
            '52-Week Range': f"{info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}",
            'Volume': info.get('volume', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A'),
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Dividend Rate': info.get('dividendRate', 'N/A'),
            'Dividend Yield': info.get('dividendYield', 'N/A'),
            'Beta': info.get('beta', 'N/A')
        }
        print(f"\nStock: {symbol}")
        for key, value in essential_info.items():
            print(f"{key:<17} {value}")
    print()


# Get valid stock names
stock_symbols = []
valid_symbols = []
while True:
    # Get comma separated ticker symbols from user
    stock_input = input("Enter stock symbols (comma-separated): ")
    # Split stock symbols by comma, remove whitespace, and make all uppercase.
    # Store in stock_symbols list
    stock_symbols = [symbol.strip().upper() for symbol in stock_input.split(',')]
    # Use validate_stock_name function to see if stocks appear in yfinance and stores valid stocks in list.
    # Loop continues until all stocks in the list are vaild, prompting user to re-enter otherwise.
    if stock_symbols:
        valid_symbols = []
        for symbol in stock_symbols:
            if validate_stock_name(symbol):
                valid_symbols.append(symbol)
            else:
                print(f"Invalid stock symbol: {symbol}. Please re-enter.")
                break
        if len(valid_symbols) == len(stock_symbols):
            break
    else:
        print("Please enter at least one stock symbol.")

# Get valid start date
while True:
    # user enters start date
    start_date = input("Enter start date (YYYY-MM-DD): ")
    try:
        # Transform start date into datetime object in Year, Month, Day format.
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        # Proceed if date is not in the future, otherwise ask for valid date. 
        if start_date <= datetime.now().date():
            break
        else:
            print("Invalid input - start date cannot be in the future. Please re-enter.")
    except ValueError:
        print("Invalid start date format. Please re-enter.")

# Get valid end date
while True:
    end_date = input("Enter end date (YYYY-MM-DD): ")
    try:
        # Transform end date into datetime object in Year, Month, Day format.
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        # Proceed if date is not before the start date or in the future.
        if end_date >= start_date and end_date <= datetime.now().date():
            break
        else:
            print("Invalid input - end date cannot be before the start date or in the future. Please re-enter.")
    except ValueError:
        print("Invalid end date format. Please re-enter.")

# Fetch stock data and summary info
stock_data = {}
stock_info = {}
# Iterate through each stock symbol, storing the data and info into dictonaries
for symbol in valid_symbols:
    data, info = fetch_stock_data(symbol, start_date, end_date)
    if not data.empty:
        stock_data[symbol] = data
        stock_info.update({symbol: info})

# Generate stock summary report using generate_summary_report function
if stock_info:
    generate_summary_report(stock_info)

# Plot stock data
if stock_data:
    plot_stock_data(stock_data)
else:
    print("No valid data found for any stock symbols. Exiting the program.")
