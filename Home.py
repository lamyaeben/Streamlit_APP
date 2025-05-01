import streamlit as st 
st.set_page_config(page_title="competitor Analysis App",  page_icon="📱", layout="centered")
st.title ("📱 Competitor Analysis App")

st.markdown("""
Welcome ! 
### Purpose:
Our application allows users to explore and analyze mobile applications 
based on a custom search query. It provides valuable insights into the competitive 
landscape by visualizing key app characteristics, helping users better
understand their market positioning.

### 📌 Key Features:
- Enter a search term (e.g., "note taking"...).
- Retrieve relevant applications through an API-based search system.
- Display the search results in an interactive data table.
- Explore multiple interactive charts: bar charts, pie charts, word clouds, and more.
- Analyze app categories, ratings distribution, free vs paid models, etc.

### How to Use the App:
1. Go to **Results Table** from the sidebar menu.
2. Enter your **search term** and fetch the results.
3. Then navigate to **Visualizations** to explore the data through graphs and charts.

*(Data is stored temporarily using Streamlit's session state to enable smooth navigation between pages.)*

### ⚙️ Technologies Used:
- **Python**
- **Streamlit**
- **Pandas** for data processing
- **Matplotlib**, **Seaborn**, and **WordCloud** for visualizations
- **API-based data retrieval** (from Lab 1 project)

### 💡 Future Improvements:
- Integrate additional data sources (ProductHunt, GitHub, etc.)
- Implement user authentication
- Enhance search filters (by price, category, minimum rating)
- Add options to save personalized dashboards

---
""")

st.info("👉 Use the sidebar menu to navigate between the different pages of the app.")





