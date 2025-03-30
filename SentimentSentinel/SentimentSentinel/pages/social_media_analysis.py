import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.sentiment_analyzer import analyze_sentiment
from utils.data_processor import fetch_social_media_data, process_sentiment_data
from utils.visualization import create_sentiment_pie_chart, create_sentiment_timeline, create_word_cloud
from utils.language_detector import detect_language
from data.sea_countries import sea_countries, country_flags

# Page configuration
st.set_page_config(
    page_title="Social Media Analysis - Sentigrade",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page title
st.title("Social Media Sentiment Analysis")
st.markdown("Analyze sentiment from social media platforms across Southeast Asia")

# Sidebar filters
with st.sidebar:
    st.subheader("Data Filters")
    
    # Platform selection
    platforms = ["Twitter", "Facebook", "Instagram", "TikTok", "LinkedIn"]
    selected_platforms = st.multiselect(
        "Social Media Platforms",
        options=platforms,
        default=["Twitter", "Facebook"],
        help="Select social media platforms to analyze"
    )
    
    # Topic selection
    topics = ["Politics", "Economy", "Environment", "Health", "Technology", "Culture", "Other"]
    selected_topics = st.multiselect(
        "Topics",
        options=topics,
        default=["Politics", "Economy"],
        help="Select topics to analyze"
    )
    
    # Volume slider
    data_volume = st.slider(
        "Data Volume (posts)",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100,
        help="Select the volume of social media posts to analyze"
    )
    
    # Language filter (from main page)
    languages = ["English", "Bahasa Indonesia", "Bahasa Malaysia", "Thai", "Vietnamese", "Filipino", "Khmer"]
    selected_languages = st.multiselect(
        "Languages",
        options=languages,
        default=["English"],
        help="Select languages to include in analysis"
    )

# Main content
tab1, tab2, tab3 = st.tabs(["Sentiment Overview", "Detailed Analysis", "Content Explorer"])

# Sentiment Overview Tab
with tab1:
    st.subheader("Sentiment Distribution")
    
    # Check if filters are selected
    if not selected_platforms or not selected_topics or not selected_languages:
        st.warning("Please select at least one platform, topic, and language to view sentiment analysis.")
    else:
        # Add loading state
        with st.spinner("Analyzing social media sentiment..."):
            try:
                # Message about data fetching
                st.info("No data available. Please connect to a data source or upload data for analysis.")
                
                # Empty state visualizations with placeholders
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = go.Figure()
                    fig.add_trace(go.Pie(
                        labels=["Positive", "Neutral", "Negative"],
                        values=[0, 0, 0],
                        hole=.4,
                        marker_colors=["#4CAF50", "#FFC107", "#F44336"]
                    ))
                    fig.update_layout(
                        title="Sentiment Distribution (No Data)",
                        height=400,
                        margin=dict(l=20, r=20, t=40, b=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = go.Figure()
                    fig.update_layout(
                        title="Sentiment by Platform (No Data)",
                        xaxis_title="Platform",
                        yaxis_title="Count",
                        height=400,
                        margin=dict(l=20, r=20, t=40, b=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Geographic distribution
                st.subheader("Geographic Distribution")
                fig = go.Figure()
                fig.update_layout(
                    title="Sentiment by Country (No Data)",
                    height=450,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Message about empty data state
                st.markdown("""
                **To get started with real data:**
                1. Connect to a social media API
                2. Upload your own dataset
                3. Configure data collection parameters
                """)
            
            except Exception as e:
                st.error(f"Error analyzing social media data: {str(e)}")

# Detailed Analysis Tab
with tab2:
    st.subheader("Sentiment Trends Over Time")
    
    # Check if filters are selected
    if not selected_platforms or not selected_topics or not selected_languages:
        st.warning("Please select at least one platform, topic, and language to view detailed analysis.")
    else:
        # Add loading state
        with st.spinner("Generating detailed sentiment analysis..."):
            try:
                # Empty state for time series
                fig = go.Figure()
                fig.update_layout(
                    title="Sentiment Trends (No Data)",
                    xaxis_title="Date",
                    yaxis_title="Sentiment Score",
                    height=400,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Topic breakdown
                st.subheader("Sentiment by Topic")
                fig = go.Figure()
                fig.update_layout(
                    title="Topic Sentiment Analysis (No Data)",
                    xaxis_title="Topic",
                    yaxis_title="Sentiment Score",
                    height=400,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Message about empty data state
                st.info("Connect to a data source to view detailed sentiment trends and topic analysis.")
                
            except Exception as e:
                st.error(f"Error generating detailed analysis: {str(e)}")

# Content Explorer Tab
with tab3:
    st.subheader("Explore Social Media Content")
    
    # Search functionality
    search_query = st.text_input("Search for specific content or keywords")
    
    # Language detection demo
    if search_query:
        try:
            detected_lang = detect_language(search_query)
            sentiment_score = analyze_sentiment(search_query, "en")  # Default to English for demo
            
            st.write(f"Detected Language: {detected_lang}")
            st.write(f"Sentiment Score: {sentiment_score:.2f}")
            
            # Sentiment classification
            if sentiment_score > 0.05:
                st.success("Positive sentiment detected")
            elif sentiment_score < -0.05:
                st.error("Negative sentiment detected")
            else:
                st.info("Neutral sentiment detected")
                
        except Exception as e:
            st.error(f"Error analyzing text: {str(e)}")
    
    # Content table placeholder
    st.subheader("Top Posts")
    st.info("Connect to a data source to view and analyze actual social media content.")
    
    # Example table structure
    st.dataframe({
        "Platform": [],
        "Date": [],
        "Content": [],
        "Sentiment": [],
        "Engagement": []
    })
    
    st.markdown("""
    ### Content Analysis Features
    - Search for specific keywords or phrases
    - Filter content by sentiment score
    - Identify trending topics and hashtags
    - Analyze engagement metrics
    """)

# Add export functionality
st.sidebar.markdown("---")
st.sidebar.subheader("Export Options")
export_format = st.sidebar.selectbox(
    "Export Format",
    options=["CSV", "Excel", "JSON", "PDF Report"],
    index=0
)
if st.sidebar.button("Export Data"):
    st.sidebar.info("Export functionality will be enabled when connected to data sources.")

# Footer
st.markdown("---")
st.markdown("© 2023 Sentigrade. All rights reserved.")
