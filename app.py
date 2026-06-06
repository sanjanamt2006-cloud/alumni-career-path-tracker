import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

from utils.data_loader import load_data

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="Alumni Career Path Tracker",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------
# LOAD DATA
# --------------------------------

df = load_data()

df["careerflow_score"] = (
    df["cgpa"] * 10
    + df["coding_skill_score"]
    + df["aptitude_score"]
    + df["communication_skill_score"]
    + df["leadership_score"]
) / 5

# --------------------------------
# HELPERS
# --------------------------------
def get_placement_rate(df):
    return round((df["placement_status"].eq("Placed").mean()) * 100, 2)

def get_avg_salary(df):
    return round(df["salary_package_lpa"].mean(), 2)

def get_top_branch(df):
    return df["branch"].value_counts().idxmax()

def get_top_tier(df):
    return df["college_tier"].value_counts().idxmax()

# --------------------------------
# AI HELPER FUNCTION (Gemini API)
# --------------------------------
def ask_claude(prompt):
    import requests
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={st.secrets['GEMINI_API_KEY']}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"API Error: {result}"
# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("🎓 Alumni Career Path Tracker")
st.caption("Empowering Students with Data-Driven Career Intelligence 🚀")
st.sidebar.success("🚀 Welcome to CareerFlow AI")
st.sidebar.markdown("---")

st.sidebar.info(
    """
    💡 Quote of the Day

    Success is where preparation
    meets opportunity.
    """
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Placement Analytics",
        "Salary Analytics",
        "Skill Intelligence",
        "Career Predictor",
        "AI Career Advisor",
        "AI Chatbot",
        "Company Recommender",
        "Career Roadmap",
        "Leaderboard",
        "Placement Insights",
        "Dataset Explorer"
    ]
)

# --------------------------------
# DASHBOARD
# --------------------------------

if page == "Dashboard":

    st.title("🎓 Alumni Career Path Tracker")
    st.markdown("""
<div style="
padding:20px;
border-radius:15px;
background-color:#1E3A8A;
color:white;
text-align:center;
">
<h2>🚀 Welcome to CareerFlow AI</h2>
<p>AI-Powered Alumni Intelligence Platform</p>
<p>📊 Placement Analytics | 🤖 Career Prediction | 🚀 AI Career Advisor | 🏆 Leaderboard</p>
</div>
""", unsafe_allow_html=True)

    st.success("🎯 CareerFlow AI helps institutions analyze alumni career trends, employability skills, placement outcomes, and career growth opportunities.")

    st.markdown("### 🌟 Platform Features")
    hero1, hero2, hero3 = st.columns(3)
    hero1.success("📈 1000+ Alumni Records")
    hero2.info("🏢 200+ Companies")
    hero3.warning("💰 25 LPA Highest Package")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("""
        🤖 Career Predictor

        Predict employability using
        CGPA and skill metrics.
        """)

    with col2:
        st.success("""
        🚀 AI Career Advisor

        Personalized recommendations
        for career growth.
        """)

    with col3:
        st.warning("""
        🏆 Talent Leaderboard

        Rank students using
        CareerFlow Score.
        """)

    st.markdown("""
    ### 🎯 What This Platform Does

    ✔ Tracks Placement Trends

    ✔ Predicts Employability Score

    ✔ Provides AI Career Guidance

    ✔ Identifies Skill Gaps

    ✔ Highlights Top Talent

    ✔ Generates Career Insights

    ✔ Recommends Companies

    ✔ Generates Career Roadmaps

    ✔ AI Chatbot for Career Queries
    """)

    st.markdown("""
    ### CareerFlow AI

    AI-Powered Alumni Intelligence, Placement Analytics,
    Career Prediction & Employability Insights Platform
    """)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Placement Rate %", get_placement_rate(df))
    c2.metric("Average Salary", f"{get_avg_salary(df)} LPA")
    c3.metric("Top Branch", get_top_branch(df))
    c4.metric("Top Tier", get_top_tier(df))

    st.subheader("📈 Placement Overview")
    fig = px.histogram(df, x="placement_status", color="placement_status", title="Placement Distribution")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    left, right = st.columns(2)

    with left:
        fig = px.histogram(df, x="branch", title="Students by Branch")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.pie(df, names="college_tier", title="College Tier Distribution")
        st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# PLACEMENT ANALYTICS
# --------------------------------

elif page == "Placement Analytics":

    st.header("📊 Placement Analytics")

    fig = px.scatter(df, x="cgpa", y="coding_skill_score", color="placement_status", title="CGPA vs Coding Skill")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.box(df, x="branch", y="cgpa", title="Branch vs CGPA")
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# SALARY ANALYTICS
# --------------------------------

