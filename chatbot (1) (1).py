import os
import streamlit as st
from google import genai

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="🎯 AI Career Advisor", page_icon="🎓", layout="wide")

# ---------- LOAD API KEY ----------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("API key missing. Add GOOGLE_API_KEY in Space → Settings → Secrets.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# ---------- INIT CLIENT ----------
@st.cache_resource
def get_client():
    return genai.Client()

client = get_client()

# ---------- SYSTEM PROMPT ----------
system_prompt = """
You are a professional AI Career Advisor.

Your role:
- Help users choose the right career path
- Suggest in-demand skills
- Provide personalized learning roadmaps
- Give resume, portfolio, and interview guidance
- Share real-world job insights

Ask users about:
- Education
- Skills
- Interests
- Career goals

Restriction:
Answer ONLY career, skills, jobs, education, and growth related queries.
If user asks anything else say:
"I can help only with career guidance and professional growth."
"""

# ---------- CREATE CHAT SESSION ----------
def create_chat():
    return client.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )

# ---------- SESSION STATE ----------
if "chat_session" not in st.session_state:
    st.session_state.chat_session = create_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("🎓 AI Career Advisor")
    st.markdown("Plan • Learn • Grow • Get Hired")

    st.divider()

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_session = create_chat()
        st.rerun()

    st.divider()

    st.markdown("### 💡 Try asking:")
    st.markdown("""
- Roadmap to become a Data Analyst  
- Best career for B.Tech student  
- In-demand skills in 2026  
- How to switch to AI career?  
- Resume tips for freshers  
""")

# ---------- TITLE ----------
st.markdown("<h1 style='text-align: center;'>🎯 AI Career Advisor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Your Personal Career Growth Partner</p>", unsafe_allow_html=True)

# ---------- DISPLAY CHAT ----------
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(message)

# ---------- USER INPUT ----------
user_input = st.chat_input("Ask about careers, skills, jobs, or learning paths...")

# ---------- RESPONSE ----------
if user_input:

    st.session_state.messages.append(("user", user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your career path... 🎯"):

            try:
                response = st.session_state.chat_session.send_message(user_input)
                bot_reply = response.text

            except Exception as e:
                print(e)  # Visible in Hugging Face logs
                bot_reply = "⚠️ Service temporarily unavailable. Please try again later."

            st.markdown(bot_reply)

    st.session_state.messages.append(("assistant", bot_reply))