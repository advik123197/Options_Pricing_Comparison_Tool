from calculations import black_scholes, get_expiration_date, get_strike_info
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import yfinance as yf
import datetime as dt

def generate_graph(ticker_symbol: str, option_type: str):
    ticker = yf.Ticker(ticker_symbol)
    S = ticker.fast_info["lastPrice"]
    expiration_date = get_expiration_date(ticker)
    strike_info = get_strike_info(S, ticker, expiration_date, option_type)

    time_stamps = []
    market_prices = []
    calculated_prices = []

    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(10, 5))

    (line_market,) = ax.plot(
        [],
        [],
        label="Market Price",
        color="green",
        linestyle="-",
        marker=".",
        linewidth=2,
    )

    (line_bs,) = ax.plot(
        [],
        [],
        label="Black Scholes Price",
        color="red",
        linestyle="-",
        marker=".",
        linewidth=2,
    )

    ax.set_title(
        f"Real-Time Options Pricing Tracker for {ticker_symbol} {option_type.upper()} at ${strike_info[0]} (Exp: {expiration_date})"
    )
    ax.set_xlabel("Time (HH:MM:SS)")
    ax.set_ylabel("Price ($)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax.legend(loc="upper left")

    def update(frame):
        new_ticker = yf.Ticker(ticker_symbol)
        S = new_ticker.fast_info["lastPrice"]

        opt_chain = new_ticker.option_chain(expiration_date)
        if option_type == "call":
            options = opt_chain.calls
        else:
            options = opt_chain.puts

        option_row = options[options["strike"] == strike_info[0]].iloc[0]
        market_price = option_row["lastPrice"]
        sigma = option_row["impliedVolatility"]

        bs_price = black_scholes(S, strike_info, sigma, expiration_date, option_type)

        now = dt.datetime.now()
        time_stamps.append(now)
        market_prices.append(market_price)
        calculated_prices.append(bs_price)

        line_market.set_data(time_stamps, market_prices)
        line_bs.set_data(time_stamps, calculated_prices)

        ax.relim()
        ax.autoscale_view()

        print(
            f"[{now.strftime('%H:%M:%S')}] Stock: ${S:.2f} | Market Option: ${market_price:.2f} | BS: ${bs_price:.2f}"
        )

        return line_market, line_bs

    animation = FuncAnimation(fig, update, interval=30000, cache_frame_data=False)

    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()




    

