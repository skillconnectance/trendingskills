import streamlit as st
import pandas as pd

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

# Set page configuration
st.set_page_config(page_title="Trending Skills & Trainer Recommender", layout="wide")

# Title
st.title("🔥 Trending Skills & Trainer Recommender")

# Load data from Google Sheets (public CSV URL)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSciotZEMPUqnyLbEwFRZSOy4r6-2L7eKjkm4IvBW8pC6tVhzmBFM08jTIqVzVfn7klNfJEFpYV5oxz/pub?output=csv"

# Load and process the data
try:
    df_trending_skills = pd.read_csv(CSV_URL)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Preprocess the trending skills data
df_trending_skills["Occurrences"] = df_trending_skills["Skill"].value_counts()
top_skills = df_trending_skills.groupby("Skill").agg({"Occurrences": "max"}).sort_values(by="Occurrences", ascending=False).head(10)

# Display Top 10 Trending Skills
st.subheader("🔥 Top 10 Trending Skills")
st.dataframe(top_skills)

# Trainer Recommender Section
st.subheader("🔍 Find Trainers Based on Skills")

# Load trainer data
trainer_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-Ar35mOmUWVi7sxlukLJLKtJ3WhtSx_dgEeB4GbNbOUAeTNKO0roiwUreM3sXFTnhlbRGM14yMqEP/pub?output=csv"
try:
    df_trainers = pd.read_csv(trainer_url)
except Exception as e:
    st.error(f"Error loading trainer data: {e}")
    st.stop()

# Preprocess the trainer data
df_trainers["Skills Taught"] = df_trainers["Skills Taught"].fillna("").apply(lambda x: [s.strip().lower() for s in x.split(",")])

# User input for Trainer Recommender
skills_input = st.text_input("🧠 Enter skills you're looking for (comma-separated):")
location_input = st.text_input("📍 Enter your location:")

if st.button("Find Trainers"):
    user_skills = [skill.strip().lower() for skill in skills_input.split(",") if skill.strip()]
    user_location = location_input.strip().lower()

    if not user_skills:
        st.warning("Please enter at least one skill.")
    else:
        # Match logic
        matches = df_trainers[df_trainers["Skills Taught"].apply(lambda skills: any(skill in skills for skill in user_skills))]

        # If a location is provided, filter trainers by city
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
