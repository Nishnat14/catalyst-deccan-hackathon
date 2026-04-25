# catalyst-deccan-hackathon

🎯 SkillCheck AI

Built by Nishant Singh

SkillCheck AI is an AI-powered tool that checks how good a person really is at skills — not just what they claim in their resume.

It helps:

Evaluate real skill level
Find weak areas
Suggest what to learn next
Provide a step-by-step learning plan
📌 Problem

Today:

People list skills in resumes (but may not truly know them)
Recruiters spend too much time screening
Skill gaps are discovered too late

👉 Problem: We don’t know real skill level quickly

🚀 Solution

SkillCheck AI solves this by:

Taking Job Description + Resume
Asking smart, real-world questions
Evaluating answers
Giving skill scores
Finding weak areas
Creating a personalised learning plan
Sending the report via email
🔁 How It Works
Resume + Job Description
          ↓
AI extracts required skills
          ↓
AI asks questions
          ↓
Evaluates answers
          ↓
Gives score
          ↓
Finds weak skills
          ↓
Creates learning plan
          ↓
Sends email report
🧠 Core Logic
1. Skill Detection

AI reads the job description and finds required skills automatically.

2. Real Skill Assessment

Instead of asking:
❌ "Rate your Python skill"

It asks:
✔ "Explain how you used Python in a real project"

👉 This checks real understanding

📊 Skill Score (Graph Style)
Strong        █████
Medium        ███
Weak          █
📊 Example Output
SQL            █████   (Strong)
Python         ████    (Strong)
Communication  █████   (Strong)
Reporting      ███     (Needs Improvement)
📈 Impact
Time Comparison
Manual Process     █████████████████ (45–60 min)
SkillCheck AI      ███               (10–15 min)
Cost Comparison
Traditional        ███████████ (₹2000–5000)
SkillCheck AI      █           (Free)
Scalability
Manual Hiring      █ (1 user at a time)
SkillCheck AI      ███████████ (Unlimited users)
🔧 Tech Stack
Frontend: Streamlit
AI Engine: OpenRouter
Automation: n8n
Email: Gmail
Version Control: GitHub
🚀 How to Run
1. Clone the repository
git clone <your-repo-link>
cd <your-project-folder>
2. Install dependencies
pip install -r requirements.txt
3. Add API key

Create .streamlit/secrets.toml and add:

OPENROUTER_API_KEY="your-api-key"
4. Run the app
streamlit run app.py
💡 Features
AI-based skill evaluation
Real question-based assessment
Dynamic skill extraction
Personalized learning plan
Email report system
Works for any job role
👨‍💻 Author

Nishant Singh

📄 License

This project is built for hackathon purposes.
