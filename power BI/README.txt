# Power BI Dashboard

The processed Gold-layer stock market data was served through
Microsoft Fabric Warehouse and consumed by Power BI for analytical
reporting.

## Dashboard Pages

### 1. Stock Overview

Provides an overview of stock prices and trading activity, including
closing-price trends, high/low price movements, trading volume and
interactive stock selection.

### 2. Stock Performance

Provides comparative analysis across stocks, including top stocks by
average closing price and trading volume.

### 3. Market & Asset Analysis

Provides an overview of the assets and markets included in the dataset,
including asset-type distribution and market-level comparisons.

## Data Source

Power BI consumes the dimensional model served through the Microsoft
Fabric Warehouse:

- Dim_Date
- Dim_Stock
- Fact_Stock_Prices