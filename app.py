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

# Image Upload
uploaded_file = st.file_uploader(
    "🖼️ একটি ছবি আপলোড করুন",
    type=["jpg", "jpeg", "png"]
)

# Text Input
question = st.text_input("আপনার প্রশ্ন লিখুন")

# Send Button
if st.button("Send"):

    if question or uploaded_file:

        # Image AI
        if uploaded_file:

            image_bytes = uploaded_file.read()

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    "এই ছবিটি বাংলায় বিস্তারিতভাবে ব্যাখ্যা করো।",
                    {
                        "mime_type": uploaded_file.type,
                        "data": image_bytes,
                    },
                ],
            )

        # Normal Chat
        else:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=question
            )

        answer = response.text

        # Show Answer
        st.success(answer)

        # Voice Output
        tts = gTTS(
            text=answer,
            lang="bn"
        )

        tmp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(tmp.name)

        st.audio(tmp.name)
