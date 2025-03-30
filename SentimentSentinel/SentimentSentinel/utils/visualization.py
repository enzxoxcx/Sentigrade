import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from utils.sentiment_analyzer import get_sentiment_color

def create_sentiment_pie_chart(data, title="Sentiment Distribution"):
    """
    Create a pie chart showing sentiment distribution.
    
    Args:
        data (dict): Dictionary with sentiment categories as keys and counts as values
        title (str): Chart title
        
    Returns:
        Figure: Plotly figure object
    """
    if not data:
        # Return empty chart if no data
        fig = go.Figure(go.Pie(
            labels=["Positive", "Neutral", "Negative"],
            values=[0, 0, 0],
            hole=.4,
            marker_colors=["#4CAF50", "#FFC107", "#F44336"]
        ))
        fig.update_layout(
            title=title,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
        
    labels = list(data.keys())
    values = list(data.values())
    
    colors = ["#4CAF50" if label == "positive" else 
              "#FFC107" if label == "neutral" else 
              "#F44336" for label in labels]
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        marker_colors=colors
    ))
    
    fig.update_layout(
        title=title,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_sentiment_timeline(df, date_column, sentiment_column, title="Sentiment Over Time"):
    """
    Create a line chart showing sentiment over time.
    
    Args:
        df (DataFrame): DataFrame containing sentiment data
        date_column (str): Column containing dates
        sentiment_column (str): Column containing sentiment scores
        title (str): Chart title
        
    Returns:
        Figure: Plotly figure object
    """
    if df is None or df.empty:
        # Return empty chart if no data
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Sentiment Score",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
        
    # Ensure date column is datetime
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Sort by date
    df = df.sort_values(by=date_column)
    
    # Create chart
    fig = px.line(
        df, 
        x=date_column, 
        y=sentiment_column,
        title=title
    )
    
    # Add reference line for neutral sentiment
    fig.add_hline(
        y=0, 
        line_dash="dash", 
        line_color="gray",
        annotation_text="Neutral",
        annotation_position="bottom right"
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sentiment Score",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_word_cloud(words_with_weights, title="Top Words"):
    """
    Create a word cloud visualization. Since we can't create actual word clouds,
    this returns a bar chart of top words.
    
    Args:
        words_with_weights (dict): Dictionary with words as keys and weights as values
        title (str): Chart title
        
    Returns:
        Figure: Plotly figure object
    """
    if not words_with_weights:
        # Return empty chart if no data
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title="Word",
            yaxis_title="Frequency",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
        
    # Sort words by weight
    sorted_words = sorted(words_with_weights.items(), key=lambda x: x[1], reverse=True)
    
    # Take top 20 words
    top_words = dict(sorted_words[:20])
    
    # Create horizontal bar chart
    fig = px.bar(
        x=list(top_words.values()), 
        y=list(top_words.keys()),
        orientation='h',
        title=title
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Frequency",
        yaxis_title="Word",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_sentiment_heatmap(df, x_column, y_column, sentiment_column, title="Sentiment Heatmap"):
    """
    Create a heatmap showing sentiment across two dimensions.
    
    Args:
        df (DataFrame): DataFrame containing sentiment data
        x_column (str): Column for x-axis
        y_column (str): Column for y-axis
        sentiment_column (str): Column containing sentiment scores
        title (str): Chart title
        
    Returns:
        Figure: Plotly figure object
    """
    if df is None or df.empty:
        # Return empty chart if no data
        fig = go.Figure()
        fig.update_layout(
            title=title,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
        
    # Pivot data
    pivot = df.pivot_table(
        values=sentiment_column,
        index=y_column,
        columns=x_column,
        aggfunc='mean'
    )
    
    # Create heatmap
    fig = px.imshow(
        pivot,
        color_continuous_scale=["#F44336", "#FFC107", "#4CAF50"],
        title=title
    )
    
    # Update layout
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_source_comparison(df, source_column, sentiment_column, title="Sentiment by Source"):
    """
    Create a bar chart comparing sentiment across different sources.
    
    Args:
        df (DataFrame): DataFrame containing sentiment data
        source_column (str): Column containing source names
        sentiment_column (str): Column containing sentiment scores
        title (str): Chart title
        
    Returns:
        Figure: Plotly figure object
    """
    if df is None or df.empty:
        # Return empty chart if no data
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title="Source",
            yaxis_title="Average Sentiment",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
        
    # Group by source and calculate mean sentiment
    source_sentiment = df.groupby(source_column)[sentiment_column].mean().reset_index()
    
    # Sort by sentiment
    source_sentiment = source_sentiment.sort_values(by=sentiment_column)
    
    # Create chart
    fig = px.bar(
        source_sentiment, 
        x=source_column, 
        y=sentiment_column,
        title=title,
        color=sentiment_column,
        color_continuous_scale=["#F44336", "#FFC107", "#4CAF50"]
    )
    
    # Add reference line for neutral sentiment
    fig.add_hline(
        y=0, 
        line_dash="dash", 
        line_color="gray",
        annotation_text="Neutral",
        annotation_position="bottom right"
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Source",
        yaxis_title="Average Sentiment",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_trend_chart(df, date_column, country_column, sentiment_column, countries, title="Sentiment Trends"):
    """
    Create a line chart showing sentiment trends for multiple countries.
    
    Args:
        df (DataFrame): DataFrame containing sentiment data
        date_column (str): Column containing dates
        country_column (str): Column containing country names
        sentiment_column (str): Column containing sentiment scores
        countries (list): List of countries to include
        title (str): Chart title
        
    Returns:
        Figure: Plotly figure object
    """
    if df is None or df.empty:
        # Return empty chart if no data
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Sentiment Score",
            height=500,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
        
    # Ensure date column is datetime
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Filter for selected countries
    df = df[df[country_column].isin(countries)]
    
    # Sort by date
    df = df.sort_values(by=date_column)
    
    # Create chart
    fig = px.line(
        df, 
        x=date_column, 
        y=sentiment_column,
        color=country_column,
        title=title
    )
    
    # Add reference line for neutral sentiment
    fig.add_hline(
        y=0, 
        line_dash="dash", 
        line_color="gray",
        annotation_text="Neutral",
        annotation_position="bottom right"
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sentiment Score",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title="Country"
    )
    
    return fig

def create_forecast_chart(historical_df, forecast_df, date_column, sentiment_column, title="Sentiment Forecast"):
    """
    Create a line chart showing historical sentiment and forecast.
    
    Args:
        historical_df (DataFrame): DataFrame containing historical sentiment data
        forecast_df (DataFrame): DataFrame containing forecast sentiment data
        date_column (str): Column containing dates
        sentiment_column (str): Column containing sentiment scores
        title (str): Chart title
        
    Returns:
        Figure: Plotly figure object
    """
    fig = go.Figure()
    
    # Check if historical data exists
    if historical_df is not None and not historical_df.empty:
        # Ensure date column is datetime
        historical_df[date_column] = pd.to_datetime(historical_df[date_column])
        
        # Sort by date
        historical_df = historical_df.sort_values(by=date_column)
        
        # Add historical data
        fig.add_trace(go.Scatter(
            x=historical_df[date_column],
            y=historical_df[sentiment_column],
            name='Historical',
            line=dict(color='blue')
        ))
    
    # Check if forecast data exists
    if forecast_df is not None and not forecast_df.empty:
        # Ensure date column is datetime
        forecast_df[date_column] = pd.to_datetime(forecast_df[date_column])
        
        # Sort by date
        forecast_df = forecast_df.sort_values(by=date_column)
        
        # Add forecast data
        fig.add_trace(go.Scatter(
            x=forecast_df[date_column],
            y=forecast_df[sentiment_column],
            name='Forecast',
            line=dict(color='red', dash='dash')
        ))
    
    # Add reference line for neutral sentiment
    fig.add_hline(
        y=0, 
        line_dash="dash", 
        line_color="gray",
        annotation_text="Neutral",
        annotation_position="bottom right"
    )
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Sentiment Score",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # If no data, show empty chart with title
    if (historical_df is None or historical_df.empty) and (forecast_df is None or forecast_df.empty):
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Sentiment Score",
            height=500,
            margin=dict(l=20, r=20, t=40, b=20)
        )
    
    return fig
