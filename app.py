import os
import tempfile
import streamlit as st
from gtts import gTTS
from PIL import Image
from pypdf import PdfReader
from google import genai

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Page Config
st.set_page_config(
    page_title="Rifat AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Rifat AI v3.1")

# ==========================
# Image Upload
# ==========================

uploaded_image = st.file_uploader(
    "🖼️ ছবি আপলোড করুন",
    type=["jpg", "jpeg", "png"]
)

image = None

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="আপলোড করা ছবি", use_container_width=True)

# ==========================
# PDF Upload
# ==========================

uploaded_pdf = st.file_uploader(
    "📄 PDF আপলোড করুন",
    type=["pdf"]
)

# ==========================
# Chat History
# ==========================

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("আপনার প্রশ্ন লিখুন...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:

        # ==========================
        # PDF AI
        # ==========================

        if uploaded_pdf:

            reader = PdfReader(uploaded_pdf)

            pdf_text = ""

            # শুধু প্রথম ৩ পৃষ্ঠা পড়বে
            for page in reader.pages[:3]:

                text = page.extract_text()

                if text:
                    pdf_text += text

            # বেশি বড় হলে কেটে দাও
            pdf_text = pdf_text[:12000]

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
নিচের PDF-এর তথ্য ব্যবহার করে প্রশ্নের উত্তর দাও।

PDF:

{pdf_text}

প্রশ্ন:

{prompt}
"""
            )

        # ==========================
        # Image AI
        # ==========================

        elif image:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    image
                ]
            )

        # ==========================
        # Normal Chat
        # ==========================

        else:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        answer = response.text

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

        # ==========================
        # Voice Output
        # ==========================

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

    except Exception as e:

        st.error("❌ AI উত্তর তৈরি করতে সমস্যা হয়েছে। আবার চেষ্টা করুন।")

        st.exception(e)
