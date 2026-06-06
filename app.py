import streamlit as st
import pandas as pd
import plotly.express as px

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

    return round(
        (
            df["placement_status"]
            .eq("Placed")
            .mean()
        ) * 100,
        2
    )

def get_avg_salary(df):

    return round(
        df["salary_package_lpa"].mean(),
        2
    )

def get_top_branch(df):

    return (
        df["branch"]
        .value_counts()
        .idxmax()
    )

def get_top_tier(df):

    return (
        df["college_tier"]
        .value_counts()
        .idxmax()
    )

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title(
    "🎓 Alumni Career Path Tracker"
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
        "Leaderboard",
         "Placement Insights",
        "Dataset Explorer"
    ]
)

# --------------------------------
# DASHBOARD
# --------------------------------

if page == "Dashboard":

    st.title(
        "🎓 Alumni Career Path Tracker"
    )
    st.markdown("""
<div style="
padding:20px;
border-radius:15px;
background-color:#1E3A8A;
color:white;
text-align:center;
">

<h2>🚀 Welcome to CareerFlow AI</h2>

<p>
AI-Powered Alumni Intelligence Platform
</p>

<p>
📊 Placement Analytics | 🤖 Career Prediction |
🚀 AI Career Advisor | 🏆 Leaderboard
</p>

</div>
""", unsafe_allow_html=True)

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

    st.markdown(
        """
        ### CareerFlow AI

        AI-Powered Alumni Intelligence, Placement Analytics,
        Career Prediction & Employability Insights Platform
        """
    )
    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Placement Rate %",
        get_placement_rate(df)
    )

    c2.metric(
        "Average Salary",
        f"{get_avg_salary(df)} LPA"
    )

    c3.metric(
        "Top Branch",
        get_top_branch(df)
    )

    c4.metric(
        "Top Tier",
        get_top_tier(df)
    )
    st.subheader("📈 Placement Overview")

    fig = px.histogram(
        df,
        x="placement_status",
        color="placement_status",
        title="Placement Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        fig = px.histogram(
            df,
            x="branch",
            title="Students by Branch"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.pie(
            df,
            names="college_tier",
            title="College Tier Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# --------------------------------
# PLACEMENT ANALYTICS
# --------------------------------

elif page == "Placement Analytics":

    st.header(
        "📊 Placement Analytics"
    )

    fig = px.scatter(
        df,
        x="cgpa",
        y="coding_skill_score",
        color="placement_status",
        title="CGPA vs Coding Skill"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig = px.box(
        df,
        x="branch",
        y="cgpa",
        title="Branch vs CGPA"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------
# SALARY ANALYTICS
# --------------------------------

elif page == "Salary Analytics":

    st.header(
        "💰 Salary Analytics"
    )

    fig = px.histogram(
        df,
        x="salary_package_lpa",
        nbins=30,
        title="Salary Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    salary_branch = (
        df.groupby("branch")
        ["salary_package_lpa"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        salary_branch,
        x="branch",
        y="salary_package_lpa",
        title="Average Salary by Branch"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------
# SKILL INTELLIGENCE
# --------------------------------

elif page == "Skill Intelligence":

    st.header(
        "🚀 Skill Intelligence"
    )

    skills = {
        "Coding":
        df["coding_skill_score"].mean(),

        "Communication":
        df["communication_skill_score"].mean(),

        "Aptitude":
        df["aptitude_score"].mean(),

        "Leadership":
        df["leadership_score"].mean(),

        "Logical Reasoning":
        df["logical_reasoning_score"].mean()
    }

    skill_df = pd.DataFrame(
        {
            "Skill": skills.keys(),
            "Score": skills.values()
        }
    )

    fig = px.bar(
        skill_df,
        x="Skill",
        y="Score",
        title="Average Skill Scores"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------
# DATASET EXPLORER
# --------------------------------
# --------------------------------
# PLACEMENT INSIGHTS
# --------------------------------

elif page == "Placement Insights":

    st.header("📈 Placement Insights")

    placed_df = df[
        df["placement_status"] == "Placed"
    ]

    branch_salary = (
        placed_df.groupby("branch")
        ["salary_package_lpa"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        branch_salary,
        x="branch",
        y="salary_package_lpa",
        title="Average Salary by Branch"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
elif page == "Dataset Explorer":

    st.header(
        "📁 Dataset Explorer"
    )

    st.dataframe(df)

    st.write(
        "Rows:",
        df.shape[0]
    )

    st.write(
        "Columns:",
        df.shape[1]
    )

    st.write(
        "Columns Available"
    )

    st.write(
        df.columns.tolist()
    )
    # --------------------------------
# LEADERBOARD
# --------------------------------

elif page == "Leaderboard":

    st.header("🏆 Top Talent Leaderboard")

    top_students = (
        df.sort_values(
            "careerflow_score",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_students[
            [
                "student_id",
                "branch",
                "careerflow_score",
                "salary_package_lpa"
            ]
        ]
    )

# --------------------------------
# CAREER PREDICTOR
# --------------------------------

elif page == "Career Predictor":

    st.header("🤖 Career Predictor")

    cgpa = st.slider(
        "CGPA",
        0.0,
        10.0,
        7.0
    )

    coding = st.slider(
        "Coding Skill",
        0,
        100,
        50
    )

    aptitude = st.slider(
        "Aptitude",
        0,
        100,
        50
    )

    communication = st.slider(
        "Communication",
        0,
        100,
        50
    )

    score = (
        cgpa * 10 +
        coding +
        aptitude +
        communication
    ) / 4

    st.metric(
        "Employability Score",
        round(score, 2)
    )

    if score > 75:
        st.success(
            "High Placement Probability"
        )

    elif score > 60:
        st.warning(
            "Moderate Placement Probability"
        )

    else:
        st.error(
            "Low Placement Probability"
        )

# --------------------------------
# AI CAREER ADVISOR
# --------------------------------

elif page == "AI Career Advisor":

    st.header("🚀 AI Career Advisor")

    cgpa = st.number_input(
        "CGPA",
        0.0,
        10.0,
        7.0
    )

    coding = st.number_input(
        "Coding Score",
        0,
        100,
        60
    )

    if cgpa < 8:
        st.info(
            "Improve CGPA for better placement opportunities."
        )

    if coding < 70:
        st.info(
            "Practice DSA and build more projects."
        )

    st.success(
        "Recommended: Internship + Certification + Hackathons"
    )
    st.markdown("---")

st.markdown(
    """
    <center>
    <h4>🎓 CareerFlow AI</h4>
    <p>
    AI-Powered Alumni Intelligence Platform
    </p>
    <p>
    Built with Streamlit • Plotly • Python
    </p>
    </center>
    """,
    unsafe_allow_html=True
)
    
