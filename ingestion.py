import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pyarrow



stocks = [
    "AAPL", "MSFT", "NVDA", "TSLA", "META", "GOOGL", "AMZN",
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "SBIN.NS", "ITC.NS",
    "^NSEI", "^BSESN", "^GSPC", "^IXIC",
    "BTC-USD", "ETH-USD",
    "JPM", "BAC", "WMT", "COST", "DIS",
    "NFLX", "AMD", "INTC", "ORCL", "CRM",
    "ADBE", "IBM", "KO", "PEP", "MCD"
]

# Historical data
historical_df = yf.download(
    stocks,
    period="5y",
    auto_adjust=True,
    group_by="ticker"
)




historical_df.to_parquet(
    "C:/Users/Anmol/Music/Lakehouse/historical/historical_data.parquet",
    engine="pyarrow"
)




print("Historical data loaded.")
print(historical_df)

while True:
    try:
        live_df = yf.download(
            stocks,
            period="1d",
            interval="1m",
            auto_adjust=True,
            progress=False,
            group_by="ticker"
        )

        print(f"\nLIVE UPDATE : {datetime.now()}")
        records = []
        for symbol in stocks:
            try:
                ticker_df = live_df[symbol].copy()

                # Removing rows with missing Close (because these records/rows were giving null in all values and vol = 0)
                ticker_df = ticker_df.dropna(subset=["Close"])

                if ticker_df.empty:      #in case yfinance doesnt send stock data
                    print(f"{symbol}: No valid data")
                    continue

                # Remove placeholder rows:
                # Volume = 0 and OHLC all equal:-
                valid_rows = ticker_df[
                    ~(                     # ~ selects everything except rows mentioned in ()
                        (ticker_df["Volume"] == 0) &
                        (ticker_df["Open"] == ticker_df["High"]) &
                        (ticker_df["High"] == ticker_df["Low"]) &
                        (ticker_df["Low"] == ticker_df["Close"])             #these lines gives rows which have volume==0 and other values all equal to each other
                    )
                ]

                # If we found real candles, use the latest one
                if not valid_rows.empty:                                     # we only run our code if valid_rows not empty
                    latest = valid_rows.iloc[-1]
                else:
                    latest = ticker_df.iloc[-1]

                candle_time = latest.name

                volume = latest["Volume"]
                if pd.isna(volume):         #checks if volume is null
                    volume = 0              # if volume is null, volume=0

                record = {                                                         #creating a dict called record to append all stock data of a single batch. this dict resets after every batch
                    "timestamp": str(candle_time.tz_convert("Asia/Kolkata")),      #converts time to Indian standard Time
                    "ticker": symbol,
                    "open": round(float(latest["Open"]), 2),
                    "high": round(float(latest["High"]), 2),
                    "low": round(float(latest["Low"]), 2),
                    "close": round(float(latest["Close"]), 2),
                    "volume": int(volume)
                }
                records.append(record)
                print(record)              # for user to see the record after 1 batch complete

            except Exception as e:         # catching errors: 1) KeyError: if Yahoo Finance doesn't return data for a ticker
                print(f"{symbol}: {e}")    #                  2) Timezone Error (AttributeError)
                                           
        filename = datetime.now().strftime("%Y%m%d_%H%M%S")
        df = pd.DataFrame(records)                            # Created a dataframe for better presentation

        df.to_parquet(                                        # downloading the dataframe we created as parquet file in our system
            f"C:/Users/Anmol/Music/Lakehouse/Live/stocks_{filename}.parquet",
            index=False,
            engine="pyarrow"
        )

        print("-" * 80)                                        # For presentation

        time.sleep(60)                                         # to fetch data from yfinance exactly after 1 minute everytime

    except Exception as e:                                     # catching errors like:
        print("Error:", e)                                     #       1) No internet connection
        time.sleep(60)                                         #       2) Yahoo Finance is down
                                                               #       3) yf.download() fails
                                                               #       4) df.to_parquet() cannot write because the disk is full
                                                               #       5) Permission denied when writing the file
