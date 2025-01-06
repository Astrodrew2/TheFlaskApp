import streamlit as st
import os
import pickle
import git
import pandas as pd
import RooDrink as rd
import numpy as np
import matplotlib.pyplot as plt

# Path to the local repository
REPO_PATH = './repo'  # Local clone of your GitHub repository
PICKLE_FILE = "drink_data.pkl"

# GitHub repo URL (make sure the repo is public or the user has access)
REPO_URL = "https://github.com/yourusername/yourrepo.git"

# Load data from the pickle file
def load_data():
    if os.path.exists(os.path.join(REPO_PATH, PICKLE_FILE)):
        with open(os.path.join(REPO_PATH, PICKLE_FILE), "rb") as f:
            return pickle.load(f)
    return {"name": [], "beer": [], "wine": [], "whiskey": [], "username": []}

# Save data to the pickle file
def save_data(data):
    with open(os.path.join(REPO_PATH, PICKLE_FILE), "wb") as f:
        pickle.dump(data, f)

# Pull the latest version of the repository
def pull_repo():
    repo = git.Repo(REPO_PATH)
    origin = repo.remotes.origin
    origin.pull()

# Push the changes to the repository
def push_repo():
    repo = git.Repo(REPO_PATH)
    origin = repo.remotes.origin
    repo.git.add(PICKLE_FILE)
    repo.index.commit("Updated drink data")
    origin.push()

# Initialize the repository (Clone if it does not exist)
if not os.path.exists(REPO_PATH):
    git.Repo.clone_from(REPO_URL, REPO_PATH)

# Load existing data from the pickle file in the repo
data = load_data()

# Title
st.title("Interactive Drink Rating App with GitHub Integration")

# Instructions
st.markdown("### Add your drink ratings below:")
st.markdown("**Note**: You must add a rating for all categories (Beer, Wine, Whiskey).")

# Input form
with st.form("drink_form"):
    name = st.text_input("Drink Name(s) (comma-separated)", "")
    beer = st.text_input("Beer Ratings (comma-separated)", "")
    wine = st.text_input("Wine Ratings (comma-separated)", "")
    whiskey = st.text_input("Whiskey Ratings (comma-separated)", "")
    urname = st.text_input("User Names (comma-separated)", "")

    # Submit button
    submitted = st.form_submit_button("Submit Ratings")

# Process the form submission
if submitted:
    try:
        # Parse input strings into lists
        name_list = [n.strip() for n in name.split(",") if n.strip()]
        beer_list = [int(b.strip()) for b in beer.split(",") if b.strip()]
        wine_list = [int(w.strip()) for w in wine.split(",") if w.strip()]
        whiskey_list = [int(w.strip()) for w in whiskey.split(",") if w.strip()]
        user_list = [u.strip() for u in urname.split(",") if u.strip()]

        # Validate input lengths
        if not (len(name_list) == len(beer_list) == len(wine_list) == len(whiskey_list) == len(user_list)):
            st.error("All input fields must have the same number of entries!")
        else:
            # Update the data dictionary with the new entries
            data["name"].extend(name_list)
            data["beer"].extend(beer_list)
            data["wine"].extend(wine_list)
            data["whiskey"].extend(whiskey_list)
            data["username"].extend(user_list)

            # Save updated data to the pickle file
            save_data(data)

            # Push the changes to GitHub
            push_repo()

            st.success("Ratings added and pushed to GitHub successfully!")

    except ValueError:
        st.error("Please ensure all numeric fields are properly formatted (e.g., only numbers for ratings).")

# Display current data
if data["name"]:
    st.markdown("### Current Ratings Data")
    df = pd.DataFrame(data)
    st.dataframe(df)

    # Generate and display the rating plot
    st.markdown("### Drink Ratings Visualization")
    rd.DrinkRating(data["name"], data["beer"], data["wine"], data["whiskey"], data["username"])
    plt.tight_layout()
    st.pyplot(plt)
else:
    st.info("No data available yet. Add some ratings!")