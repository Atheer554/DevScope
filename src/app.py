import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# ==========================
# FUNCTIONS
# ==========================

def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.json()


def create_dataframe(data):
    repos = []

    for repo in data:
        repos.append({
            "name": repo["name"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"]
        })

    df = pd.DataFrame(repos)

    df["language"] = df["language"].fillna("Unknown")

    return df


# ==========================
# STREAMLIT UI
# ==========================
st.set_page_config(
    page_title="DevScope",
    page_icon="📊",
    layout="wide"
)

st.title("DevScope")
st.caption("Analyze GitHub repositories with interactive visualizations")

st.write("GitHub Repository Analytics Dashboard")

st.sidebar.header("Settings")

username = st.sidebar.text_input(
    "GitHub Username",
    value="microsoft"
)

# ==========================
# DATA LOADING
# ==========================

if username:

    with st.spinner("Fetching repositories..."):
      data = get_repositories(username)

    if data is not None:

        df = create_dataframe(data)

        # ==========================
        # KPI CARDS
        # ==========================

        avg_stars = round(df["stars"].mean(), 2)
        repo_count = len(df)
        max_stars = df["stars"].max()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Average Stars",
                avg_stars
            )

        with col2:
            st.metric(
                "Repositories",
                repo_count
            )

        with col3:
            st.metric(
                "Highest Stars",
                max_stars
            )

        # ==========================
        # CHART 1
        # ==========================

        language_counts = df["language"].value_counts()

        language_df = language_counts.reset_index()

        language_df.columns = ["language", "count"]

        fig = px.pie(
            language_df,
            names="language",
            values="count",
            hole=0.4,
            title="Language Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ==========================
        # CHART 2
        # ==========================

        top_repos = (
            df.sort_values("stars", ascending=False)
              .head(10)
        )

        fig = px.bar(
            top_repos,
            x="stars",
            y="name",
            orientation="h",
            title="Top Repositories by Stars"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ==========================
        # CHART 3
        # ==========================

        fig = px.scatter(
            df,
            x="stars",
            y="forks",
            hover_name="name",
            title="Stars vs Forks"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ==========================
        # DATA TABLE
        # ==========================

        st.subheader("Repository Data")

        st.dataframe(df)

    else:
        st.error("GitHub user not found")