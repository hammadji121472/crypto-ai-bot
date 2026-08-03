from google import genai
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Crypto Gemini AI Bot", page_icon="📈", layout="centered"
)

st.title("📈 Solana / Crypto Gemini AI Bot")
st.write(
    "Seedha chart upload karo — API key ki koi tension nahi, AI foran signal dega!"
)

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error(
        "Streamlit Secrets mein GEMINI_API_KEY set nahi mili! App ki Settings -> Secrets mein ja kar key add karo."
    )
else:
    client = genai.Client(api_key=api_key)

    uploaded_file = st.file_uploader(
        "Apne crypto chart ki image yahan upload karein (PNG, JPG)",
        type=["png", "jpg", "jpeg"],
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(
            image, caption="Uploaded Chart", use_container_width=True
        )

        prompt_text = st.text_input(
            "Koi khas baat batani hai? (Jaise: Main Buy karna chahta hoon)"
        )

        if st.button("Gemini se Analyse Karwayein"):
            with st.spinner("AI chart ko parh raha hai, thoda sabar karo..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[image, prompt_text if prompt_text else "Analyze this crypto chart and give trading signals (Buy/Sell/Hold) with reasons based on technical indicators like RSI, EMA, and support/resistance."],
                    )
                    st.success("Analysis Tayar Hai! 🚀")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Koi error aa gaya: {e}")
