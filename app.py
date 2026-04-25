import streamlit as st
import requests

# ── Page config ─────────────────────────────────────────
st.set_page_config(
    page_title="SkillCheck AI",
    page_icon="🎯",
    layout="centered"
)

# ── UI Styling ──────────────────────────────────────────
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

# ── Header ──────────────────────────────────────────────
st.title("🎯 SkillCheck AI")
st.write("AI Skill Assessment & Learning Plan Generator")
st.divider()

# ── API Key Check ───────────────────────────────────────
if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("API key missing. Add it in Streamlit secrets.")
    st.stop()

# ── SYSTEM PROMPT ───────────────────────────────────────
SYSTEM_PROMPT = """You are SkillCheck AI...

Follow full skill assessment flow.
Do not use markdown tables.
Keep output clean and structured.
"""

# ── Session State ───────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Chat Display ────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat Input ──────────────────────────────────────────
if prompt := st.chat_input("Enter Job Description / Resume / Answer..."):

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # ── Build Safe Messages ─────────────────────────────
    api_messages = []
    for m in st.session_state.messages:
        if "role" in m and "content" in m and m["content"]:
            api_messages.append({
                "role": str(m["role"]),
                "content": str(m["content"])
            })

    # ── API Call ───────────────────────────────────────
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "openrouter/auto",
                        "max_tokens": 2000,
                        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + api_messages
                    }
                )

                data = response.json()

                if "choices" not in data:
                    st.error(f"API Error: {data}")
                    st.stop()

                reply = data["choices"][0]["message"]["content"]

            except Exception as e:
                reply = f"Error: {str(e)}"

        st.markdown(reply)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    st.rerun()

# ── Sidebar ─────────────────────────────────────────────
with st.sidebar:
    st.header("How it works")
    st.write("""
1. Paste Job Description  
2. Paste Resume  
3. Answer questions  
4. Get skill analysis  
5. Receive learning plan  
""")

    if st.button("Reset"):
        st.session_state.messages = []
        st.rerun()

    st.caption("Built by Nishant Singh 🚀")



