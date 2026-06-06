import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.alumni_analytics import *

st.set_page_config(
    page_title="Alumni Career Path Tracker",
    page_icon="🎓",
    layout="wide"
)

df = load_data()

# SIDEBAR

st.sidebar.title("🎓 Alumni Career Path Tracker")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Placement Analytics",
        "Salary Analytics"
    ]
)

# DASHBOARD

if page == "Dashboard":

    st.title("🎓 Alumni Career Path Tracker")

    st.markdown(
        """
        ### CareerFlow AI
        Alumni Intelligence, Placement Analytics &
        Employability Insights Platform
        """
    )

    col1,col2,col3,col4 = st.columns(4)

    col1.metric(
        "Placement Rate %",
        placement_rate(df)
    )

    col2.metric(
        "Average Salary",
        average_salary(df)
    )

    col3.metric(
        "Top Branch",
        top_branch(df)
    )

    col4.metric(
        "Top College Tier",
        top_college_tier(df)
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
            names="placement_status",
            title="Placement Status Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# PLACEMENT ANALYTICS

elif page == "Placement Analytics":

    st.header("📊 Placement Analytics")

    fig = px.box(
        df,
        x="branch",
        y="cgpa",
        color="placement_status",
        title="CGPA vs Placement"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig = px.scatter(
        df,
        x="coding_skill_score",
        y="salary_package_lpa",
        color="placement_status",
        title="Coding Skill vs Salary"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# SALARY ANALYTICS

elif page == "Salary Analytics":

    st.header("💰 Salary Analytics")

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

    avg_salary_branch = (
        df.groupby("branch")
        ["salary_package_lpa"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        avg_salary_branch,
        x="branch",
        y="salary_package_lpa",
        title="Average Salary by Branch"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
