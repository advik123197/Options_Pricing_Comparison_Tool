import yfinance as yf
from graph import generate_graph

def tickerExists(ticker_symbol) -> bool:
    try:
        ticker = yf.Ticker(ticker_symbol)
        price = ticker.fast_info["lastPrice"]
        return price is not None
    except:
        return False

if __name__ == "__main__":
    ticker_symbol = ""
    while not tickerExists(ticker_symbol):
        ticker_symbol = str(input("Enter Ticker: "))
        if not tickerExists(ticker_symbol):
            print("Invalid Ticker.")
    while True:
        choice = input("Enter option type (call: 0, put: 1): ")
        try:
            choice = int(choice)
            break
        except:
            print("Invalid Choice.")
        if choice != 1 or choice != 0:
            print("Invalid Choice.")
    if choice == 0:
        generate_graph(ticker_symbol, "call")
    else:
        generate_graph(ticker_symbol, "put")
    

