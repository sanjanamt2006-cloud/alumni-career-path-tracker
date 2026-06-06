import streamlit as st

from utils.data_loader import load_data
from utils.alumni_analytics import *

st.set_page_config(
    page_title="Alumni Career Path Tracker",
    page_icon="🎓",
    layout="wide"
)

df = load_data()

st.title(
    "🎓 Alumni Career Path Tracker"
)

st.subheader(
    "CareerFlow AI - Placement & Employability Analytics"
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

st.write(
    "Dataset Preview"
)

st.dataframe(
    df.head()
)
