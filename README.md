# 📈 Stock Data Intelligence Dashboard

A comprehensive full-stack financial platform for analyzing Nifty50 stock data with machine learning predictions and interactive visualizations. Built with FastAPI, Pandas, and modern web technologies.

## 🚀 Features

### Core Functionality
- **Data Pipeline**: Automated processing of 50 Nifty50 CSV files with data cleaning and feature engineering
- **Real-time Analytics**: Daily returns, moving averages (7-day, 30-day), 52-week high/low, volatility metrics
- **Machine Learning**: Linear regression-based price predictions for next 5 days
- **Interactive Dashboard**: Modern web interface with Chart.js visualizations
- **RESTful API**: Fully documented endpoints with Swagger UI

### Advanced Features
- **Stock Comparison**: Side-by-side analysis of any two stocks
- **Top Gainers/Losers**: Real-time identification of best/worst performing stocks
- **Volatility Analysis**: 7-day rolling volatility tracking
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **Quick Start Templates**: Pre-built API examples and usage scenarios

### API Endpoints
- `GET /companies` - List all available stock symbols
- `GET /data/{symbol}` - Historical data with technical metrics
- `GET /summary/{symbol}` - Key statistics (52-week high/low, average volatility)
- `GET /compare?symbol1=X&symbol2=Y` - Comparative analysis of two stocks
- `GET /predict/{symbol}` - ML-based price predictions for next 5 days
- `GET /top-gainers` - Best performing stocks with daily returns
- `GET /volatility/{symbol}` - Volatility metrics and trends

## 🛠 Tech Stack

### Backend
- **FastAPI** (0.104.1) - High-performance async web framework
- **Uvicorn** (0.24.0) - ASGI server with auto-reload
- **Pandas** (2.1.4) - Data manipulation and analysis
- **NumPy** (1.26.2) - Numerical computations
- **SQLite** - Lightweight database storage

### Frontend
- **HTML5 + Tailwind CSS** - Modern, responsive UI
- **Vanilla JavaScript** - No frameworks, pure JS implementation
- **Chart.js** - Interactive data visualizations

### Data Processing
- **Python 3.10.12** - Core processing language
- **Glob** - File pattern matching for batch processing

## 📊 Data Pipeline

The system processes 50 CSV files containing Nifty50 stock data:
- **Fields**: Date, Symbol, Series, OHLCV data, Turnover, Trades, Deliverable Volume
- **Custom Metrics**: Daily returns, moving averages (7/30-day), 52-week high/low, volatility

### Processing Steps
1. Load and merge all CSV files from kaggle/ directory
2. Standardize column names and data types
3. Filter equity series only (Series == 'EQ')
4. Handle missing values with forward-fill and mean imputation
5. Calculate technical indicators and metrics
6. Store in SQLite for fast queries and CSV export

###Deployed on Render
https://findash-q699.onrender.com/
