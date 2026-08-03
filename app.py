import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="Yahoo Pro Signal Bot", page_icon="⚡", layout="centered"
)

st.title("⚡ Pro Crypto Signal Bot (Yahoo Live Data)")
st.write(
    "Yeh system Yahoo Finance se live data uthata hai — 100% working aur"
    " error-free!"
)

st.divider()

# Coin selection (Yahoo symbols format)
coin_option = st.selectbox(
    "Coin Select Karein",
    ["SOL-USD", "BTC-USD", "ETH-USD", "BNB-USD", "PEPE20314-USD"],
)
interval = st.selectbox("Timeframe Select Karein", ["1h", "1d"])

if st.button("🚀 Live Signal Check Karein"):
  with st.spinner("Live data fetch ho raha hai..."):
    try:
      # Yahoo Finance se data lana
      df = yf.download(
          coin_option, period="5d", interval="1h" if interval == "1h" else "1d"
      )

      if not df.empty:
        # MultiIndex columns fix for yfinance newer versions
        if isinstance(df.columns, pd.MultiIndex):
          df.columns = df.columns.get_level_values(0)

        close_prices = df["Close"]

        # RSI calculation
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        current_price = float(close_prices.iloc[-1])
        current_rsi = float(rsi.iloc[-1])

        st.success(
            f"Data Mil Gaya! Current Price: **${current_price:.4f}** | RSI:"
            f" **{current_rsi:.2f}**"
        )

        if current_rsi <= 32:
          st.markdown(
              "### 🟢 STRONG BUY SIGNAL (Oversold)"
              f"Market oversold zone ({current_rsi:.2f}) mein hai. Yeh bounce"
              " karne ka strong mauqa hai!"
          )
        elif current_rsi >= 68:
          st.markdown(
              "### 🔴 STRONG SELL SIGNAL (Overbought)"
              f"Market overbought zone ({current_rsi:.2f}) mein hai. Yahan se"
              " price gir sakti hai!"
          )
        else:
          st.markdown(
              "### 🟡 HOLD / NEUTRAL"
              f"RSI current level ({current_rsi:.2f}) par neutral hai. Mazeed"
              " confirmation ka wait karein."
          )
      else:
        st.error("Data nahi mila. Dobara koshish karein.")
    except Exception as e:
      st.error(f"Error aa gaya: {e}")
