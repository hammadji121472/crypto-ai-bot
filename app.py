import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="Pro Sniper Signal Bot", page_icon="🎯", layout="centered"
)

st.title("🎯 Pro Crypto Sniper Bot (Strict Signals Only)")
st.write(
    "Sirf pakka signal milega — No Hold, No Bakwas. Entry lo ya door raho!"
)

st.divider()

coin_option = st.selectbox(
    "Coin Select Karein",
    ["SOL-USD", "BTC-USD", "ETH-USD", "BNB-USD", "PEPE20314-USD"],
)
interval = st.selectbox("Timeframe Select Karein", ["1h", "1d"])

if st.button("🚀 Strict Signal Nikalein"):
  with st.spinner("Market scan ho rahi hai..."):
    try:
      df = yf.download(
          coin_option, period="5d", interval="1h" if interval == "1h" else "1d"
      )

      if not df.empty:
        if isinstance(df.columns, pd.MultiIndex):
          df.columns = df.columns.get_level_values(0)

        close_prices = df["Close"]

        # RSI Calculation
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        current_price = float(close_prices.iloc[-1])
        current_rsi = float(rsi.iloc[-1])

        st.info(
            f"Current Price: **${current_price:.4f}** | RSI Value:"
            f" **{current_rsi:.2f}**"
        )

        # Strict Sniper Logic (No Hold allowed if not extreme)
        if current_rsi <= 30:
          # BUY SETUP
          entry = current_price
          sl = entry * 0.975  # 2.5% Stop Loss
          tp = entry * 1.06  # 6% Take Profit

          st.error(
              "🟢 **STRONG BUY SIGNAL — ENTRY LO!**"
          )  # error box for high visibility green look or success
          st.success(
              f"• **Action:** BUY / LONG\n"
              f"• **Entry Price:** ${entry:.4f}\n"
              f"• **Stop Loss (SL):** ${sl:.4f} (2.5% Risk)\n"
              f"• **Take Profit (TP):** ${tp:.4f} (6% Profit)"
          )

        elif current_rsi >= 70:
          # SELL SETUP
          entry = current_price
          sl = entry * 1.025  # 2.5% Stop Loss above
          tp = entry * 0.94  # 6% Take Profit below

          st.error(
              "🔴 **STRONG SELL SIGNAL — SHORT ENTRY LO!**\n\n"
              f"• **Action:** SELL / SHORT\n"
              f"• **Entry Price:** ${entry:.4f}\n"
              f"• **Stop Loss (SL):** ${sl:.4f} (2.5% Risk)\n"
              f"• **Take Profit (TP):** ${tp:.4f} (6% Profit)"
          )

        else:
          # NO ENTRY
          st.warning(
              "❌ **KOI SIGNAL NAHI — ABHI ENTRY MAT LO!**\nMarket beech mein"
              " phansi hai (Neutral Zone). Fake breakout se bachne ke liye"
              " bilkul trade mat karo, sabar karo."
          )

      else:
        st.error("Data nahi mila. Dobara koshish karein.")
    except Exception as e:
      st.error(f"Error aa gaya: {e}")
