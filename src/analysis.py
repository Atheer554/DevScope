import requests
import pandas as pd
import plotly.express as px

# ==========================
# GET DATA FROM GITHUB API
# ==========================

url = "https://api.github.com/users/microsoft/repos"

response = requests.get(url)
data = response.json()

# ==========================
# EXTRACT ONLY NEEDED FIELDS
# ==========================

repos = []

for repo in data:
    repos.append({
        "name": repo["name"],
        "language": repo["language"],
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"]
    })

# ==========================
# CREATE DATAFRAME
# ==========================

df = pd.DataFrame(repos)

# Replace missing languages
df["language"] = df["language"].fillna("Unknown")

# ==========================
# BASIC ANALYSIS
# ==========================

print("\nAverage Stars:")
print(df["stars"].mean())

print("\nMost Starred Repository:")
print(df[df["stars"] == df["stars"].max()])

print("\nTop 5 Repositories:")
print(df.sort_values("stars", ascending=False).head(5))

print("\nLanguage Counts:")
print(df["language"].value_counts())

# ==========================
# CHART 1 - DONUT CHART
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

fig.show()

# ==========================
# CHART 2 - TOP REPOS BY STARS
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

fig.show()

# ==========================
# CHART 3 - STARS VS FORKS
# ==========================

fig = px.scatter(
    df,
    x="stars",
    y="forks",
    hover_name="name",
    title="Stars vs Forks"
)

fig.show()