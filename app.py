from flask import Flask, jsonify
import yfinance as yf

app = Flask(__name__)

# Endpoint for Latest Data
@app.route('/stock/<ticker>/<exchange>', methods=['GET'])
def latest_stock_data(ticker, exchange):
    # Adjust ticker for different exchanges
    if exchange.upper() == "ASX":
        yf_ticker = f"{ticker}.AX"
    else:
        yf_ticker = ticker.upper()

    stock = yf.Ticker(yf_ticker)
    data = stock.history(period="10d")
    latest = data.iloc[-1]

    response = {
        "ticker": ticker.upper(),
        "exchange": exchange.upper(),
        "latest_data": {
            "open": round(latest['Open'], 2),
            "high": round(latest['High'], 2),
            "low": round(latest["Low"], 2),
            "close": round(latest["Close"], 2),
            "volume": int(latest["Volume"])
        }
    }
    return jsonify(response)

# Endpoint for Historical Data
@app.route('/stock/<ticker>/<exchange>/historical', methods=['GET'])
def historical_stock_data(ticker, exchange):
    # Adjust ticker based on exchange
    if exchange.upper() == "ASX":
        yf_ticker = f"{ticker}.AX"
    else:
        yf_ticker = ticker.upper()

    stock = yf.Ticker(yf_ticker)
    historical = stock.history(period="30d")

    historical_data = []
    for date, row in historical.iterrows():
        historical_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": round(row["Open"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "close": round(row["Close"], 2),
            "volume": int(row["Volume"])
        })

    response = {
        "ticker": ticker.upper(),
        "exchange": exchange.upper(),
        "historical_data": historical_data
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)