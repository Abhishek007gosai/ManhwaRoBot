# Webs/utitls.py

"""
Utility functions and constants for Webs module.
"""

# Default message format (can be customized as needed)
DEFAULT_MSG_FORMAT = "{title} — {author} — {year}"

def format_message(title: str, author: str = "Unknown", year: str = "") -> str:
    """
    Format a message using the default format.
    
    Example:
        format_message("Naruto", "Masashi Kishimoto", "1999")
        -> "Naruto — Masashi Kishimoto — 1999"
    """
    return DEAULT_MSG_FORMAT.format(title=title, author=author, year=year)


def safe_get(dictionary: dict, key: str, default=None):
    """
    Safe dictionary getter to avoid KeyError.
    """
    return dictionary[key] if key in dictionary else default


def clean_text(text: str) -> str:
    """
    Basic text cleaner (remove extra spaces, newlines).
    """
  
  return " ".join(text.split())