elif page == "Salary Analytics":

    st.header("💰 Salary Analytics")

    fig = px.histogram(df, x="salary_package_lpa", nbins=30, title="Salary Distribution")
    st.plotly_chart(fig, use_container_width=True)

    salary_branch = df.groupby("branch")["salary_package_lpa"].mean().reset_index()
    fig = px.bar(salary_branch, x="branch", y="salary_package_lpa", title="Average Salary by Branch")
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# SKILL INTELLIGENCE
# --------------------------------

elif page == "Skill Intelligence":

    st.header("🚀 Skill Intelligence")

    skills = {
        "Coding": df["coding_skill_score"].mean(),
        "Communication": df["communication_skill_score"].mean(),
        "Aptitude": df["aptitude_score"].mean(),
        "Leadership": df["leadership_score"].mean(),
        "Logical Reasoning": df["logical_reasoning_score"].mean()
    }

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=list(skills.values()), theta=list(skills.keys()), fill="toself"))
    fig.update_layout(title="🚀 Skill Radar Analysis")
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# CAREER PREDICTOR
# --------------------------------

elif page == "Career Predictor":

    st.header("🤖 Career Predictor")

    cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
    coding = st.slider("Coding Skill", 0, 100, 50)
    aptitude = st.slider("Aptitude", 0, 100, 50)
    communication = st.slider("Communication", 0, 100, 50)

    score = (cgpa * 10 + coding + aptitude + communication) / 4

    st.metric("Employability Score", round(score, 2))

    if score > 75:
        st.balloons()
        st.success("🎉 High Placement Probability")
    elif score > 60:
        st.warning("Moderate Placement Probability")
    else:
        st.error("Low Placement Probability")

# --------------------------------
# AI CAREER ADVISOR
# --------------------------------

elif page == "AI Career Advisor":

    st.header("🚀 AI Career Advisor")

    cgpa = st.number_input("CGPA", 0.0, 10.0, 7.0)
    coding = st.number_input("Coding Score", 0, 100, 60)

    if st.button("🎯 Get Career Advice"):
        if cgpa < 8:
            st.info("📚 Improve CGPA for better placement opportunities.")
        if coding < 70:
            st.info("💻 Practice DSA and build more projects.")

        st.success("🏆 Recommended Path")
        st.markdown("""
1️⃣ Complete Industry Internship

2️⃣ Earn Relevant Certifications

3️⃣ Participate in Hackathons

4️⃣ Build Portfolio Projects

5️⃣ Apply for Product & Service Companies
""")

    st.markdown("---")

# --------------------------------
# AI CHATBOT (Gemini API)
# --------------------------------

