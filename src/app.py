import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ==========================================
# PAGE SETUP & CONFIGURATION
# ==========================================
# Set the page to wide mode for a better dashboard layout
st.set_page_config(page_title="Influencer Analytics Dashboard", page_icon="📊", layout="wide")

# Dashboard Title and Business Context
st.title("🌟 Instagram Influencer Analytics Dashboard")
st.markdown("""
Welcome to the interactive **Instagram Influencer Analytics Dashboard**. 
This tool empowers marketing teams to discover the most valuable influencers for their campaigns.
By leveraging machine learning (K-Means clustering) and advanced metrics (Authenticity Score), 
you can filter out fake accounts, find highly engaged niche creators, and explore geographic trends.
""")

# ==========================================
# DATA LOADING & PREPARATION
# ==========================================
# Using st.cache_data ensures the dataset is only loaded once, improving app performance
@st.cache_data
def load_data():
    """
    Loads the segmented dataset exported from the Jupyter Notebook and calculates 
    on-the-fly metrics required for the dashboard.
    """
    df = pd.read_csv('data/processed/influencers_segmented.csv')
    
    # Feature Engineering: Authenticity Score
    # Story: 'engagement_avg' includes all interactions, while 'authentic_engagement' filters out bots.
    # By dividing the two, we get a percentage of "real" audience engagement.
    # We replace 0 with 1 in the denominator to avoid DivisionByZero errors.
    df['authenticity_score'] = df['authentic_engagement'] / df['engagement_avg'].replace(0, 1)
    
    # Cap the score at 100% (1.0) to handle any minor data anomalies from the original source
    df['authenticity_score'] = df['authenticity_score'].clip(upper=1.0)
    
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file not found! Please ensure you have run the Jupyter Notebook to export the CSV.")
    st.stop()

# ==========================================
# SIDEBAR: INTERACTIVE FILTERS
# ==========================================
st.sidebar.header("🔍 Advanced Filters")
st.sidebar.markdown("Use these filters to drill down into specific influencer demographics.")

# Segment Filter (e.g., Top Performers, Mega Celebrities)
segments = df['Segmento'].dropna().unique()
selected_segments = st.sidebar.multiselect("Filter by Business Segment:", options=segments, default=segments)

# Category Filter (e.g., Lifestyle, Sports, Music)
categories = [cat for cat in df['category_1'].dropna().unique() if cat != 'Unknown']
selected_categories = st.sidebar.multiselect("Filter by Content Category:", options=categories, default=categories)

st.sidebar.markdown("---")

# Bot Detection Filter
st.sidebar.markdown("### 🤖 Audience Quality")
st.sidebar.markdown("Enable this to hide accounts that likely purchased fake followers or likes.")
exclude_bots = st.sidebar.checkbox("Exclude Suspicious Accounts (Authenticity < 60%)", value=False)

# ------------------------------------------
# APPLYING FILTERS TO DATASET
# ------------------------------------------
df_filtered = df[(df['Segmento'].isin(selected_segments))]

if selected_categories:
    # Allow selected categories plus influencers where the category is Unknown
    df_filtered = df_filtered[(df_filtered['category_1'].isin(selected_categories)) | (df_filtered['category_1'] == 'Unknown')]

if exclude_bots:
    # Keep only highly authentic accounts
    df_filtered = df_filtered[df_filtered['authenticity_score'] >= 0.60]

st.markdown("---")

# ==========================================
# KEY PERFORMANCE INDICATORS (KPIs)
# ==========================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Influencers", f"{len(df_filtered):,}")
with col2:
    st.metric("Avg Engagement Rate", f"{df_filtered['engagement_rate'].mean()*100:.2f}%")
with col3:
    st.metric("Avg Audience Authenticity", f"{df_filtered['authenticity_score'].mean()*100:.1f}%")
with col4:
    st.metric("Avg Followers", f"{int(df_filtered['followers'].mean()):,}")

st.markdown("---")

# ==========================================
# SECTION 1: GEOSPATIAL ANALYSIS
# ==========================================
st.markdown("### 🌍 Global Reach: Where is the most engaged audience?")
st.markdown("This choropleth map highlights the average engagement rate by country. Lighter/Brighter colors indicate nations where followers are highly interactive, making them prime targets for localized marketing.")

# Group data by country to find the mean engagement rate
df_geo = df_filtered[df_filtered['audience_country(mostly)'] != 'Unknown']
geo_avg = df_geo.groupby('audience_country(mostly)')['engagement_rate'].mean().reset_index()

fig_map = px.choropleth(
    geo_avg, 
    locations="audience_country(mostly)", 
    locationmode="country names",
    color="engagement_rate",
    hover_name="audience_country(mostly)",
    color_continuous_scale=px.colors.sequential.Plasma,
    title="Average Engagement Rate by Country",
    height=700  # <--- Added height to make the map much bigger
)
# Reduce margins to maximize map size
fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
st.plotly_chart(fig_map, width='stretch')

st.markdown("---")

# ==========================================
# SECTION 2: BOT DETECTION (SCATTERPLOT)
# ==========================================
st.markdown("### 🤖 Bot Detection: Total vs Authentic Engagement")
st.markdown("The dashed line represents 100% authenticity. Influencers located far below the dashed line (in the red zone) possess high total engagement but very low genuine interactions, heavily implying the use of bots or spam networks.")

fig_bot = px.scatter(
    df_filtered, 
    x="engagement_avg", 
    y="authentic_engagement", 
    color="authenticity_score",
    hover_name="instagram_name",
    hover_data=["followers", "Segmento", "authenticity_score"],
    color_continuous_scale="RdYlGn", # Red for Low Authenticity, Green for High
    title="Authentic vs Average Engagement (Green = Real, Red = Suspicious)"
)
# Draw the ideal 1:1 ratio line
max_eng = df_filtered['engagement_avg'].max()
fig_bot.add_shape(type="line", x0=0, y0=0, x1=max_eng, y1=max_eng, line=dict(color="White", dash="dash"))

st.plotly_chart(fig_bot, width='stretch')

st.markdown("---")

# ==========================================
# SECTION 3: DISTRIBUTIONS & RANKINGS
# ==========================================
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("### 📊 Segment Distribution")
    st.markdown("Overview of how the filtered influencers are distributed across our K-Means clusters.")
    counts = df_filtered['Segmento'].value_counts().reset_index()
    counts.columns = ['Segment', 'Count']
    st.bar_chart(counts.set_index('Segment'))

with col_chart2:
    st.markdown("### 🏆 Top 10 Categories by Engagement")
    st.markdown("Which content niches drive the most interactions?")
    df_cat = df_filtered[df_filtered['category_1'] != 'Unknown']
    if not df_cat.empty:
        cat_avg = df_cat.groupby('category_1')['engagement_rate'].mean().sort_values(ascending=False).head(10).reset_index()
        st.bar_chart(cat_avg.set_index('category_1'))
    else:
        st.info("No valid categories found with current filters.")

st.markdown("---")

# ==========================================
# SECTION 4: RAW DATA EXPORT
# ==========================================
st.markdown("### 📋 Detailed Influencer Database")
st.markdown("Browse the raw data below. You can use the Streamlit interface to download this filtered view as a CSV for reporting.")
display_cols = ['influencer_insta_name', 'category_1', 'followers', 'engagement_rate', 'authenticity_score', 'Segmento']
st.dataframe(df_filtered[display_cols], width='stretch')
