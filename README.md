# Stock Data Intelligence Dashboard

A comprehensive full-stack financial platform for analyzing Nifty50 stock data with machine learning predictions and interactive visualizations.

## 🚀 Features

### Core Functionality
- **Data Pipeline**: Automated processing of 50 Nifty50 CSV files with data cleaning and feature engineering
- **Real-time Analytics**: Daily returns, moving averages (7-day, 30-day), 52-week high/low, volatility metrics
- **Machine Learning**: Linear regression-based price predictions for next 5 days
- **Interactive Dashboard**: Modern web interface with Chart.js visualizations

### Advanced Features
- **Stock Comparison**: Side-by-side analysis of any two stocks
- **Top Gainers/Losers**: Real-time identification of best/worst performing stocks
- **Volatility Analysis**: 7-day rolling volatility tracking
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS

### API Endpoints
- `GET /companies` - List all available stock symbols
- `GET /data/{symbol}` - Historical data with metrics
- `GET /summary/{symbol}` - Key statistics (52-week high/low, average)
- `GET /compare?symbol1=X&symbol2=Y` - Comparative analysis
- `GET /predict/{symbol}` - ML-based price predictions
- `GET /top-gainers` - Best performing stocks
- `GET /volatility/{symbol}` - Volatility metrics

## 🛠 Tech Stack

### Backend
- **FastAPI** - High-performance async web framework
- **Pandas** - Data manipulation and analysis
- **Scikit-learn** - Machine learning for predictions
- **SQLite** - Lightweight database storage

### Frontend
- **HTML5 + Tailwind CSS** - Modern, responsive UI
- **Vanilla JavaScript** - No frameworks, pure JS
- **Chart.js** - Interactive data visualizations

### Data Processing
- **Python** - Core processing language
- **NumPy** - Numerical computations
- **Glob** - File pattern matching

## 📊 Data Pipeline

The system processes 50 CSV files containing:
- Date, Symbol, Series, OHLCV data
- Turnover, Trades, Deliverable Volume
- Custom metrics: Daily returns, moving averages, volatility

**Processing Steps:**
1. Load and merge all CSV files
2. Standardize column names and data types
3. Filter equity series only
4. Handle missing values with forward-fill
5. Calculate technical indicators
6. Store in SQLite for fast queries

## 🤖 Machine Learning

### Linear Regression Model
- **Input**: Last 30 days closing prices
- **Output**: Next 5 days price predictions
- **Why Linear Regression?**: Simple, interpretable, fast training
- **Limitations**: Assumes linear trends, doesn't handle seasonality, external factors

### Usage
```python
# Predict next 5 days for INFY
response = requests.get("http://localhost:8000/predict/INFY")
predictions = response.json()["predictions"]
```

## 🏗 Project Structure

```
project/
├── kaggle/              # Raw CSV data files
├── data/                # Processed data & database
│   ├── processed_data.csv
│   └── stock_data.db
├── backend/             # FastAPI server
│   ├── main.py
│   └── requirements.txt
├── frontend/            # Web dashboard
│   └── index.html
├── process_data.py      # Data processing script
└── README.md
```

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Data Processing
```bash
python process_data.py
```

### Frontend
Open `frontend/index.html` in any modern web browser.

## 📈 API Documentation

### Interactive Docs
Visit `http://localhost:8000/docs` for Swagger UI with interactive API testing.

### Example Requests

```bash
# Get all companies
curl http://localhost:8000/companies

# Get INFY data (last 30 days)
curl "http://localhost:8000/data/INFY?days=30"

# Compare INFY vs TCS
curl "http://localhost:8000/compare?symbol1=INFY&symbol2=TCS"

# Get price predictions
curl http://localhost:8000/predict/INFY
```

## 🎯 Usage Examples

### Basic Stock Analysis
1. Select company from sidebar
2. View closing price chart with predictions
3. Switch between 30/90-day views
4. Check summary statistics

## 📊 Data Insights

### Key Metrics Explained
- **Daily Return**: `(Close - Open) / Open` - Day's price movement
- **Moving Averages**: Smoothed price trends over time
- **52-Week High/Low**: Annual price range (252 trading days)
- **Volatility**: 7-day rolling standard deviation of prices


## 🙏 Acknowledgments

- Nifty50 data from Kaggle
- Chart.js for visualization library
- FastAPI for robust API framework
- Tailwind CSS for styling

## 📞 Support

For questions or issues:
- Open GitHub issue
- Check API documentation at `/docs`
- Review data processing logs

---

**Built with ❤️ for financial data enthusiasts**