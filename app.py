import os
import streamlit as st
from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.title("🤖 Rifat AI")

question = st.text_input("আপনার প্রশ্ন লিখুন")

if st.button("Send"):
    if question:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question
        )
        st.write(response.text)
