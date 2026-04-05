import pandas as pd
import numpy as np
import glob
import os
import sqlite3
from datetime import datetime

def load_and_process_data(data_folder):
    """
    Load all CSV files from the data folder, clean and process them.
    """
    all_files = glob.glob(os.path.join(data_folder, "*.csv"))
    df_list = []

    for file in all_files:
        df = pd.read_csv(file)
        df_list.append(df)

    # Merge all dataframes
    combined_df = pd.concat(df_list, ignore_index=True)

    return combined_df

def standardize_columns(df):
    """
    Standardize column names to snake_case and remove spaces.
    """
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('%', 'percent')
    return df

def convert_date(df):
    """
    Convert Date column to datetime.
    """
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def filter_series(df):
    """
    Filter only rows where series == 'EQ'
    """
    df = df[df['series'] == 'EQ']
    return df

def handle_missing_values(df):
    """
    Handle missing values in the dataframe.
    """
    # For numeric columns, fill with forward fill or mean
    numeric_cols = ['prev_close', 'open', 'high', 'low', 'last', 'close', 'vwap', 'volume', 'turnover', 'trades', 'deliverable_volume', 'percent_deliverble']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(method='ffill').fillna(df[col].mean())

    # Drop rows with missing date or symbol
    df = df.dropna(subset=['date', 'symbol'])

    return df

def calculate_metrics(df):
    """
    Calculate required metrics grouped by symbol.
    """
    # Sort by symbol and date
    df = df.sort_values(['symbol', 'date'])

    # Daily Return
    df['daily_return'] = (df['close'] - df['open']) / df['open']

    # Moving Averages
    df['ma_7'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(window=7).mean())
    df['ma_30'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(window=30).mean())

    # 52-week High/Low (252 trading days)
    df['52w_high'] = df.groupby('symbol')['high'].transform(lambda x: x.rolling(window=252).max())
    df['52w_low'] = df.groupby('symbol')['low'].transform(lambda x: x.rolling(window=252).min())

    # Volatility (7-day rolling std of close)
    df['volatility'] = df.groupby('symbol')['close'].transform(lambda x: x.rolling(window=7).std())

    # Volume Trend (7-day MA of volume)
    df['volume_trend'] = df.groupby('symbol')['volume'].transform(lambda x: x.rolling(window=7).mean())

    return df

def save_to_csv(df, output_path):
    """
    Save the processed dataframe to CSV.
    """
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

def save_to_sqlite(df, db_path, table_name='stock_data'):
    """
    Save the dataframe to SQLite database.
    """
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"Data saved to SQLite database: {db_path}, table: {table_name}")

if __name__ == "__main__":
    data_folder = r"c:\Users\sreen\Desktop\FinDash\kaggle"
    output_csv = "processed_data.csv"
    db_path = "stock_data.db"

    # Load and process
    df = load_and_process_data(data_folder)
    df = standardize_columns(df)
    df = convert_date(df)
    df = filter_series(df)
    df = handle_missing_values(df)
    df = calculate_metrics(df)

    # Save
    save_to_csv(df, output_csv)
    save_to_sqlite(df, db_path)

    print("Data processing complete!")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(df.head())