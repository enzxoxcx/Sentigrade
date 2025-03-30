import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import re

# Dictionary of supported languages with their codes
supported_languages = {
    "English": "en",
    "Bahasa Indonesia": "id",
    "Bahasa Malaysia": "ms",
    "Thai": "th",
    "Vietnamese": "vi",
    "Filipino": "tl",
    "Khmer": "km",
    "Burmese": "my",
    "Lao": "lo"
}

# Initialize NLTK resources
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text, language_code="en"):
    """
    Analyze sentiment of text using appropriate analyzer for the language.
    
    Args:
        text (str): Text to analyze
        language_code (str): Language code for the text (default: English)
        
    Returns:
        float: Sentiment score between -1 (negative) and 1 (positive)
    """
    if not text:
        return 0.0
    
    # Clean the text
    text = clean_text(text)
    
    # Use VADER for English
    if language_code == "en":
        scores = sia.polarity_scores(text)
        # Convert compound score to range -1 to 1
        return scores['compound']
        
    # For other languages, use a simplified approach
    # In a real implementation, language-specific models would be used
    else:
        # This is a simplified placeholder
        # A real implementation would use language-specific models
        scores = sia.polarity_scores(text)
        return scores['compound'] * 0.8  # Reduced confidence for non-English
        
def clean_text(text):
    """
    Clean text for sentiment analysis.
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
        
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove mentions and hashtags for cleaner analysis
    text = re.sub(r'@\w+', '', text)
    
    # Keep hashtags but remove the # symbol to count the word
    text = re.sub(r'#(\w+)', r'\1', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def categorize_sentiment(score):
    """
    Categorize sentiment score into positive, neutral, or negative.
    
    Args:
        score (float): Sentiment score between -1 and 1
        
    Returns:
        str: Sentiment category ('positive', 'neutral', or 'negative')
    """
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"
        
def get_sentiment_color(score):
    """
    Get color code for sentiment visualization.
    
    Args:
        score (float): Sentiment score between -1 and 1
        
    Returns:
        str: Hex color code
    """
    if score >= 0.05:
        # Positive - green gradient based on strength
        intensity = min(1.0, score * 2)
        return f"#{int(144 + 111 * intensity):02x}{int(238):02x}{int(144 + 111 * intensity):02x}"
    elif score <= -0.05:
        # Negative - red gradient based on strength
        intensity = min(1.0, abs(score) * 2)
        return f"#{int(255):02x}{int(128 - 128 * intensity):02x}{int(128 - 128 * intensity):02x}"
    else:
        # Neutral - yellow
        return "#FFC107"

def get_language_specific_sentiment_model(language_code):
    """
    Placeholder for getting language-specific sentiment models.
    In a real implementation, this would load appropriate models for each language.
    
    Args:
        language_code (str): Language code
        
    Returns:
        object: Sentiment model appropriate for the language
    """
    # This is a placeholder - in a real implementation, this would
    # return language-specific sentiment models
    return sia
