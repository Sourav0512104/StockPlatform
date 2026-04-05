from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

app = FastAPI(title="Stock Data Intelligence Dashboard API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data once on startup
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed_data.csv")
df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])

# Ensure data is sorted
df = df.sort_values(['symbol', 'date'])

@app.get("/companies")
def get_companies():
    """Return list of all unique stock symbols with latest metrics"""
    symbols = df['symbol'].unique().tolist()
    companies_data = []

    for symbol in symbols:
        symbol_data = df[df['symbol'] == symbol].sort_values('date')
        if not symbol_data.empty:
            latest = symbol_data.iloc[-1]
            prev_close = latest['prev_close'] if pd.notna(latest['prev_close']) else latest['open']
            change_rs = latest['close'] - prev_close
            change_percent = (change_rs / prev_close) * 100 if prev_close != 0 else 0

            companies_data.append({
                "symbol": symbol,
                "latest_close": latest['close'],
                "change_rs": round(change_rs, 2),
                "change_percent": round(change_percent, 2),
                "daily_return": latest['daily_return']
            })

    return {"companies": companies_data}

@app.get("/data/{symbol}")
def get_data(symbol: str, days: int = 30):
    """Return last N days data for a symbol"""
    symbol_data = df[df['symbol'] == symbol.upper()]
    if symbol_data.empty:
        raise HTTPException(status_code=404, detail="Symbol not found")

    # Get last N days
    latest_date = symbol_data['date'].max()
    start_date = latest_date - timedelta(days=days)
    filtered_data = symbol_data[symbol_data['date'] >= start_date]

    # Convert to dict for JSON
    result = filtered_data[['date', 'open', 'high', 'low', 'close', 'volume', 'daily_return', 'ma_7', 'ma_30', 'volatility']].to_dict('records')

    # Convert dates to string
    for record in result:
        record['date'] = record['date'].strftime('%Y-%m-%d')

    return {"symbol": symbol.upper(), "data": result}

@app.get("/summary/{symbol}")
def get_summary(symbol: str):
    """Return summary metrics for a symbol"""
    symbol_data = df[df['symbol'] == symbol.upper()]
    if symbol_data.empty:
        raise HTTPException(status_code=404, detail="Symbol not found")

    # Calculate metrics
    avg_close = symbol_data['close'].mean()
    high_52w = symbol_data['52w_high'].dropna().iloc[-1] if not symbol_data['52w_high'].dropna().empty else None
    low_52w = symbol_data['52w_low'].dropna().iloc[-1] if not symbol_data['52w_low'].dropna().empty else None

    return {
        "symbol": symbol.upper(),
        "52_week_high": high_52w,
        "52_week_low": low_52w,
        "average_close": avg_close
    }

@app.get("/compare")
def compare_stocks(symbol1: str, symbol2: str, days: int = 30):
    """Compare closing prices of two symbols"""
    data1 = df[df['symbol'] == symbol1.upper()]
    data2 = df[df['symbol'] == symbol2.upper()]

    if data1.empty or data2.empty:
        raise HTTPException(status_code=404, detail="One or both symbols not found")

    # Get last N days
    latest_date = max(data1['date'].max(), data2['date'].max())
    start_date = latest_date - timedelta(days=days)

    data1_filtered = data1[data1['date'] >= start_date][['date', 'close']].rename(columns={'close': f'{symbol1.upper()}_close'})
    data2_filtered = data2[data2['date'] >= start_date][['date', 'close']].rename(columns={'close': f'{symbol2.upper()}_close'})

    # Merge on date
    merged = pd.merge(data1_filtered, data2_filtered, on='date', how='outer').sort_values('date')

    # Calculate correlation
    corr_data = merged.dropna()
    correlation = corr_data[f'{symbol1.upper()}_close'].corr(corr_data[f'{symbol2.upper()}_close']) if not corr_data.empty else None

    # Convert to dict
    result = merged.to_dict('records')
    for record in result:
        record['date'] = record['date'].strftime('%Y-%m-%d')

    return {"comparison": result, "correlation": round(correlation, 4) if correlation else None}

@app.get("/top-losers")
def get_top_losers(days: int = 1, limit: int = 10):
    """Return top losing stocks in the last N days"""
    # Get latest date
    latest_date = df['date'].max()
    start_date = latest_date - timedelta(days=days)

    # Filter data
    recent_data = df[df['date'] >= start_date]

    # Calculate returns per symbol
    returns = recent_data.groupby('symbol').agg({
        'close': ['first', 'last'],
        'daily_return': 'mean'
    }).reset_index()

    returns.columns = ['symbol', 'first_close', 'last_close', 'avg_daily_return']
    returns['total_return'] = (returns['last_close'] - returns['first_close']) / returns['first_close']

    # Sort by total return ascending (worst performers)
    top_losers = returns.sort_values('total_return', ascending=True).head(limit)

    return {"top_losers": top_losers[['symbol', 'total_return', 'avg_daily_return']].to_dict('records')}


@app.get("/top-gainers")
def get_top_gainers(days: int = 1, limit: int = 10):
    """Return top gaining stocks in the last N days"""
    # Get latest date
    latest_date = df['date'].max()
    start_date = latest_date - timedelta(days=days)

    # Filter data
    recent_data = df[df['date'] >= start_date]

    # Calculate returns per symbol
    returns = recent_data.groupby('symbol').agg({
        'close': ['first', 'last'],
        'daily_return': 'mean'
    }).reset_index()

    returns.columns = ['symbol', 'first_close', 'last_close', 'avg_daily_return']
    returns['total_return'] = (returns['last_close'] - returns['first_close']) / returns['first_close']

    # Sort by total return descending
    top_gainers = returns.sort_values('total_return', ascending=False).head(limit)

    return {"top_gainers": top_gainers[['symbol', 'total_return', 'avg_daily_return']].to_dict('records')}

@app.get("/volatility/{symbol}")
def get_volatility(symbol: str, days: int = 30):
    """Return volatility data for a symbol"""
    symbol_data = df[df['symbol'] == symbol.upper()]
    if symbol_data.empty:
        raise HTTPException(status_code=404, detail="Symbol not found")

    latest_date = symbol_data['date'].max()
    start_date = latest_date - timedelta(days=days)
    filtered_data = symbol_data[symbol_data['date'] >= start_date]

    result = filtered_data[['date', 'volatility']].dropna().to_dict('records')
    for record in result:
        record['date'] = record['date'].strftime('%Y-%m-%d')

    return {"symbol": symbol.upper(), "volatility": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
