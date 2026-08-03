import streamlit as st
import openai
from PIL import Image
import base64
import io

st.set_page_config(page_title="Crypto AI Trading Bot", page_icon="📈", layout="centered")

st.title("🤖 Solana / Crypto Vision AI Bot")
st.write("Chart ka screenshot upload karo, aur AI batayega ke trade leni hai ya nahi!")

api_key = st.text_input("Apni OpenAI API Key yahan enter karo:", type="password")

if api_key:
    openai.api_key = api_key

    uploaded_file = st.file_uploader("TradingView ka 15-min ya 1-hour chart upload karo...", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Chart", use_column_width=True)
        
        user_notes = st.text_input("Koi khas baat batani hai? (Jaise: Main Buy karna chahta hoon)", "")

        if st.button("🔍 Chart Analyse Karo"):
            with st.spinner("AI Chart parh raha hai... Sabr karo..."):
                try:
                    client = openai.OpenAI(api_key=api_key)
                    
                    prompt = """
                    Tum ek professional crypto trader aur technical analyst ho. Ye di gayi chart image (15-minute ya 1-hour timeframe) ko ghaur se dekho. RSI, Support/Resistance, Trend aur Candlestick patterns ko analyze karo.
                    
                    Mujhe neechay diye gaye format mein bilkul saaf jawab do:
                    1. **Trade Leni Chahiye ya Nahi?** (Yes / No / Wait)
                    2. **Confidence Level:** (Percentage batao jaise 80% ya 85%)
                    3. **Action:** (BUY ya SELL)
                    4. **Entry Price:** (Approximate price jahan entry leni hai)
                    5. **Stop Loss (SL):** (Safe stop loss level kahan hona chahiye)
                    6. **Wajah (Reason):** (Short mein batao ke ye signal kyun diya hai)
                    
                    Agar chart clear nahi hai ya risk zyada hai, toh saaf 'WAIT' likho aur ghalat signal mat do.
                    """

                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt + f"\nUser Note: {user_notes}"},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{img_str}"
                                        },
                                    },
                                ],
                            }
                        ],
                        max_tokens=500,
                    )

                    analysis_result = response.choices[0].message.content
                    st.success("Analysis Mukammal Ho Gayi!")
                    st.markdown("### 📊 AI Trading Signal:")
                    st.markdown(analysis_result)

                except Exception as e:
                    st.error(f"Koi masla aa gaya: {e}")
else:
    st.warning("Pehle apni OpenAI API Key oper enter karo taake bot chal sake.")
