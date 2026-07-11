import os
import tempfile
import streamlit as st
from PIL import Image
from pypdf import PdfReader
from gtts import gTTS
from google import genai
from google.genai import types
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
# ==========================
# Gemini Client
# ==========================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ==========================
# Page Config
# ==========================

st.set_page_config(
    page_title="🤖 Rifat AI v4.0",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Rifat AI v4.0")
audio = mic_recorder(
    start_prompt="🎤 কথা বলুন",
    stop_prompt="⏹️ Stop",
    key="voice"
)
st.caption("🚀 Chat • Image • PDF • Internet • Voice")

# ==========================
# Sidebar
# ==========================

with st.sidebar:

    st.header("⚙️ Rifat AI")

    search_mode = st.toggle(
        "🌐 Internet Search",
        value=False
    )

    voice_mode = st.toggle(
        "🔊 Voice Response",
        value=True
    )

    st.divider()

    st.write("📂 Upload Files")

# ==========================
# Image Upload
# ==========================

uploaded_image = st.file_uploader(
    "🖼️ Upload Image",
    type=["jpg", "jpeg", "png"]
)

image = None

if uploaded_image:

    image = Image.open(uploaded_image)

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

# ==========================
# PDF Upload
# ==========================

uploaded_pdf = st.file_uploader(
    "📄 Upload PDF",
    type=["pdf"]
)

# ==========================
# Chat History
# ==========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = {}

    st.session_state.memory = {}
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])
memory_text = ""

for key, value in st.session_state.memory.items():
    memory_text += f"{key}: {value}\n"
prompt = st.chat_input("💬 Ask Rifat AI...")
# ==========================
# User Message
# ==========================
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

            # শুধু প্রথম ৩ পৃষ্ঠা
            for page in reader.pages[:3]:

                text = page.extract_text()

                if text:
                    pdf_text += text

            # বেশি বড় হলে কেটে দাও
            pdf_text = pdf_text[:12000]

            response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"""
Memory:

{memory_text}

নিচের PDF ব্যবহার করে প্রশ্নের উত্তর দাও।

PDF:

{pdf_text}

User Question:

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
        # Internet Search
        # ==========================

        elif search_mode:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[
                        types.Tool(
                            google_search=types.GoogleSearch()
                        )
                    ]
                )
            )

        # ==========================
        # Normal Chat
        # ==========================

        else:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
Memory:

{memory_text}

User:

{prompt}
"""
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

        if voice_mode:

            try:

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

            except Exception:

                st.warning("🔊 Voice তৈরি করা যায়নি।")

    except Exception as e:

        st.error("❌ AI উত্তর তৈরি করতে সমস্যা হয়েছে।")

        with st.expander("Error Details"):

            st.code(str(e))

# ==========================
# Footer
# ==========================

st.divider()

st.caption("🚀 Rifat AI v4.0 | Powered by Gemini")
