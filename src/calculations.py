import yfinance as yf
import numpy as np
from scipy.stats import norm
import math
import pandas
import matplotlib as pt
import datetime as dt

def get_expiration_date(ticker) -> str:
    expiration_dates = ticker.options
    expiration_date = ""
    while expiration_date not in expiration_dates:
        for date in expiration_dates:
            print(date)
        expiration_date = str(input("Enter expiration date (YYYY-MM-DD): "))
        if expiration_date not in expiration_dates:
            print("Invalid Expiration Date.")
    return expiration_date

def get_strike_price(curr_price, ticker, 
                     expiration_date, 
                     option_type="call") -> list:
    opt_chain = ticker.option_chain(expiration_date)
    options = opt_chain.calls[["strike", "lastPrice", "impliedVolatility"]]
    if option_type == "put": 
        options = opt_chain.puts[["strike", "lastPrice", "impliedVolatility"]]
    
    print(options["strike"], "\n")
    print("Current Price: ", curr_price, "\n")

    K = -1.0
    while float(K) not in options["strike"].values:
        K = input("Enter Strike Price: ")
        if float(K) not in options["strike"].values:
            print("Invalid Strike Price.")

    implied_volatility = options.loc[options["strike"] == float(K), "impliedVolatility"].values[0]

    return [float(K), implied_volatility]

def get_time_to_expiration(expiration_date) -> float:
    curr_date = dt.date.today()
    T = dt.datetime.strptime(expiration_date, "%Y-%m-%d").date()
    T -= curr_date
    return float(T.days / 365)

def get_rf(time_to_expiry) -> float:
    if time_to_expiry <= 0.25:
        ticker_symbol = "^IRX"
    elif time_to_expiry <= 3.0:
        ticker_symbol = "^FVX"
    else:
        ticker_symbol = "^TNX"
    ticker = yf.Ticker(ticker_symbol)
    return ticker.fast_info["lastPrice"] / 100.0

def black_scholes(ticker_symbol, option_type="call"):

    """ S : current stock price
        K : option strike price
        T : time to expiration date (years)
        r : risk-free interest rate as decimal
        sigma : implied volatility as decimal
        option_type : 'call' or 'put' """

    ticker = yf.Ticker(ticker_symbol)
    S = ticker.fast_info['lastPrice']
    expiration_date = get_expiration_date(ticker)
    strike_info = get_strike_price(S, ticker, expiration_date, option_type)
    K = strike_info[0]
    sigma = strike_info[1]
    T = get_time_to_expiration(expiration_date)
    r = get_rf(T)
    d1 = math.log(S / K) + ((r + (math.pow(sigma, 2) / 2)) * T)
    d1 /= (sigma * math.sqrt(T))
    d2 = d1 - (sigma * math.sqrt(T))

    if option_type == "call":
        return round((S * norm.cdf(d1)) - (K * math.pow(math.e, (-1 * r * T)) * norm.cdf(d2)), 2)
    else:
        return round((K * math.pow(math.e, -1 * r * T) * norm.cdf(-1 * d2)) - (S * norm.cdf(-d1)), 2)

    

if __name__ == "__main__":
    print(black_scholes("AAPL"))
    
    
    
