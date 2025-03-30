# Southeast Asian countries with metadata

# Country names and their ISO codes
sea_countries = {
    "Singapore": "SG",
    "Malaysia": "MY",
    "Indonesia": "ID",
    "Thailand": "TH",
    "Vietnam": "VN",
    "Philippines": "PH",
    "Myanmar": "MM",
    "Cambodia": "KH",
    "Laos": "LA",
    "Brunei": "BN",
    "Timor-Leste": "TL"
}

# Country codes for easier lookup
country_codes = {v: k for k, v in sea_countries.items()}

# ISO codes to language mapping (primary languages)
country_languages = {
    "SG": ["en", "zh", "ms", "ta"],  # English, Chinese, Malay, Tamil
    "MY": ["ms", "en", "zh", "ta"],  # Malay, English, Chinese, Tamil
    "ID": ["id"],                    # Indonesian
    "TH": ["th"],                    # Thai
    "VN": ["vi"],                    # Vietnamese
    "PH": ["tl", "en"],              # Filipino (Tagalog), English
    "MM": ["my"],                    # Burmese
    "KH": ["km"],                    # Khmer
    "LA": ["lo"],                    # Lao
    "BN": ["ms"],                    # Malay
    "TL": ["pt", "tet"]              # Portuguese, Tetum
}

# Country flags (emoji codes)
country_flags = {
    "SG": "🇸🇬",
    "MY": "🇲🇾",
    "ID": "🇮🇩",
    "TH": "🇹🇭",
    "VN": "🇻🇳",
    "PH": "🇵🇭",
    "MM": "🇲🇲",
    "KH": "🇰🇭",
    "LA": "🇱🇦",
    "BN": "🇧🇳",
    "TL": "🇹🇱"
}

# Country regions (for filtering)
country_regions = {
    "Maritime Southeast Asia": ["SG", "MY", "ID", "PH", "BN", "TL"],
    "Mainland Southeast Asia": ["TH", "VN", "MM", "KH", "LA"],
    "ASEAN Members": ["SG", "MY", "ID", "TH", "VN", "PH", "MM", "KH", "LA", "BN"],
    "Mekong Region": ["TH", "VN", "MM", "KH", "LA"]
}

# Population data (millions, approximate 2023)
country_population = {
    "SG": 5.9,
    "MY": 33.2,
    "ID": 275.5,
    "TH": 70.1,
    "VN": 98.2,
    "PH": 113.9,
    "MM": 54.8,
    "KH": 16.7,
    "LA": 7.5,
    "BN": 0.4,
    "TL": 1.3
}

# GDP per capita (USD, approximate 2023)
country_gdp_per_capita = {
    "SG": 72794,
    "MY": 12422,
    "ID": 4225,
    "TH": 7233,
    "VN": 3756,
    "PH": 3462,
    "MM": 1140,
    "KH": 1655,
    "LA": 2614,
    "BN": 32344,
    "TL": 1796
}

# Internet penetration rate (%, approximate 2023)
country_internet_penetration = {
    "SG": 95.0,
    "MY": 89.6,
    "ID": 71.7,
    "TH": 77.8,
    "VN": 70.3,
    "PH": 67.0,
    "MM": 47.2,
    "KH": 52.6,
    "LA": 43.3,
    "BN": 95.0,
    "TL": 34.2
}

def get_country_data(country_code):
    """
    Get comprehensive data for a specific country.
    
    Args:
        country_code (str): ISO country code
        
    Returns:
        dict: Dictionary containing country data
    """
    if country_code not in country_codes:
        return None
        
    return {
        "name": country_codes[country_code],
        "code": country_code,
        "flag": country_flags.get(country_code, ""),
        "languages": country_languages.get(country_code, []),
        "population": country_population.get(country_code, 0),
        "gdp_per_capita": country_gdp_per_capita.get(country_code, 0),
        "internet_penetration": country_internet_penetration.get(country_code, 0),
        "regions": [region for region, countries in country_regions.items() if country_code in countries]
    }

def get_countries_by_region(region):
    """
    Get countries in a specific region.
    
    Args:
        region (str): Region name
        
    Returns:
        list: List of country codes in the region
    """
    return country_regions.get(region, [])