elif page == "AI Chatbot":

    st.header("🤖 AI Career Chatbot")
    st.markdown("Ask me anything about careers, placements, skills, or job market trends!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    user_input = st.chat_input("Ask your career question here...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                system_context = f"""You are CareerFlow AI, an expert alumni career advisor.
You help students with career guidance, placement preparation, skill building, and job market insights.
Dataset context: {df.shape[0]} alumni records, avg salary {get_avg_salary(df)} LPA, placement rate {get_placement_rate(df)}%.
Be concise, practical, and encouraging. Use emojis to make responses friendly."""

                full_prompt = f"{system_context}\n\nStudent question: {user_input}"

                try:
                    response = ask_claude(full_prompt)
                except Exception as e:
                    response = f"⚠️ Error: {str(e)}"

                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

# --------------------------------
# COMPANY RECOMMENDER
# --------------------------------

elif page == "Company Recommender":

    st.header("🏢 Smart Company Recommender")
    st.markdown("Get AI-powered company recommendations based on your profile!")

    col1, col2 = st.columns(2)

    with col1:
        branch = st.selectbox("Your Branch", df["branch"].unique())
        cgpa = st.slider("Your CGPA", 0.0, 10.0, 7.5)
        coding = st.slider("Coding Skill", 0, 100, 60)

    with col2:
        communication = st.slider("Communication Skill", 0, 100, 60)
        preferred_role = st.selectbox("Preferred Role", [
            "Software Engineer", "Data Analyst", "Product Manager",
            "DevOps Engineer", "UI/UX Designer", "Business Analyst"
        ])
        salary_expectation = st.slider("Expected Salary (LPA)", 3, 50, 10)

    if st.button("🔍 Find My Best Companies"):
        with st.spinner("AI is analyzing your profile..."):
            prompt = f"""You are a career placement expert. Based on this student profile, recommend exactly 6 companies.

Student Profile:
- Branch: {branch}
- CGPA: {cgpa}
- Coding Skill: {coding}/100
- Communication: {communication}/100
- Preferred Role: {preferred_role}
- Expected Salary: {salary_expectation} LPA

Give recommendations in this exact format for each company:
1. **Company Name** (Tier: Mass/Mid/Dream) - Role: [role] | Salary: [X-Y LPA] | Why: [one line reason]

Be specific, realistic, and helpful. Include a mix of easy, moderate, and dream companies."""

            try:
                response = ask_claude(prompt)
                st.success("🎯 Your Personalized Company Recommendations")
                st.markdown(response)
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

        st.markdown("---")
        st.markdown("### 📊 Companies from Our Alumni Data")
        if "company_name" in df.columns:
            top_companies = df[df["branch"] == branch]["company_name"].value_counts().head(10)
            fig = px.bar(
                x=top_companies.values,
                y=top_companies.index,
                orientation="h",
                title=f"Top Hiring Companies for {branch}",
                labels={"x": "Alumni Count", "y": "Company"}
            )
            st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# CAREER ROADMAP
# --------------------------------

elif page == "Career Roadmap":

    st.header("🗺️ AI Career Roadmap Generator")
    st.markdown("Get a personalized step-by-step career roadmap powered by AI!")

    col1, col2 = st.columns(2)

    with col1:
        branch = st.selectbox("Your Branch", df["branch"].unique())
        cgpa = st.slider("Current CGPA", 0.0, 10.0, 7.0)
        current_year = st.selectbox("Current Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])

    with col2:
        goal = st.selectbox("Career Goal", [
            "Software Engineer at FAANG",
            "Data Scientist / ML Engineer",
            "Product Manager",
            "DevOps / Cloud Engineer",
            "Startup Founder",
            "Higher Studies (MS/MBA)",
            "Government / PSU Jobs"
        ])
        skills_known = st.multiselect("Skills You Already Know", [
            "Python", "Java", "C++", "JavaScript", "SQL",
            "Machine Learning", "React", "Node.js", "Docker", "AWS"
        ])

    if st.button("🚀 Generate My Roadmap"):
        with st.spinner("AI is crafting your personalized roadmap..."):
            prompt = f"""You are an expert career coach for engineering students in India.
Create a detailed, actionable career roadmap for this student.

Student Profile:
- Branch: {branch}
- CGPA: {cgpa}
- Current Year: {current_year}
- Career Goal: {goal}
- Skills Known: {', '.join(skills_known) if skills_known else 'None mentioned'}

Create a roadmap with these sections:
## 🎯 Goal Analysis
## 📚 Skills to Learn (Priority Order)
## 🗓️ Month-by-Month Action Plan (next 6 months)
## 🏆 Milestones & Checkpoints
## 💼 Internship & Project Strategy
## 🔗 Resources & Platforms
## ⚠️ Common Mistakes to Avoid

Be specific, realistic for Indian engineering students, and motivating. Use emojis."""

            try:
                response = ask_claude(prompt)
                st.success("✅ Your Personalized Career Roadmap is Ready!")
                st.markdown(response)
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

        st.markdown("---")
        st.markdown("### 📊 Alumni Who Achieved Similar Goals")
        score = (cgpa * 10 + 60) / 2
        similar = df[df["careerflow_score"] >= score].head(5)
        if not similar.empty:
            st.dataframe(similar[["student_id", "branch", "careerflow_score", "salary_package_lpa"]])

# --------------------------------
# LEADERBOARD
# --------------------------------

elif page == "Leaderboard":

    st.header("🥇 Top Talent Leaderboard")
    st.success("Students ranked using CareerFlow AI Score")

    top_students = df.sort_values("careerflow_score", ascending=False).head(10)
    st.dataframe(top_students[["student_id", "branch", "careerflow_score", "salary_package_lpa"]])
    st.balloons()
    st.info("Top 10 students based on CareerFlow AI Score")

# --------------------------------
# PLACEMENT INSIGHTS
# --------------------------------

elif page == "Placement Insights":

    st.header("📈 Placement Insights")

    placed_df = df[df["placement_status"] == "Placed"]
    branch_salary = placed_df.groupby("branch")["salary_package_lpa"].mean().reset_index()

    fig = px.bar(branch_salary, x="branch", y="salary_package_lpa", title="Average Salary by Branch")
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# DATASET EXPLORER
# --------------------------------

elif page == "Dataset Explorer":

    st.header("📁 Dataset Explorer")
    st.dataframe(df)
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])
    st.write("Columns Available")
    st.write(df.columns.tolist())
