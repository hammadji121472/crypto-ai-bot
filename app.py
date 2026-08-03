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

# Ab yahan 15m, 1h aur 1d teeno pakke show honge
timeframe_choice = st.selectbox(
    "Timeframe Select Karein", ["15m", "1h", "1d"]
)

if st.button("🚀 Strict Signal Nikalein"):
  with st.spinner("Market scan ho rahi hai..."):
    try:
      # 15m ke liye period 2 days kar diya hai taake Yahoo error na de
      if timeframe_choice == "15m":
        yf_interval = "15m"
        yf_period = "2d"
      elif timeframe_choice == "1h":
        yf_interval = "1h"
        yf_period = "7d"
      else:
        yf_interval = "1d"
        yf_period = "1mo"

      df = yf.download(coin_option, period=yf_period, interval=yf_interval)

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
            f"Timeframe: **{timeframe_choice}** | Current Price:"
            f" **${current_price:.4f}** | RSI Value: **{current_rsi:.2f}**"
        )

        # Strict Sniper Logic
        if current_rsi <= 30:
          entry = current_price
          sl = entry * 0.975
          tp = entry * 1.06

          st.success(
              f"🟢 **STRONG BUY SIGNAL — ENTRY LO!**\n\n"
              f"• **Action:** BUY / LONG\n"
              f"• **Entry Price:** ${entry:.4f}\n"
              f"• **Stop Loss (SL):** ${sl:.4f} (2.5% Risk)\n"
              f"• **Take Profit (TP):** ${tp:.4f} (6% Profit)"
          )

        elif current_rsi >= 70:
          entry = current_price
          sl = entry * 1.025
          tp = entry * 0.94

          st.error(
              f"🔴 **STRONG SELL SIGNAL — SHORT ENTRY LO!**\n\n"
              f"• **Action:** SELL / SHORT\n"
              f"• **Entry Price:** ${entry:.4f}\n"
              f"• **Stop Loss (SL):** ${sl:.4f} (2.5% Risk)\n"
              f"• **Take Profit (TP):** ${tp:.4f} (6% Profit)"
          )

        else:
          st.warning(
              "❌ **KOI SIGNAL NAHI — ABHI ENTRY MAT LO!**\nMarket beech mein"
              " phansi hai (Neutral Zone). Fake breakout se bachne ke liye"
              " bilkul trade mat karo, sabar karo."
          )

      else:
        st.error(
            "Data nahi mila. Is timeframe par data available nahi hai, doosra"
            " select karein."
        )
    except Exception as e:
      st.error(f"Error aa gaya: {e}")
