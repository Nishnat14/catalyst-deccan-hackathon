import streamlit as st
import requests
import json

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="SkillCheck AI", page_icon="🎯")

if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("Missing API Key")
    st.stop()

API_KEY = st.secrets["OPENROUTER_API_KEY"]

SYSTEM_PROMPT = """
You are SkillCheck AI — an elite AI interviewer.

STRICT FLOW:

1. Extract skills from Job Description
2. Map Resume skills
3. Assess one skill at a time:
   - Ask 2 questions (concept + practical)
4. Wait for answers
5. Score skill (0–10)
6. Move to next skill

After all skills:
7. Generate:
   - Skill scores
   - Gap analysis
   - Personalized learning plan
   - Time estimates
   - Adjacent skills

Rules:
- Be structured
- No markdown tables
- Be concise
- Act like interviewer
"""

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "stage" not in st.session_state:
    st.session_state.stage = "jd"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "skills" not in st.session_state:
    st.session_state.skills = []

if "current_skill_index" not in st.session_state:
    st.session_state.current_skill_index = 0

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "answers" not in st.session_state:
    st.session_state.answers = {}

# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────
st.title("🎯 SkillCheck AI (Elite Version)")
st.write("AI-powered Skill Assessment + Learning Plan")

progress_map = {
    "jd": 10,
    "resume": 30,
    "assessment": 60,
    "evaluation": 80,
    "complete": 100
}

st.progress(progress_map.get(st.session_state.stage, 0))

# ─────────────────────────────────────────────
# HELPER: CALL LLM
# ─────────────────────────────────────────────
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
                "max_tokens": 1500
            }
        )

        data = response.json()

        if "choices" not in data:
            return f"Error: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return str(e)

# ─────────────────────────────────────────────
# STAGE 1: JOB DESCRIPTION
# ─────────────────────────────────────────────
if st.session_state.stage == "jd":
    jd = st.text_area("Paste Job Description")

    if st.button("Submit JD"):
        prompt = f"Extract top 5 skills from this JD:\n{jd}\nReturn as JSON list."

        reply = call_llm([{"role": "user", "content": prompt}])

        try:
            skills = json.loads(reply)
        except:
            skills = [s.strip("- ") for s in reply.split("\n") if s]

        st.session_state.skills = skills
        st.session_state.stage = "resume"
        st.success(f"Skills detected: {skills}")
        st.rerun()

# ─────────────────────────────────────────────
# STAGE 2: RESUME
# ─────────────────────────────────────────────
elif st.session_state.stage == "resume":
    resume = st.text_area("Paste Resume")

    if st.button("Start Assessment"):
        st.session_state.stage = "assessment"
        st.rerun()

# ─────────────────────────────────────────────
# STAGE 3: ASSESSMENT
# ─────────────────────────────────────────────
elif st.session_state.stage == "assessment":

    skills = st.session_state.skills
    idx = st.session_state.current_skill_index

    if idx >= len(skills):
        st.session_state.stage = "evaluation"
        st.rerun()

    current_skill = skills[idx]

    st.subheader(f"Assessing: {current_skill}")

    if current_skill not in st.session_state.answers:
        question_prompt = f"""
        Ask 2 interview questions for {current_skill}:
        1 conceptual
        1 practical
        """

        questions = call_llm([{"role": "user", "content": question_prompt}])

        st.session_state.answers[current_skill] = {
            "questions": questions,
            "user_answer": ""
        }

    st.write(st.session_state.answers[current_skill]["questions"])

    user_answer = st.text_area("Your Answer", key=current_skill)

    if st.button("Submit Answer"):
        st.session_state.answers[current_skill]["user_answer"] = user_answer

        eval_prompt = f"""
        Evaluate answer for {current_skill}.

        Answer: {user_answer}

        Give:
        Score (0-10)
        Short reason
        """

        result = call_llm([{"role": "user", "content": eval_prompt}])

        try:
            score = int([s for s in result.split() if s.isdigit()][0])
        except:
            score = 5

        st.session_state.scores[current_skill] = {
            "score": score,
            "feedback": result
        }

        st.session_state.current_skill_index += 1
        st.rerun()

# ─────────────────────────────────────────────
# STAGE 4: EVALUATION
# ─────────────────────────────────────────────
elif st.session_state.stage == "evaluation":

    st.subheader("📊 Skill Scores")

    for skill, data in st.session_state.scores.items():
        st.write(f"{skill}: {data['score']}/10")
        st.caption(data["feedback"])

    st.session_state.stage = "complete"

# ─────────────────────────────────────────────
# STAGE 5: LEARNING PLAN
# ─────────────────────────────────────────────
elif st.session_state.stage == "complete":

    st.subheader("🚀 Learning Plan")

    scores = st.session_state.scores

    weak_skills = [s for s in scores if scores[s]["score"] < 6]

    prompt = f"""
    Skills: {weak_skills}

    Create learning plan:
    - topics
    - resources
    - timeline
    - adjacent skills
    """

    plan = call_llm([{"role": "user", "content": prompt}])

    st.write(plan)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("Flow")
    st.write("""
    1. Job Description
    2. Resume
    3. Assessment
    4. Evaluation
    5. Learning Plan
    """)

    if st.button("Reset"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

