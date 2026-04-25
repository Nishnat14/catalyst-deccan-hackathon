import streamlit as st
import requests

# ── CONFIG ─────────────────────────────────────────────
st.set_page_config(
    page_title="SkillSense AI – Skill Assessment Agent",
    page_icon="🎯",
    layout="centered"
)

# ── STYLING ────────────────────────────────────────────
st.markdown("""
<style>
.main { background-color: #f8f9fb; }
.stChatMessage { border-radius: 12px; margin-bottom: 8px; }
.status-box {
    background: #eef2ff;
    border-left: 4px solid #4f46e5;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── API KEY ────────────────────────────────────────────
if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("Missing API Key")
    st.stop()

API_KEY = st.secrets["OPENROUTER_API_KEY"]

# ── SYSTEM PROMPT ──────────────────────────────────────
SYSTEM_PROMPT = """You are SkillSense AI...

Follow full structured assessment flow.
Do not use markdown tables.
Use bullet points only.
"""

# ── HELPER FUNCTION (FIXED) ────────────────────────────
def call_llm(messages):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/auto",
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
                "max_tokens": 2000
            }
        )

        data = response.json()

        if "choices" not in data:
            return f"API Error: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return str(e)

# ── SESSION STATE ──────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.stage = "start"
    st.session_state.greeted = False
    st.session_state.email_sent = False

# ── GREETING ───────────────────────────────────────────
if not st.session_state.greeted:
    greeting = "👋 Hi! Paste Job Description to begin 🚀"
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.session_state.greeted = True

# ── STATUS ─────────────────────────────────────────────
stage_labels = {
    "start": "📋 Paste Job Description",
    "jd_received": "📄 Paste Resume",
    "resume_received": "🔍 Assessment Starting",
    "assessing": "💬 Assessment in Progress",
    "complete": "✅ Done"
}
st.markdown(f"<div class='status-box'>{stage_labels.get(st.session_state.stage)}</div>", unsafe_allow_html=True)

# ── CHAT DISPLAY ───────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── INPUT ──────────────────────────────────────────────
if prompt := st.chat_input("Type here..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Stage control
    user_count = len([m for m in st.session_state.messages if m["role"] == "user"])

    if user_count == 1:
        st.session_state.stage = "jd_received"
    elif user_count == 2:
        st.session_state.stage = "resume_received"
    else:
        st.session_state.stage = "assessing"

    # Email handling
    if "@" in prompt and "." in prompt:
        reply = "Your personalised assessment report has been sent! Best of luck!"
        st.session_state.stage = "complete"
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = call_llm(st.session_state.messages)
                st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ── SIDEBAR ────────────────────────────────────────────
with st.sidebar:
    st.write("### Flow")
    st.write("""
1. JD  
2. Resume  
3. Questions  
4. Analysis  
5. Plan  
""")

    if st.button("Reset"):
        st.session_state.clear()
        st.rerun()
