# Real-Time Stock Market Data Pipeline

An end-to-end **Data Engineering project** that ingests historical and near-real-time market data from Yahoo Finance, processes it through a **Bronze → Silver → Gold** architecture using Microsoft Fabric, validates the curated data, and exposes it through a Fabric Warehouse and Power BI.

## 🏗️ Architecture

<img width="1536" height="1024" alt="data_pipeline_architecture" src="https://github.com/user-attachments/assets/3aa19fc0-71fd-4380-b020-6afe1406d13d" />


**Yahoo Finance → Python/yFinance → Parquet → Fabric Lakehouse → Silver → Gold → Validation → Fabric Warehouse → Power BI**

## 🚀 Key Features

- Historical market data ingestion for approximately **5 years**
- Near-real-time ingestion at **1-minute intervals**
- **35 assets** across equities, indices, and cryptocurrencies
- Parquet-based data storage
- Microsoft Fabric Lakehouse
- Bronze → Silver → Gold medallion architecture
- Dimensional modeling using a **star schema**
- Data-quality validation
- Fabric Warehouse
- Interactive Power BI reports

## 🛠️ Technologies

- Python
- yFinance
- Pandas
- PyArrow
- Parquet
- Microsoft Fabric
- Fabric Lakehouse
- PySpark / Spark
- SQL
- Fabric Warehouse
- Power BI
- GitHub

## 📥 Data Ingestion

The pipeline processes **35 assets** across equities, indices, and cryptocurrencies.

Historical data is downloaded using `yfinance` for approximately **5 years** and stored as Parquet.

For near-real-time ingestion, a Python `while` loop requests **1-minute market data**. Each batch is cleaned, converted to Asia/Kolkata timestamps, and written to a timestamped Parquet file. The process waits 60 seconds before requesting the next batch.

## 🥉 Bronze Layer

The Bronze layer of the Microsoft Fabric Lakehouse contains 1,000+ raw Parquet files. Each stock contributes approximately 35 records, resulting in around 35,000 current stock records. 
In addition, approximately 64,000 historical records are stored in the Bronze layer, bringing the total dataset to roughly 100,000 records which is loaded to the bronze lakehouse of fabric.

## 🥈 Silver Layer — Notebook 1

The first Fabric notebook cleans and standardizes the ingested data.

Processing includes:

- Handling null and invalid records
- Cleaning timestamps
- Standardizing columns
- Validating OHLC values
- Preparing data for downstream modeling

## 🥇 Gold Layer — Notebook 2

The second Fabric notebook creates the analytical dimensional model.

The Gold layer contains:

### Dim_Date

Date-related attributes used for time-based analysis.

### Dim_Stock

Stock/asset attributes such as:

- Stock ID
- Ticker
- Asset name
- Asset type
- Market
- Exchange

### Fact_Stock_Prices

Market measurements including:

- Open
- High
- Low
- Close
- Volume
- Date ID
- Stock ID
- Timestamp

The model follows a **star schema**:

```text
Dim_Date ───────┐
                ├── Fact_Stock_Prices
Dim_Stock ──────┘
```

## ✅ Data Validation — Notebook 3

The third Fabric notebook performs data-quality checks on the Gold tables.

Checks include:

- Record counts
- NULL values
- Duplicate records
- Distinct stock counts
- OHLC consistency
- Referential integrity
- Valid stock/date relationships

## 🏢 Fabric Warehouse

Validated Gold data is exposed through a **Microsoft Fabric Warehouse**, providing a SQL-based analytical layer.

## 📊 Power BI

Power BI connects to the curated analytical model and provides interactive reports for:

- Stock performance
- Closing-price trends
- High vs. low price trends
- Trading volume
- Market and asset analysis
- Equity, index, and cryptocurrency analysis

The reports include stock/company selection through slicers.

## 📁 Repository Structure

```text
Real-Time-Stock-Market-Pipeline/
│
├── ingestion/
│   ├── stock_ingestion.py
│   └── README.md
│
├── notebooks/
│   ├── 01_silver_cleaning.ipynb
│   ├── 02_gold_dimensional_model.ipynb
│   └── 03_data_validation.ipynb
│
├── sql/
│   └── validation_queries.sql
│
├── architecture/
│   └── data_pipeline_architecture.png
│
├── screenshots/
│   ├── silver_layer_table.jpg
│   ├── gold_dim_date.jpg
│   ├── gold_dim_stock.jpg
│   ├── gold_fact_stock_prices.jpg
│   ├── gold_data_model.jpg
│   └── data_validation.jpg
│
├── powerbi/
│   ├── dashboard_overview.jpg
│   ├── stock_performance.jpg
│   ├── market_asset_analysis.jpg
│   └── README.md
│
└── README.md
```

## 🧠 Data Engineering Concepts Demonstrated

- Batch ingestion
- Near-real-time ingestion
- ETL / ELT
- Medallion architecture
- Data cleaning
- Data validation
- Parquet
- Lakehouse architecture
- Dimensional modeling
- Star schema
- Fact and dimension tables
- SQL
- Cloud data engineering
- Business intelligence

## 🔄 Pipeline Summary

```text
Yahoo Finance
      ↓
Python / yFinance
      ↓
Parquet Files
      ↓
Bronze
      ↓
Silver
      ↓
Gold
 ┌────┴───────────┐
Dim_Date       Dim_Stock
      \            /
       Fact_Stock_Prices
              ↓
       Data Validation
              ↓
      Fabric Warehouse
              ↓
           Power BI
```

## 🎯 Project Purpose

This project demonstrates practical Data Engineering by taking raw external market data and transforming it into a validated, dimensional analytical dataset suitable for business intelligence.

It combines Python-based ingestion, Microsoft Fabric, Lakehouse processing, dimensional modeling, SQL validation, and Power BI reporting in one end-to-end pipeline.
