import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
from utils import convert_abbr_to_int
plt.rcParams.update({
    'font.size': 10,
    'axes.titlesize': 10,
    'axes.labelsize': 7,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16,
    'font.family': 'Comic Sans MS'
})
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Arial', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)



st.title("Application Visualizations")
df1 = st.session_state.get("google_play")
df2 = st.session_state.get("producthunt")
df3 = st.session_state.get("github")

if "google_play" not in st.session_state:
    st.warning("No data available. Please perform a search in the Results tab first.")
    st.stop()



st.sidebar.header("Filters pour Google Play")
app_ids = df1["appId"].tolist()
selected_ids = st.sidebar.multiselect("Filter by Application ID:", app_ids, default=app_ids)
filtered_df1 = df1[df1["appId"].isin(selected_ids)]
st.sidebar.header("Filters pour Product Hunt")
app_ids = df2["title"].tolist()
selected_ids = st.sidebar.multiselect("Filter by Application title:", app_ids, default=app_ids)
filtered_df2 = df2[df2["title"].isin(selected_ids)]
st.sidebar.header("Filters pour GitHub")
app_ids = df3["name"].tolist()
selected_ids = st.sidebar.multiselect("Filter by Application name:", app_ids, default=app_ids)
filtered_df3 = df3[df3["name"].isin(selected_ids)]
st.markdown("<h3 style='color: steelblue;'>Google Play Store Data</h3>", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs([
    "Rating Distribution",
    "Free vs Paid Apps",
    "Top Apps by Installs",
    "Word Cloud"
])

# Rating Distribution
with tab1:
    st.subheader("Distribution of App Ratings")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.histplot(filtered_df1["score"].dropna(), bins=10, kde=False, ax=ax1, color="royalblue")
    ax1.set_xlabel("Rating")
    ax1.set_ylabel("Number of Apps")
    ax1.set_title("App Ratings Histogram")
    st.pyplot(fig1)

# Free vs Paid
with tab2:
    st.subheader("Free vs Paid Applications")
    paid_free_counts = filtered_df1["free"].value_counts()
    labels = ["Free" if is_free else "Paid" for is_free in paid_free_counts.index]
    fig2, ax2 = plt.subplots(figsize=(2, 2))
    ax2.pie(paid_free_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=["lightgreen", "lightcoral"])
    ax2.axis("equal")
    ax2.set_title("Free vs Paid Distribution")
    st.pyplot(fig2)

# Top Apps by Installs
with tab3:
    st.subheader("Top 5 Applications by Install Count")
    top_apps = filtered_df1[["title", "installs"]].sort_values(by="installs", ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="installs", y="title", data=top_apps, palette="magma", ax=ax)
    ax.set_title("Top 5 Apps by Installs")
    ax.set_xlabel("Installs")
    ax.set_ylabel("Application Title")
    st.pyplot(fig)

# Word Cloud
with tab4:
    st.subheader("Word Cloud from App Descriptions")
    text = " ".join(filtered_df1["description"].dropna().tolist())
    wordcloud = WordCloud(background_color='white', width=600, height=300).generate(text)
    fig3, ax3 = plt.subplots()
    ax3.imshow(wordcloud, interpolation='bilinear')
    ax3.axis("off")
    st.pyplot(fig3)

# Product Hunt
st.markdown("<h3 style='color: steelblue;'>Product Hunt Data</h3>", unsafe_allow_html=True)

if "producthunt" not in st.session_state:
    st.warning("No data available. Please perform a search in the Results tab first.")
    st.stop()

tabs1, tabs2, tabs3 ,tabs4= st.tabs([
    "Followers per Product",
    "Star Rating Distribution",
    "Word Cloud from Descriptions",
    "Top 10 Products by Followers"
])

with tabs1:
    df_clean = filtered_df2[filtered_df2['followers'] != "NONE"].copy()
    df_clean["followers"] = df_clean["followers"].str.replace("followers", "", regex=False).str.replace(",", "")
    df_clean["followers"] = df_clean["followers"].apply(convert_abbr_to_int)
    df_clean = df_clean.sort_values("followers", ascending=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(df_clean["title"], df_clean["followers"], color='skyblue')
    ax.set_xlabel("Followers")
    ax.set_title("Number of Followers per Product")
    st.pyplot(fig)

with tabs2:
    df_rating = filtered_df2[filtered_df2["rating"].notnull()]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df_rating["rating"], bins=[0, 1, 2, 3, 4, 5], edgecolor='black', color="orange")
    ax.set_title("Star Rating Distribution")
    ax.set_xlabel("Stars")
    ax.set_ylabel("Number of Products")
    st.pyplot(fig)

with tabs3:
    text = " ".join(filtered_df2["more_details"].dropna().tolist())
    wordcloud = WordCloud(width=600, height=300, background_color="white").generate(text)
    st.image(wordcloud.to_array(), use_container_width=True)

with tabs4:
    st.subheader("Top 5 Products by Followers")
    df_clean = filtered_df2[filtered_df2['followers'] != "NONE"].copy()
    df_clean["followers"] = df_clean["followers"].str.replace("followers", "", regex=False).str.replace(",", "")
    df_clean["followers"] = df_clean["followers"].apply(convert_abbr_to_int)
    df_clean = df_clean.sort_values("followers", ascending=False).head(5)
    
    st.dataframe(df_clean[["title", "tagline", "followers"]])
st.markdown("<h3 style='color: steelblue;'>GitHub Data</h3>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Language Distribution",
    "Top GitHub Projects",
    "Word Cloud from Descriptions",
    "Scatter Plot: Stars",
    "Heatmap: Stars by Language and Repo"
])


if "github" not in st.session_state:
    st.warning("No data available. Please perform a search in the Results tab first.")
    st.stop()

with tab1:
    lang_counts = filtered_df3["language"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(lang_counts, labels=lang_counts.index, autopct="%1.1f%%", startangle=140, colors=sns.color_palette("pastel"))
    ax.axis("equal")
    plt.title("Language Usage Distribution")
    st.pyplot(fig)

with tab2:
    top_starred = filtered_df3.sort_values("stars", ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=top_starred, x="stars", y="name", palette="coolwarm", ax=ax)
    ax.set_title("Top GitHub Projects by Stars")
    ax.set_xlabel("Stars")
    ax.set_ylabel("Repository Name")
    st.pyplot(fig)

with tab3:
    text = " ".join(filtered_df3["description"].dropna())
    wordcloud = WordCloud(background_color="white", max_words=100, width=600, height=300).generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

with tab4:
    fig = px.scatter(
        filtered_df3,
        x="stars",
        y="stars",
        hover_name="name",
        color="language",
        size="stars",
        title="GitHub Project Stars by Language"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    heatmap_data = filtered_df3.pivot_table(index="language", columns="full_name", values="stars", fill_value=0)
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Repository", y="Language", color="Stars"),
        aspect="auto",
        color_continuous_scale="Blues"
    )
    st.subheader("Heatmap of GitHub Stars by Language and Repository")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("See explanation"):
        st.write('''
            This heatmap visualizes the number of GitHub stars for each repository across programming languages.
            Darker shades represent repositories with higher star counts.
            It helps identify which projects are more popular within each language category.
        ''')