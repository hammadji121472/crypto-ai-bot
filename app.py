from google import genai
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Crypto Gemini AI Bot", page_icon="📈", layout="centered"
)

st.title("🤖 Solana / Crypto Gemini AI Bot")
st.write(
    "Seedha chart upload karo — API key ki koi tension nahi, AI foran signal"
    " dega!"
)

try:
  api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
  api_key = None

if not api_key:
  st.error(
      "⚠️ Streamlit Secrets mein GEMINI_API_KEY set nahi mili! App ki Settings"
      " -> Secrets mein ja kar key add karo."
  )
else:
  client = genai.Client(api_key=api_key)

  uploaded_file = st.file_uploader(
      "TradingView ka 15-min ya 1-hour chart upload karo...",
      type=["png", "jpg", "jpeg"],
  )

  if uploaded_file is not None:
    image = Image.open(uploaded_file)
    if image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    ):
      image = image.convert("RGB")

    st.image(image, caption="Uploaded Chart", use_column_width=True)

    user_prompt = st.text_input(
        "Koi khas baat batani hai? (Jaise: Main Buy karna chahta hoon)"
    )

    if st.button("🔍 Gemini se Analyse Karwayein"):
      with st.spinner("Gemini AI chart ko analyze kar raha hai..."):
        prompt_text = (
            "You are an expert crypto day trader and technical analyst."
            " Analyze this 15-minute or 1-hour cryptocurrency chart image."
            " Look at indicators like RSI, moving averages (EMA/SMA),"
            " support/resistance, and candlestick patterns. Give a clear"
            " verdict: Should the user take a LONG (buy), SHORT (sell), or"
            " STAY OUT? Provide entry zone, stop loss, and take profit"
            " targets with a short reasoning."
        )
        if user_prompt:
          prompt_text += f"\nUser's additional note: {user_prompt}"

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=[image, prompt_text]
        )

        st.subheader("📊 Gemini AI Analysis & Trade Verdict:")
        st.write(response.text)
