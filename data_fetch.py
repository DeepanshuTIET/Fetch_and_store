from flask import Flask
import yfinance as yf
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Define the list of tickers
TICKERS = ['INFY.NS', 'SBIN.NS', 'NHPC.NS', 'BHEL.NS', 'SAIL.NS']

# Flask configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fiveindistocks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class StockData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), index=True, nullable=False)
    datetime = db.Column(db.DateTime, index=True, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)

# Create the database and the database table
with app.app_context():
    db.create_all()

# Function to fetch and store recent data (past 3 records) with 5-minute interval
def fetch_and_store_recent_data():
    with app.app_context():
        for ticker in TICKERS:
            try:
                # Calculate end_date and start_date for fetching past 15 minutes (3 records)
                end_date = datetime.now()
                start_date = end_date - timedelta(minutes=15)

                # Fetch data for the past 15 minutes with 5-minute interval
                data = yf.download(ticker, start=start_date, end=end_date, interval='5m')

                # Check if data is empty (no records found)
                if data.empty:
                    print(f"No data found for {ticker} in the past 15 minutes.")
                    continue

                # Iterate over fetched data and store in the database
                for index, row in data.iterrows():
                    stock_data = StockData(
                        ticker=ticker,
                        datetime=index,
                        open=row['Open'],
                        high=row['High'],
                        low=row['Low'],
                        close=row['Close'],
                        volume=row['Volume']
                    )
                    db.session.add(stock_data)

                db.session.commit()
                print(f"Fetched and stored recent data for {ticker} successfully.")
            except Exception as e:
                print(f"Failed to fetch or store recent data for {ticker}: {str(e)}")

# Function to fetch and store initial data when the application starts
@app.route('/history')
def fetch_and_store_initial_data():
    for ticker in TICKERS:
        try:
            # Fetch data for the last 10 days with daily interval
            end_date = datetime.now()
            start_date = end_date - timedelta(days=10)
            data = yf.download(ticker, start=start_date, end=end_date, interval='1d')

            # Iterate over fetched data and store in the database
            for index, row in data.iterrows():
                stock_data = StockData(
                    ticker=ticker,
                    datetime=index,
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    volume=row['Volume']
                )
                db.session.add(stock_data)

            db.session.commit()
            print(f"Fetched and stored initial data for {ticker} successfully.")
        except Exception as e:
            print(f"Failed to fetch or store initial data for {ticker}: {str(e)}")

# Fetch initial data when the application starts
with app.app_context():
    fetch_and_store_initial_data()


if __name__ == '__main__':
    with app.app_context():
        # Fetch initial data when the application starts
        fetch_and_store_initial_data()

        # Scheduler to run the fetch_and_store_recent_data function every 5 minutes
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            fetch_and_store_recent_data,  # The function to be executed
            'cron',                       # Specifies the type of trigger (in this case, a cron-like schedule)
            day_of_week='mon-fri',        # The job will run from Monday to Friday
            hour='9-14',                  # The job will run every hour from 9 AM to 2 PM (full hours)
            minute='*/5',                 # The job will run every 5 minutes within the specified hours
            timezone='Asia/Kolkata'       # The timezone in which to interpret the schedule
        )
        scheduler.add_job(
            fetch_and_store_recent_data,  # The function to be executed
            'cron',                       # Specifies the type of trigger (in this case, a cron-like schedule)
            day_of_week='mon-fri',        # The job will run from Monday to Friday
            hour='15',                    # The job will run in the 15th hour
            minute='0-30/5',              # The job will run every 5 minutes from 15:00 to 15:30
            timezone='Asia/Kolkata'       # The timezone in which to interpret the schedule
        )
        scheduler.start()

        # Run the Flask app
        app.run(debug=True)
