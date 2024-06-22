# Stock Data Fetcher

This project is a Flask web application that fetches and stores stock data for a list of tickers using the `yfinance` library. The application stores the data in an SQLite database and schedules periodic updates using APScheduler.

## Features

- Fetches and stores stock data for the last 10 days when the application starts.
- Periodically fetches and stores stock data every 5 minutes during market hours.
- Stores stock data in an SQLite database using SQLAlchemy.

## Requirements

- Python 3.7 or higher
- Flask
- yfinance
- Flask-SQLAlchemy
- APScheduler

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/stock-data-fetcher.git
    cd stock-data-fetcher
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Open the `app.py` file.
2. Set the `SECRET_KEY` in the Flask configuration.
3. Ensure the database URI in `SQLALCHEMY_DATABASE_URI` points to the desired SQLite database file.

## Running the Application

1. Initialize the database:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

2. Run the Flask application:

    ```bash
    python app.py
    ```

The application will start and fetch the initial data. It will also set up a scheduler to fetch and store recent data every 5 minutes during the specified market hours.

## Endpoints

- `/history`: Fetches and stores initial data for the last 10 days.

## Scheduling

The application uses APScheduler to fetch and store recent data every 5 minutes during market hours (9 AM to 2 PM and 3 PM to 3:30 PM IST, Monday to Friday).

## Database Schema

The SQLite database contains a single table `StockData` with the following columns:

- `id`: Integer, primary key
- `ticker`: String, stock ticker symbol
- `datetime`: DateTime, timestamp of the stock data
- `open`: Float, opening price
- `high`: Float, highest price
- `low`: Float, lowest price
- `close`: Float, closing price
- `volume`: Integer, trading volume

## License

This project is licensed under the MIT License.
