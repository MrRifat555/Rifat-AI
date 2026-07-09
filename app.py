import os
import tempfile
import streamlit as st
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
from google import genai

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Page Title
st.set_page_config(
    page_title="Rifat AI",
    page_icon="🤖"
)

st.title("🤖 Rifat AI")

# Voice Recorder
audio = mic_recorder(
    start_prompt="🎤 কথা বলুন",
    stop_prompt="⏹️ Stop",
    key="mic"
)

# Text Input
question = st.text_input("আপনার প্রশ্ন লিখুন")

# Send Button
if st.button("Send"):

    if question:

        # AI Response
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question
        )

        answer = response.text

        # Show Answer
        st.success(answer)

        # Convert Answer to Voice
        tts = gTTS(
            text=answer,
            lang="bn"
        )

        tmp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(tmp.name)

        # Play Voice
        st.audio(tmp.name)
