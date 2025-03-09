from flask import Flask, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/stock/<ticker>/<exchange>', methods=['GET'])
def stock_analysis(ticker, exchange):
    # Adjust ticker for exchanges other than NASDAQ/NYSE
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

if __name__ == '__main__':
    app.run(debug=True)