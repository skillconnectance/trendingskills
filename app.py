import streamlit as st
import pandas as pd

# Set the title of the page
st.title("🔥 Trending Skills in GCC")

# Use the correct URL for the Trending Skills sheet
TRENDING_SKILLS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSciotZEMPUqnyLbEwFRZSOy4r6-2L7eKjkm4IvBW8pC6tVhzmBFM08jTIqVzVfn7klNfJEFpYV5oxz/pub?gid=2086370624&single=true&output=csv"

# Load the Trending Skills data from Google Sheets
try:
    df_trending_skills = pd.read_csv(TRENDING_SKILLS_URL)
except Exception as e:
    st.error(f"Error loading Trending Skills data: {e}")
    st.stop()

# Check the first few rows to verify the correct data is loaded
st.write("### Data Loaded:")
st.write(df_trending_skills.head())

# Ensure the "Occurrences" column exists before processing
if "Occurrences" in df_trending_skills.columns:
    # Sort and display top 10 trending skills
    top_skills = df_trending_skills.sort_values(by="Occurrences", ascending=False).head(10)
    st.write("### Top 10 Trending Skills (based on learner submissions):")
    st.dataframe(top_skills)

    # Create a bar chart for the top 10 skills
    st.write("### Trending Skills Visualization:")
    st.bar_chart(top_skills.set_index("Skill")["Occurrences"])
else:
    st.error("The 'Occurrences' column is missing or incorrectly named.")
