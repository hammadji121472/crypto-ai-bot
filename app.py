import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Binance Live Pro Signal Bot", page_icon="⚡", layout="centered"
)

st.title("⚡ Binance Live Crypto Signal Bot (Zero Error)")
st.write(
    "Yeh system seedha Binance market se live data uthata hai — Na koi API key"
    " chahiye, na kabhi 429 error aayega!"
)

st.divider()

# User se coin select karwana
symbol = st.selectbox(
    "Coin Select Karein",
    ["SOLUSDT", "BTCUSDT", "ETHUSDT", "PEPEUSDT", "BNBUSDT"],
)
interval = st.selectbox("Timeframe Select Karein", ["1h", "4h", "15m"])


# Binance se live data fetch karne ka function
def get_binance_data(symbol, interval):
  url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"
  try:
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(
        data,
        columns=[
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "num_trades",
            "taker_buy_base",
            "taker_buy_quote",
            "ignore",
        ],
    )
    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    return df
  except Exception as e:
    return None


if st.button("🚀 Live Signal Check Karein"):
  with st.spinner("Binance से live data fetch ho raha hai..."):
    df = get_binance_data(symbol, interval)

    if df is not None and not df.empty:
      # Simple RSI calculation logic for live data
      delta = df["close"].diff()
      gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
      loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
      rs = gain / loss
      df["rsi"] = 100 - (100 / (1 + rs))

      current_price = df["close"].iloc[-1]
      current_rsi = df["rsi"].iloc[-1]

      st.success(
          f"Live Data Mil Gaya! Current Price: **${current_price:.4f}** | RSI:"
          f" **{current_rsi:.2f}**"
      )

      # Signal Logic
      if current_rsi <= 32:
        st.markdown(
            "### 🟢 STRONG BUY SIGNAL (Oversold)"
            f"Market oversold zone ({current_rsi:.2f}) mein hai. Yeh bounce karne"
            " ka strong mauqa hai!"
        )
      elif current_rsi >= 68:
        st.markdown(
            "### 🔴 STRONG SELL SIGNAL (Overbought)"
            f"Market overbought zone ({current_rsi:.2f}) mein hai. Yahan se price"
            " gir sakti hai!"
        )
      else:
        st.markdown(
            "### 🟡 HOLD / NEUTRAL"
            f"RSI current level ({current_rsi:.2f}) par neutral hai. Mazeed"
            " confirmation ka wait karein."
        )
    else:
      st.error(
          "Binance se data laane mein masla hua. Dobara button dabayein."
      )
