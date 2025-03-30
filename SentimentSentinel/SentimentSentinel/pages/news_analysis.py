import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.sentiment_analyzer import analyze_sentiment, categorize_sentiment
from utils.data_processor import fetch_news_data, export_data
from utils.visualization import create_sentiment_heatmap, create_source_comparison, create_sentiment_timeline
from utils.news_api import fetch_and_analyze_news, setup_api_keys
from data.sea_countries import sea_countries
import os

# Page configuration
st.set_page_config(
    page_title="News Analysis - Sentigrade",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page title
st.title("News Media Sentiment Analysis")
st.markdown("Analyze sentiment from news sources across Southeast Asia")

# Check if API keys are configured
api_key, cse_id, gemini_api_key, api_configured = setup_api_keys()

# Sidebar filters
with st.sidebar:
    st.subheader("Data Filters")
    
    # News source selection
    news_sources = ["Major Publications", "Local News", "International Coverage", "Financial News", "Political News"]
    selected_sources = st.multiselect(
        "News Sources",
        options=news_sources,
        default=["Major Publications", "Local News"],
        help="Select news sources to analyze"
    )
    
    # Topic selection
    topics = ["Politics", "Economy", "International Relations", "Health", "Technology", "Environment", "Culture"]
    selected_topics = st.multiselect(
        "Topics",
        options=topics,
        default=["Politics", "Economy"],
        help="Select news topics to analyze"
    )
    
    # Country selection
    selected_countries = st.multiselect(
        "Countries",
        options=list(sea_countries.keys()),
        default=["Singapore", "Malaysia"],
        help="Select countries to analyze news from"
    )
    
    # Publication date range
    date_range = st.date_input(
        "Publication Date Range",
        value=[],
        help="Select date range for news analysis"
    )
    
    # API configuration section
    st.sidebar.markdown("---")
    st.sidebar.subheader("API Configuration")
    
    if not api_configured:
        st.sidebar.warning("Google API and CSE ID not configured. Add them to enable live news analysis.")
        if st.sidebar.button("Configure API Keys"):
            st.session_state.show_api_config = True
    else:
        st.sidebar.success("API keys configured! Live news analysis is available.")
        if st.sidebar.button("Update API Keys"):
            st.session_state.show_api_config = True

# API Configuration Modal
if "show_api_config" not in st.session_state:
    st.session_state.show_api_config = False

if st.session_state.show_api_config:
    with st.form("api_config_form"):
        st.subheader("Configure Google API Keys")
        google_api = st.text_input("Google API Key", type="password")
        cse_id = st.text_input("Google Custom Search Engine ID", type="password")
        gemini_api = st.text_input("Gemini API Key (optional, uses Google API Key if empty)", type="password")
        
        submit_api = st.form_submit_button("Save API Keys")
        
        if submit_api:
            # In Streamlit, we can't actually set environment variables permanently
            # However, we can create session state variables to simulate this experience
            st.session_state.google_api_key = google_api
            st.session_state.google_cse_id = cse_id
            st.session_state.gemini_api_key = gemini_api if gemini_api else google_api
            
            # Mock environment variable setting for this session only
            os.environ["GOOGLE_API_KEY"] = google_api
            os.environ["GOOGLE_CSE_ID"] = cse_id
            os.environ["GEMINI_API_KEY"] = gemini_api if gemini_api else google_api
            
            st.success("API keys have been saved for this session!")
            st.session_state.show_api_config = False
            st.rerun()

# Main content
tab1, tab2, tab3 = st.tabs(["News Sentiment Overview", "Publication Analysis", "Content Analysis"])

# News Sentiment Overview Tab
with tab1:
    st.subheader("News Sentiment Across Southeast Asia")
    
    # Check if filters are selected
    if not selected_sources or not selected_topics or not selected_countries:
        st.warning("Please select at least one source, topic, and country to view news sentiment analysis.")
    elif not api_configured:
        st.warning("API keys not configured. Please configure API keys to access live news data.")
        if st.button("Configure API Keys", key="tab1_config_button"):
            st.session_state.show_api_config = True
            st.rerun()
    else:
        # Add loading state
        with st.spinner("Analyzing news sentiment..."):
            try:
                # Convert topics and countries to search queries
                search_queries = []
                for topic in selected_topics:
                    for country in selected_countries:
                        search_queries.append(f"{topic}, {country}")
                
                # Get news data using the Google CSE API
                news_df = fetch_and_analyze_news(
                    queries=search_queries,
                    max_results_per_query=3,  # Limited to prevent API quota exhaustion
                    with_progress=True
                )
                
                if news_df.empty:
                    st.info("No news data found for the selected filters. Try different topics or countries.")
                else:
                    # Add sentiment categorization
                    news_df['sentiment_category'] = news_df['sentiment_score'].apply(categorize_sentiment)
                    
                    # Show some statistics
                    st.success(f"Found {len(news_df)} news articles for analysis.")
                    
                    # Visualizations
                    # Sentiment distribution
                    sentiment_counts = news_df['sentiment_category'].value_counts().to_dict()
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Sentiment pie chart
                        from utils.visualization import create_sentiment_pie_chart
                        fig = create_sentiment_pie_chart(sentiment_counts, "Sentiment Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Average sentiment by topic
                        topic_sentiment = news_df.groupby('query')['sentiment_score'].mean().reset_index()
                        topic_sentiment.columns = ['Topic', 'Average Sentiment']
                        
                        fig = px.bar(
                            topic_sentiment, 
                            x='Topic', 
                            y='Average Sentiment',
                            color='Average Sentiment',
                            color_continuous_scale=["#F44336", "#FFC107", "#4CAF50"],
                            title="Average Sentiment by Topic and Country"
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Source Analysis
                    st.subheader("News Source Analysis")
                    source_counts = news_df['source'].value_counts().reset_index()
                    source_counts.columns = ['Source', 'Count']
                    
                    fig = px.bar(
                        source_counts, 
                        x='Source', 
                        y='Count',
                        title="Article Count by Source",
                        color='Count',
                        color_continuous_scale="Viridis"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error analyzing news data: {str(e)}")

# Publication Analysis Tab
with tab2:
    st.subheader("Publication Analysis")
    
    # Check if filters are selected
    if not selected_sources or not selected_topics:
        st.warning("Please select at least one source and topic to view publication analysis.")
    elif not api_configured:
        st.warning("API keys not configured. Please configure API keys to access live news data.")
        if st.button("Configure API Keys", key="tab2_config_button"):
            st.session_state.show_api_config = True
            st.rerun()
    else:
        # Add loading state
        with st.spinner("Analyzing publications..."):
            try:
                # If we don't have data in session state, fetch it
                if "news_data" not in st.session_state or st.session_state.news_data is None:
                    # Convert topics and countries to search queries
                    search_queries = []
                    for topic in selected_topics:
                        for country in selected_countries:
                            search_queries.append(f"{topic}, {country}")
                    
                    # Get news data using the Google CSE API
                    news_df = fetch_and_analyze_news(
                        queries=search_queries,
                        max_results_per_query=3,  # Limited to prevent API quota exhaustion
                        with_progress=True
                    )
                    
                    # Store in session state to prevent repeat API calls
                    st.session_state.news_data = news_df
                else:
                    news_df = st.session_state.news_data
                
                if news_df.empty:
                    st.info("No news data found for the selected filters. Try different topics or countries.")
                else:
                    # Add sentiment categorization
                    news_df['sentiment_category'] = news_df['sentiment_score'].apply(categorize_sentiment)
                    
                    # Media outlet comparison
                    st.subheader("Media Outlet Sentiment Comparison")
                    
                    # Group by source and calculate average sentiment
                    source_sentiment = news_df.groupby('source')['sentiment_score'].agg(['mean', 'count']).reset_index()
                    source_sentiment.columns = ['Source', 'Average Sentiment', 'Article Count']
                    
                    # Filter sources with at least 2 articles for more meaningful comparison
                    source_sentiment_filtered = source_sentiment[source_sentiment['Article Count'] >= 1]
                    
                    if not source_sentiment_filtered.empty:
                        fig = px.bar(
                            source_sentiment_filtered,
                            x='Source',
                            y='Average Sentiment',
                            color='Average Sentiment',
                            color_continuous_scale=["#F44336", "#FFC107", "#4CAF50"],
                            title="Media Outlet Sentiment Comparison",
                            hover_data=['Article Count']
                        )
                        fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Neutral")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Not enough data to compare media outlets. Try selecting more topics or countries.")
                    
                    # Publication bias analysis
                    st.subheader("Topic Coverage Analysis")
                    
                    # Calculate topic coverage by source
                    topic_coverage = pd.crosstab(
                        news_df['source'], 
                        news_df['query']
                    ).reset_index()
                    
                    if not topic_coverage.empty and len(topic_coverage.columns) > 1:
                        # Melt for plotting
                        topic_coverage_melted = topic_coverage.melt(
                            id_vars=['source'],
                            var_name='Topic',
                            value_name='Count'
                        )
                        
                        fig = px.bar(
                            topic_coverage_melted,
                            x='source',
                            y='Count',
                            color='Topic',
                            title="Topic Coverage by Media Outlet",
                            barmode='group'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Not enough topic coverage data available.")
                
            except Exception as e:
                st.error(f"Error analyzing publications: {str(e)}")

# Content Analysis Tab
with tab3:
    st.subheader("News Content Analysis")
    
    # Search functionality
    search_query = st.text_input("Search for specific news topics or keywords")
    
    if not api_configured:
        st.warning("API keys not configured. Please configure API keys to access live news data.")
        if st.button("Configure API Keys", key="tab3_config_button"):
            st.session_state.show_api_config = True
            st.rerun()
    elif search_query:
        with st.spinner(f"Searching for news articles related to '{search_query}'..."):
            # Parse the search query into a list
            search_terms = [search_query]
            
            # Get news data
            search_results = fetch_and_analyze_news(
                queries=search_terms,
                max_results_per_query=5,
                with_progress=True
            )
            
            if search_results.empty:
                st.info(f"No news articles found matching '{search_query}'. Try a different search term.")
            else:
                # Add sentiment categorization
                search_results['sentiment_category'] = search_results['sentiment_score'].apply(categorize_sentiment)
                
                # Show the results in a nicely formatted way
                st.success(f"Found {len(search_results)} articles matching '{search_query}'")
                
                # Sentiment distribution
                sentiment_counts = search_results['sentiment_category'].value_counts().to_dict()
                
                # Pie chart
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Sentiment distribution
                    from utils.visualization import create_sentiment_pie_chart
                    fig = create_sentiment_pie_chart(sentiment_counts, "Sentiment Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Articles table with formatted sentiment
                    st.subheader("Search Results")
                    
                    # Create a styled dataframe
                    for idx, row in search_results.iterrows():
                        with st.container():
                            col1, col2 = st.columns([5, 1])
                            with col1:
                                st.markdown(f"#### [{row['title']}]({row['link']})")
                                st.markdown(f"**Source:** {row['source']} | **Date:** {row['date']}")
                                st.markdown(row['snippet'])
                            with col2:
                                # Display sentiment with color
                                sentiment = row['sentiment_category']
                                score = row['sentiment_score']
                                color = "#4CAF50" if sentiment == "positive" else "#F44336" if sentiment == "negative" else "#FFC107"
                                st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:5px; text-align:center; color:white;'><b>{sentiment.upper()}</b><br>{score:.2f}</div>", unsafe_allow_html=True)
                            st.markdown("---")
    else:
        # If user hasn't searched yet
        if "news_data" in st.session_state and st.session_state.news_data is not None and not st.session_state.news_data.empty:
            # Show the most recent data we have
            news_df = st.session_state.news_data
            news_df['sentiment_category'] = news_df['sentiment_score'].apply(categorize_sentiment)
            
            # Show top articles
            st.subheader("Top News Articles")
            
            # Sort by absolute sentiment score to get the most opinionated articles
            sorted_df = news_df.copy()
            sorted_df['abs_score'] = sorted_df['sentiment_score'].abs()
            sorted_df = sorted_df.sort_values('abs_score', ascending=False).head(5)
            
            # Display articles
            for idx, row in sorted_df.iterrows():
                with st.container():
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"#### [{row['title']}]({row['link']})")
                        st.markdown(f"**Source:** {row['source']} | **Date:** {row['date']}")
                        st.markdown(row['snippet'])
                    with col2:
                        # Display sentiment with color
                        sentiment = row['sentiment_category']
                        score = row['sentiment_score']
                        color = "#4CAF50" if sentiment == "positive" else "#F44336" if sentiment == "negative" else "#FFC107"
                        st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:5px; text-align:center; color:white;'><b>{sentiment.upper()}</b><br>{score:.2f}</div>", unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.info("Use the search box above to find news articles on specific topics.")
            
            # Example search suggestions
            st.markdown("### Search Suggestions:")
            suggestion_cols = st.columns(3)
            
            with suggestion_cols[0]:
                if st.button("Singapore Economy"):
                    # Set the search query and rerun
                    st.session_state.search_query = "Singapore Economy"
                    st.rerun()
            
            with suggestion_cols[1]:
                if st.button("Malaysia Politics"):
                    st.session_state.search_query = "Malaysia Politics"
                    st.rerun()
            
            with suggestion_cols[2]:
                if st.button("Indonesia Technology"):
                    st.session_state.search_query = "Indonesia Technology"
                    st.rerun()

# Add export functionality
st.sidebar.markdown("---")
st.sidebar.subheader("Export Options")
export_format = st.sidebar.selectbox(
    "Export Format",
    options=["CSV", "Excel", "JSON", "PDF Report"],
    index=0
)

# Enable export if we have data
if "news_data" in st.session_state and st.session_state.news_data is not None and not st.session_state.news_data.empty:
    if st.sidebar.button("Export Data"):
        # Convert format string to lowercase for our function
        format_str = export_format.lower().replace(" report", "")
        
        # Use our export function from data_processor
        export_path = export_data(st.session_state.news_data, format=format_str, filename="sentigrade_news_export")
        
        if export_path:
            st.sidebar.success(f"Data exported successfully as {export_format}!")
            
            # For formats other than PDF, provide download link
            if format_str != "pdf":
                with open(export_path, "rb") as file:
                    st.sidebar.download_button(
                        label=f"Download {export_format}",
                        data=file,
                        file_name=f"sentigrade_news_export.{format_str}",
                        mime=f"application/{format_str}"
                    )
        else:
            st.sidebar.error(f"Failed to export data as {export_format}.")
else:
    if st.sidebar.button("Export Data"):
        st.sidebar.info("No data available to export. Please fetch news data first.")

# Footer
st.markdown("---")
st.markdown("© 2023 Sentigrade. All rights reserved.")
