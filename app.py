import streamlit as st
import pandas as pd

# Set the title of the page
st.title("🔥 Trending Skills in GCC")

# Google Sheets URL for Trending Skills (make sure this is a public CSV URL)
Trending_Skills_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSciotZEMPUqnyLbEwFRZSOy4r6-2L7eKjkm4IvBW8pC6tVhzmBFM08jTIqVzVfn7klNfJEFpYV5oxz/pub?output=csv"

# Load the Trending Skills data
try:
    df_trending_skills = pd.read_csv(Trending_Skills_SHEET_URL)
except Exception as e:
    st.error(f"Error loading Trending Skills data: {e}")
    st.stop()

# Sort the skills by Occurrences in descending order and get the top 10
top_skills = df_trending_skills.sort_values(by="Occurrences", ascending=False).head(10)

# Display the top 10 trending skills
st.write("### Top 10 Trending Skills (based on learner submissions):")
st.dataframe(top_skills)

# Visualization: Trending skills in a bar chart
st.write("### Visualization of Trending Skills:")
st.bar_chart(top_skills.set_index("Skill")["Occurrences"])
