from calculations import black_scholes, get_expiration_date, get_strike_info
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import yfinance as yf

def generate_graph(ticker_symbol: str, option_type: str):
    ticker = yf.Ticker(ticker_symbol)
    S = ticker.fast_info['lastPrice']
    expiration_date = get_expiration_date(ticker)
    strike_info = get_strike_info(S, ticker, expiration_date, option_type)
    curr_price = strike_info[2]
    calculated_price = black_scholes(S, strike_info, expiration_date, option_type)
    
