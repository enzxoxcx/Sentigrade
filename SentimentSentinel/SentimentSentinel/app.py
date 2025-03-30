import streamlit as st
from utils.sentiment_analyzer import supported_languages
from data.sea_countries import sea_countries, country_codes
import os

# Page configuration
st.set_page_config(
    page_title="Sentigrade - Southeast Asia Sentiment Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application title and introduction
st.title("Sentigrade - Southeast Asia Sentiment Analysis")

# Add logo
with st.sidebar:
    st.image("assets/sentigrade_logo.svg", width=200)
    st.subheader("Real-time Sentiment Analysis for Southeast Asia")
    
    # Language selection
    selected_language = st.selectbox(
        "Analysis Language",
        options=list(supported_languages.keys()),
        index=0,
        help="Select the language for sentiment analysis"
    )
    
    # Country/Region filter
    selected_countries = st.multiselect(
        "Countries/Regions",
        options=list(sea_countries.keys()),
        default=["Singapore"],
        help="Select countries or regions to analyze"
    )
    
    # Date range
    date_range = st.date_input(
        "Date Range",
        value=[],
        help="Select date range for analysis"
    )
    
    # Source selection
    source_options = ["Social Media", "News", "Press Releases", "All Sources"]
    selected_sources = st.multiselect(
        "Data Sources",
        options=source_options,
        default=["Social Media"],
        help="Select data sources to analyze"
    )
    
    # About section
    st.sidebar.markdown("---")
    st.sidebar.subheader("About Sentigrade")
    st.sidebar.info(
        """
        Sentigrade provides real-time sentiment analysis tailored for 
        Southeast Asian markets. Our platform helps businesses, political parties, 
        and organizations understand public sentiment across multiple languages and regions.
        """
    )

# Main content
st.markdown("""
## Welcome to Sentigrade - Southeast Asia Edition

Sentigrade is a sentiment analysis platform tailored specifically for Southeast Asia, designed to 
empower organizations with real-time insights into public opinion.

### Key Features:
- **Real-Time Sentiment Monitoring**: Track public sentiment as it unfolds
- **Multilingual Analysis**: Understand sentiment in multiple Southeast Asian languages
- **Comprehensive Dashboard**: Intuitive visualizations of sentiment trends and breakdowns
- **Regional Focus**: Tailored specifically for Southeast Asian markets
""")

# Dashboard overview section
st.header("Dashboard Overview")

# Create three columns for metrics
col1, col2, col3 = st.columns(3)

# Display metrics with conditional formatting based on sentiment
with col1:
    st.metric(
        label="Overall Sentiment Score", 
        value="N/A",
        delta=None,
        help="Overall sentiment score across all sources and regions"
    )

with col2:
    st.metric(
        label="Social Media Sentiment", 
        value="N/A",
        delta=None,
        help="Sentiment score from social media sources"
    )

with col3:
    st.metric(
        label="News Sentiment", 
        value="N/A",
        delta=None,
        help="Sentiment score from news sources"
    )

# Navigation instructions
st.markdown("""
### Navigate to Specific Analysis Pages:
- **Social Media Analysis**: Detailed sentiment analysis from social media platforms
- **News Analysis**: Sentiment trends from news outlets across Southeast Asia
- **Trend Analysis**: Historical trends and predictions for sentiment changes
""")

# Get started section
st.header("Get Started")
st.markdown("""
1. Select your preferred language from the sidebar
2. Choose countries/regions of interest
3. Set a date range for analysis
4. Select data sources to analyze
5. Navigate to specific analysis pages for detailed insights
""")

# Error/Empty state
if not selected_countries or not selected_sources:
    st.warning("Please select at least one country/region and data source to begin analysis.")

# Footer
st.markdown("---")
st.markdown("© 2023 Sentigrade. All rights reserved.")
