"""
Text redactor for cloakprompt.

This module handles the actual redaction of sensitive information from text
using regex patterns loaded from configuration files.
"""

import re
import logging
from typing import List, Dict, Any, Tuple
from .parser import ConfigParser

logger = logging.getLogger(__name__)


class TextRedactor:
    """Redacts sensitive information from text using regex patterns."""
    
    def __init__(self, config_parser: ConfigParser):
        """
        Initialize the text redactor.
        
        Args:
            config_parser: Configuration parser instance
        """
        self.config_parser = config_parser
        self.compiled_patterns: List[Tuple[re.Pattern, str, str]] = []
        self._compile_patterns()
    
    def _compile_patterns(self, custom_config_path: str = None) -> None:
        """
        Compile regex patterns for efficient matching.
        
        Args:
            custom_config_path: Optional path to custom configuration file
        """
        patterns = self.config_parser.get_regex_patterns(custom_config_path)
        self.compiled_patterns.clear()
        
        for pattern_info in patterns:
            try:
                # Compile the regex pattern
                compiled_regex = re.compile(pattern_info['regex'], re.IGNORECASE | re.MULTILINE)
                placeholder = pattern_info['placeholder']
                name = pattern_info['name']
                
                self.compiled_patterns.append((compiled_regex, placeholder, name))
                logger.debug(f"Compiled pattern '{name}': {pattern_info['regex']}")
                
            except re.error as e:
                logger.warning(f"Invalid regex pattern '{pattern_info.get('name', 'unknown')}': {e}")
                continue
        
        logger.info(f"Successfully compiled {len(self.compiled_patterns)} regex patterns")
    
    def redact_text(self, text: str, custom_config_path: str = None) -> str:
        """
        Redact sensitive information from the given text.
        
        Args:
            text: Input text to redact
            custom_config_path: Optional path to custom configuration file
            
        Returns:
            Text with sensitive information redacted
        """
        if custom_config_path:
            # Recompile patterns if custom config is provided
            self._compile_patterns(custom_config_path)
        
        if not text:
            return text
        
        redacted_text = text
        redaction_count = 0
        
        for pattern, placeholder, name in self.compiled_patterns:
            try:
                # Find all matches and replace them
                matches = pattern.findall(redacted_text)
                if matches:
                    redacted_text = pattern.sub(placeholder, redacted_text)
                    redaction_count += len(matches)
                    logger.debug(f"Redacted {len(matches)} matches using pattern '{name}'")
                    
            except Exception as e:
                logger.warning(f"Error applying pattern '{name}': {e}")
                continue
        
        if redaction_count > 0:
            logger.info(f"Redacted {redaction_count} sensitive items from text")
        else:
            logger.debug("No sensitive information found in text")
        
        return redacted_text
    
    def redact_with_details(self, text: str, custom_config_path: str = None) -> Dict[str, Any]:
        """
        Redact text and return detailed information about what was redacted.
        
        Args:
            text: Input text to redact
            custom_config_path: Optional path to custom configuration file
            
        Returns:
            Dictionary containing redacted text and redaction details
        """
        if custom_config_path:
            self._compile_patterns(custom_config_path)
        
        if not text:
            return {
                'redacted_text': text,
                'redactions': [],
                'total_redactions': 0
            }
        
        redacted_text = text
        redactions = []
        total_redactions = 0
        
        for pattern, placeholder, name in self.compiled_patterns:
            try:
                # Find all matches
                matches = list(pattern.finditer(redacted_text))
                if matches:
                    # Replace matches in the text
                    redacted_text = pattern.sub(placeholder, redacted_text)
                    
                    # Record details about each match
                    for match in matches:
                        redactions.append({
                            'pattern_name': name,
                            'placeholder': placeholder,
                            'start_pos': match.start(),
                            'end_pos': match.end(),
                            'matched_text': match.group(),
                            'replacement': placeholder
                        })
                    
                    total_redactions += len(matches)
                    
            except Exception as e:
                logger.warning(f"Error applying pattern '{name}': {e}")
                continue
        
        return {
            'redacted_text': redacted_text,
            'redactions': redactions,
            'total_redactions': total_redactions
        }
    
    def get_pattern_summary(self, custom_config_path: str = None) -> Dict[str, Any]:
        """
        Get a summary of all available redaction patterns.
        
        Args:
            custom_config_path: Optional path to custom configuration file
            
        Returns:
            Dictionary containing pattern summary information
        """
        patterns = self.config_parser.get_regex_patterns(custom_config_path)
        
        summary = {
            'total_patterns': len(patterns),
            'categories': {},
            'pattern_details': []
        }
        
        for pattern in patterns:
            category = pattern.get('category', 'Unknown')
            if category not in summary['categories']:
                summary['categories'][category] = 0
            summary['categories'][category] += 1
            
            summary['pattern_details'].append({
                'name': pattern.get('name', 'unknown'),
                'category': category,
                'description': pattern.get('description', ''),
                'regex': pattern['regex'],
                'placeholder': pattern['placeholder']
            })
        
        return summary
