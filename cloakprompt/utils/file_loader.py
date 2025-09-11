"""
File and input loading utilities for cloakprompt.

This module handles loading text from various input sources including
inline text, files, and stdin.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Union
from rich.console import Console
from rich.panel import Panel

logger = logging.getLogger(__name__)
console = Console()


class InputLoader:
    """Handles loading input from various sources."""
    
    @staticmethod
    def load_text(text: str) -> str:
        """
        Load text from inline string input.
        
        Args:
            text: Input text string
            
        Returns:
            The input text
        """
        if not text or not text.strip():
            raise ValueError("Text input cannot be empty")
        
        logger.debug(f"Loaded {len(text)} characters from inline text input")
        return text.strip()
    
    @staticmethod
    def load_file(file_path: Union[str, Path]) -> str:
        """
        Load text from a file.
        
        Args:
            file_path: Path to the file to load
            
        Returns:
            File contents as string
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            PermissionError: If the file cannot be read
            UnicodeDecodeError: If the file contains invalid encoding
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        try:
            # Try to read as UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
        except UnicodeDecodeError:
            # Fall back to system default encoding
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                logger.warning(f"File {file_path} read with system encoding (not UTF-8)")
            except Exception as e:
                raise UnicodeDecodeError(f"Failed to read file {file_path} with any encoding: {e}")
        
        if not content.strip():
            logger.warning(f"File {file_path} is empty")
        
        logger.info(f"Loaded {len(content)} characters from file: {file_path}")
        return content
    
    @staticmethod
    def load_stdin() -> str:
        """
        Load text from stdin (piped input).
        
        Returns:
            Text from stdin
            
        Raises:
            ValueError: If no input is provided via stdin
        """
        # Check if stdin has data
        if sys.stdin.isatty():
            raise ValueError("No input provided via stdin. Use --text or --file instead.")
        
        try:
            content = sys.stdin.read()
            
            if not content or not content.strip():
                raise ValueError("Stdin input is empty")
            
            logger.info(f"Loaded {len(content)} characters from stdin")
            return content.strip()
            
        except Exception as e:
            logger.error(f"Failed to read from stdin: {e}")
            raise
    
    @staticmethod
    def load_input(text: Optional[str] = None, 
                   file_path: Optional[Union[str, Path]] = None,
                   use_stdin: bool = False) -> str:
        """
        Load input from the specified source.
        
        Args:
            text: Inline text input
            file_path: Path to file input
            use_stdin: Whether to read from stdin
            
        Returns:
            Loaded text content
            
        Raises:
            ValueError: If no input source is specified or if multiple sources are specified
        """
        input_sources = sum([bool(text), bool(file_path), use_stdin])
        
        if input_sources == 0:
            raise ValueError("No input source specified. Use --text, --file, or --stdin")
        
        if input_sources > 1:
            raise ValueError("Multiple input sources specified. Use only one of --text, --file, or --stdin")
        
        try:
            if text:
                return InputLoader.load_text(text)
            elif file_path:
                return InputLoader.load_file(file_path)
            elif use_stdin:
                return InputLoader.load_stdin()
            else:
                raise ValueError("No valid input source found")
                
        except Exception as e:
            logger.error(f"Failed to load input: {e}")
            raise
    
    @staticmethod
    def validate_file_path(file_path: Union[str, Path]) -> bool:
        """
        Validate that a file path exists and is readable.
        
        Args:
            file_path: Path to validate
            
        Returns:
            True if file is valid and readable
        """
        try:
            file_path = Path(file_path)
            return file_path.exists() and file_path.is_file() and file_path.stat().st_size > 0
        except Exception:
            return False
    
    @staticmethod
    def get_file_info(file_path: Union[str, Path]) -> dict:
        """
        Get information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing file information
        """
        file_path = Path(file_path)
        
        try:
            stat = file_path.stat()
            return {
                'path': str(file_path),
                'exists': file_path.exists(),
                'is_file': file_path.is_file(),
                'size_bytes': stat.st_size if file_path.exists() else 0,
                'size_mb': round(stat.st_size / (1024 * 1024), 2) if file_path.exists() else 0,
                'readable': file_path.is_file() and os.access(file_path, os.R_OK)
            }
        except Exception as e:
            return {
                'path': str(file_path),
                'exists': False,
                'is_file': False,
                'size_bytes': 0,
                'size_mb': 0,
                'readable': False,
                'error': str(e)
            }
