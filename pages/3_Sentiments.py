import streamlit as st
import pandas as pd
import plotly.express as px
from utils import compute_sentiments, compute_sentiment_score, get_reviews_by_app_id

st.set_page_config(page_title="Sentiment Analysis", layout="wide")
st.title("🧠 Sentiment Analysis of Apps")

# Retrieve previously searched apps
apps_df = st.session_state.get("google_play")

if apps_df is None or apps_df.empty:
    st.warning("No app data available. Please search first.")
    st.stop()

sentiment_results = []

with st.spinner("📊 Analyzing sentiments..."):
    for idx, row in apps_df.iterrows():
        try:
            reviews = get_reviews_by_app_id(row["appId"])
            sentiments = compute_sentiments(reviews)
            score = compute_sentiment_score(sentiments)

            sentiment_results.append({
                "title": row["title"],  # This is the app's name
                "appId": row["appId"],
                "score_sentiment": score.get("positive", 0),  # For the bar chart (positive sentiment)
                "n_reviews": len(reviews),
                "reviews": reviews,
                "sentiments": sentiments
            })

        except Exception as e:
            st.error(f"Error for {row['title']}: {e}")

# Create a DataFrame with the results
df_sentiments = pd.DataFrame(sentiment_results)
tab1, tab2 = st.tabs(["📊 Overview", "📈 Details"])

with tab1:
    # 📈 Bar chart of sentiment scores (positive only)
    fig = px.bar(df_sentiments, x="title", y="score_sentiment", color="score_sentiment",
                 color_continuous_scale="RdYlGn", title="Positive Sentiment Score of Apps" )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # 🔍 Details for a selected app
    selected_title = st.selectbox("Choose an app to see details:", df_sentiments["title"])
    selected = df_sentiments[df_sentiments["title"] == selected_title].iloc[0]

    st.subheader(f"Details for: {selected_title}")

    # Displaying reviews with their sentiment in a more readable format
    for rev, sent in zip(selected["reviews"], selected["sentiments"]):
        # Use a colored box for each review and sentiment
        sentiment_color = "green" if sent == "positive" else "red" if sent == "negative" else "gray"
        st.markdown(f"<div style='padding: 10px; border-radius: 5px; background-color: {sentiment_color}; color: white;'>"
                    f"<b>Sentiment:</b> {sent.capitalize()}<br>"
                    f"<b>Review:</b> {rev}</div>", unsafe_allow_html=True)