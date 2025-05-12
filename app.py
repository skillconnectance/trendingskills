import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import requests

# Skill to category mapping (you can expand this as needed)
skill_to_category = {
    "python": "Programming",
    "excel": "Programming",
    "java": "Programming",
    "soft skills": "Soft Skills",
    "communication": "Soft Skills",
    "leadership": "Soft Skills",
    "data analysis": "Data Science",
    "machine learning": "Data Science",
    "marketing": "Marketing",
    "sales": "Sales"
    # Add more skill-category mappings here...
}

# Streamlit setup
st.set_page_config(page_title="Trainer & Trending Skills", layout="wide")
st.title("🔍 Trainer & Trending Skills Recommender")

# Load data from Google Sheet (public CSV URLs)
CSV_URL_TRENDING = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-Ar35mOmUWVi7sxlukLJLKtJ3WhtSx_dgEeB4GbNbOUAeTNKO0roiwUreM3sXFTnhlbRGM14yMqEP/pub?gid=2086370624&single=true&output=csv"
CSV_URL_TRAINERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-Ar35mOmUWVi7sxlukLJLKtJ3WhtSx_dgEeB4GbNbOUAeTNKO0roiwUreM3sXFTnhlbRGM14yMqEP/pub?output=csv"

try:
    df_trending_skills = pd.read_csv(CSV_URL_TRENDING)
    df_trainers = pd.read_csv(CSV_URL_TRAINERS)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Process trending skills data
df_trending_skills = df_trending_skills[['Skill', 'Occurrences']]  # Only keep relevant columns
top_skills = df_trending_skills.sort_values(by="Occurrences", ascending=False).head(10)

# Preprocess the trainer data (Skills taught)
df_trainers["Skills Taught"] = df_trainers["Skills Taught"].fillna("").apply(lambda x: [s.strip().lower() for s in x.split(",")])

# Display trending skills
st.subheader("🔥 Top 10 Trending Skills")
for index, row in top_skills.iterrows():
    st.write(f"**{row['Skill']}** - {row['Occurrences']} Occurrences")

# User input for trainer recommendation
skills_input = st.text_input("🧠 Enter skills you're looking for (comma-separated):")
location_input = st.text_input("📍 Enter your location:")

if st.button("Find Trainers"):
    user_skills = [skill.strip().lower() for skill in skills_input.split(",") if skill.strip()]
    user_location = location_input.strip().lower()

    if not user_skills:
        st.warning("Please enter at least one skill.")
    else:
        # Match logic for trainers
        matches = df_trainers[df_trainers["Skills Taught"].apply(lambda skills: any(skill in skills for skill in user_skills))]

        if user_location:
            matches = matches[matches["City"].str.contains(user_location)]

        if not matches.empty:
            st.success(f"✅ Found {len(matches)} matching trainer(s):")
            for _, row in matches.iterrows():
                # Layout in two columns
                col1, col2 = st.columns([1, 3])

                with col1:
                    if isinstance(row['Profile Picture Upload'], str) and row['Profile Picture Upload'].startswith("http"):
                        st.image(row['Profile Picture Upload'], width=120)
                    else:
                        st.image("https://via.placeholder.com/120", width=120)

                with col2:
                    st.markdown(f"### {row['First Name']} {row['Last Name']}")
                    st.markdown(f"📍 **City:** {row['City'].capitalize()}")
                    st.markdown(f"📅 **Experience:** {row['Years of Experience']} years")
                    st.markdown(f"📝 **Bio:** {row['Short Bio']}")

                    # Show Skills with Categories
                    categories = set()
                    for skill in row['Skills Taught']:
                        category = skill_to_category.get(skill.strip(), "Uncategorized")
                        categories.add(category)
                    st.markdown(f"🛠️ **Skills by Categories:** {', '.join(categories)}")

                    # Show LinkedIn profile if available
                    if pd.notna(row['LinkedIn Profile URL']):
                        st.markdown(f"[🔗 Connect on LinkedIn]({row['LinkedIn Profile URL']})", unsafe_allow_html=True)

                st.markdown("---")
        else:
            st.warning("⚠️ No matching trainers found.")
