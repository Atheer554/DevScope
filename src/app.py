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
st.markdown("""
<style>

.main {
    background-color: #121826;
}

h1 {
    color: #E9D8FD;
}

h2, h3 {
    color: #D6BCFA;
}

[data-testid="metric-container"] {
    background-color: #1E2538;
    border: 1px solid #B794F4;
    padding: 20px;
    border-radius: 15px;
}

[data-testid="stSidebar"] {
    background-color: #1A2030;
}

</style>
""", unsafe_allow_html=True)

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
# CHARTS
# ==========================

col1, col2 = st.columns(2)

# --------------------------
# DONUT CHART
# --------------------------

language_counts = df["language"].value_counts()

language_df = language_counts.reset_index()

language_df.columns = ["language", "count"]

fig_donut = px.pie(
    language_df,
    names="language",
    values="count",
    hole=0.4,
    title="💜 Language Distribution",
    color_discrete_sequence=[
        "#C4B5FD",
        "#A78BFA",
        "#D8B4FE",
        "#F0ABFC",
        "#F9A8D4",
        "#93C5FD",
        "#7DD3FC",
        "#A5B4FC"
    ]
)

fig_donut.update_layout(
    paper_bgcolor="#121826",
    plot_bgcolor="#121826",
    font_color="#E9D8FD"
)

# --------------------------
# BAR CHART
# --------------------------

top_repos = (
    df.sort_values("stars", ascending=False)
      .head(10)
)

fig_bar = px.bar(
    top_repos,
    x="stars",
    y="name",
    orientation="h",
    title="💜 Top Repositories"
)

fig_bar.update_traces(
    marker_color="#B794F4"
)

fig_bar.update_layout(
    paper_bgcolor="#121826",
    plot_bgcolor="#121826",
    font_color="#E9D8FD"
)

# --------------------------
# DISPLAY TOP ROW
# --------------------------

with col1:
    st.plotly_chart(
        fig_donut,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

# --------------------------
# SCATTER CHART
# --------------------------

fig_scatter = px.scatter(
    df,
    x="stars",
    y="forks",
    hover_name="name",
    title="💜 Stars vs Forks"
)

fig_scatter.update_traces(
    marker=dict(
        color="#C084FC",
        size=10
    )
)

fig_scatter.update_layout(
    paper_bgcolor="#121826",
    plot_bgcolor="#121826",
    font_color="#E9D8FD"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# ==========================
# DATA TABLE
# ==========================

with st.expander("📋 View Repository Data"):
    st.dataframe(df)