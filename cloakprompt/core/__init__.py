"""
Core functionality for CloakPrompt.

This package contains the main redaction logic and configuration parsing.
"""

from .parser import ConfigParser
from .redactor import TextRedactor

__all__ = ["ConfigParser", "TextRedactor"]
