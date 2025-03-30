import re
import string
from utils.sentiment_analyzer import supported_languages

def detect_language(text):
    """
    Simple language detection for Southeast Asian languages.
    This is a simplified placeholder - a real implementation would use 
    language detection libraries like langdetect or fastText.
    
    Args:
        text (str): Text to detect language
        
    Returns:
        str: Detected language code (e.g., 'en', 'id', 'th')
    """
    if not text:
        return "en"  # Default to English for empty text
        
    # Clean text
    text = text.lower()
    text = re.sub(r'[{}]'.format(string.punctuation), ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # This is a simplified approach using character ranges
    # A real implementation would use dedicated language detection libraries
    
    # Thai character range (approximate)
    thai_chars = re.findall(r'[\u0E00-\u0E7F]', text)
    if len(thai_chars) > len(text) * 0.3:
        return "th"
        
    # Vietnamese character range (approximate)
    vietnamese_chars = re.findall(r'[àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]', text)
    if len(vietnamese_chars) > len(text) * 0.2:
        return "vi"
        
    # Bahasa Indonesia/Malaysia keywords (simplified approach)
    id_ms_keywords = ['dan', 'atau', 'tidak', 'yang', 'di', 'ini', 'itu', 'dengan', 'untuk', 'pada']
    words = text.split()
    id_ms_count = sum(1 for word in words if word in id_ms_keywords)
    if id_ms_count > len(words) * 0.2:
        # This is highly simplified - a real implementation would differentiate between Indonesian and Malaysian
        return "id"  # Default to Indonesian
        
    # Filipino keywords (simplified approach)
    tl_keywords = ['ang', 'ng', 'sa', 'at', 'ay', 'mga', 'ko', 'mo', 'ka', 'niya']
    words = text.split()
    tl_count = sum(1 for word in words if word in tl_keywords)
    if tl_count > len(words) * 0.2:
        return "tl"
        
    # Default to English if no other language is detected
    return "en"

def get_supported_languages():
    """
    Get list of supported languages.
    
    Returns:
        dict: Dictionary of supported languages with their codes
    """
    return supported_languages

def is_language_supported(language_code):
    """
    Check if a language is supported.
    
    Args:
        language_code (str): Language code to check
        
    Returns:
        bool: True if language is supported, False otherwise
    """
    return language_code in supported_languages.values()

def get_language_name(language_code):
    """
    Get language name from code.
    
    Args:
        language_code (str): Language code
        
    Returns:
        str: Language name or None if not supported
    """
    for name, code in supported_languages.items():
        if code == language_code:
            return name
    return None
