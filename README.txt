# Data Ingestion

Stock market data was ingested using Python and the `yfinance` library.

## Historical Data

Historical data for the selected stocks was retrieved using the `yfinance`
API for a 5-year period and stored as Parquet files.

## Live Data

Live market data was retrieved at 1-minute intervals.

A `while True` loop continuously:
1. Fetches the latest 1-minute market data.
2. Filters invalid/placeholder candles.
3. Extracts the latest valid OHLCV record for each asset.
4. Converts timestamps to IST.
5. Writes the batch to a timestamped Parquet file.
6. Waits 60 seconds before fetching the next batch.

The generated Parquet files were subsequently processed in Microsoft Fabric.