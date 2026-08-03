import base64
import io
from openai import OpenAI
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Crypto AI Trading Bot", page_icon="📈", layout="centered"
)

st.title("🤖 Solana / Crypto Vision AI Bot")
st.write("Chart ka screenshot upload karo, aur AI batayega ke trade leni hai ya nahi!")

api_key = st.text_input("Apni OpenAI API Key yahan enter karo:", type="password")

if api_key:
  client = OpenAI(api_key=api_key)

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

    if st.button("🔍 Chart Analyse Karo"):
      with st.spinner("AI chart ko analyze kar raha hai..."):
        try:
          buffered = io.BytesIO()
          image.save(buffered, format="JPEG")
          encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

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
            prompt_text += (
                f"\nUser's additional note: {user_prompt}"
            )

          response = client.chat.completions.create(
              model="gpt-4o",
              messages=[
                  {
                      "role": "user",
                      "content": [
                          {"type": "text", "text": prompt_text},
                          {
                              "type": "image_url",
                              "image_url": {
                                  "url": f"data:image/jpeg;base64,{encoded_image}"
                              },
                          },
                      ],
                  }
              ],
              max_tokens=800,
          )

          st.subheader("📊 AI Analysis & Trade Verdict:")
          st.write(response.choices[0].message.content)

        except Exception as e:
          st.error(f"Koi masla aa gaya: {e}")
else:
  st.warning("Pehle apni API Key oper enter karo taake bot chal sake.")
