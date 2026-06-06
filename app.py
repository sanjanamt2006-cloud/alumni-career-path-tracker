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
st.write(df["placement_status"].unique())

# --------------------------------
# HELPERS
# --------------------------------

def get_placement_rate(df):

    try:
        return round(
            (df["placement_status"] == 1).mean()*100,
            2
        )
    except:
        return 0

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

    st.markdown(
        """
        ### CareerFlow AI

        Alumni Intelligence • Placement Analytics •
        Employability Insights
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

    st.markdown("---")

    left,right = st.columns(2)

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
