"""
YAML configuration parser for cloakprompt.

This module handles loading and merging regex rules from YAML configuration files.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ConfigParser:
    """Parser for YAML configuration files containing regex patterns."""
    
    def __init__(self, default_config_path: Optional[str] = None):
        """
        Initialize the config parser.
        
        Args:
            default_config_path: Path to default configuration file
        """
        if default_config_path is None:
            # Default to the config file in the package
            package_dir = Path(__file__).parent.parent
            default_config_path = package_dir / "config" / "regex_cleanup.yaml"
        
        self.default_config_path = Path(default_config_path)
        self.default_config = self._load_yaml(self.default_config_path)
    
    def _load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """
        Load and parse a YAML file.
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            Parsed YAML content as dictionary
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            yaml.YAMLError: If the file contains invalid YAML
        """
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = yaml.safe_load(file)
                
            if content is None:
                logger.warning(f"Configuration file {file_path} is empty or contains only comments")
                return {}
                
            return content
            
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML file {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load configuration file {file_path}: {e}")
            raise
    
    def _merge_configs(self, base_config: Dict[str, Any], 
                       override_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge override configuration into base configuration.
        
        Args:
            base_config: Base configuration dictionary
            override_config: Override configuration dictionary
            
        Returns:
            Merged configuration dictionary
        """
        merged = base_config.copy()
        
        for category, category_rules in override_config.items():
            if category not in merged:
                merged[category] = category_rules
            else:
                # Merge rules within the category
                if 'rules' in category_rules and 'rules' in merged[category]:
                    # Create a map of rule names for easy lookup
                    existing_rules = {rule.get('name', ''): rule 
                                    for rule in merged[category]['rules']}
                    
                    for new_rule in category_rules['rules']:
                        rule_name = new_rule.get('name', '')
                        if rule_name in existing_rules:
                            # Update existing rule
                            existing_rules[rule_name].update(new_rule)
                        else:
                            # Add new rule
                            merged[category]['rules'].append(new_rule)
                else:
                    # If no rules to merge, just override the entire category
                    merged[category] = category_rules
        
        return merged
    
    def get_config(self, custom_config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the final configuration after merging default and custom configs.
        
        Args:
            custom_config_path: Optional path to custom configuration file
            
        Returns:
            Merged configuration dictionary
        """
        if custom_config_path is None:
            return self.default_config
        
        custom_path = Path(custom_config_path)
        if not custom_path.exists():
            logger.warning(f"Custom configuration file not found: {custom_path}")
            return self.default_config
        
        try:
            custom_config = self._load_yaml(custom_path)
            merged_config = self._merge_configs(self.default_config, custom_config)
            logger.info(f"Successfully merged custom configuration from {custom_path}")
            return merged_config
        except Exception as e:
            logger.error(f"Failed to load custom configuration, using default: {e}")
            return self.default_config
    
    def get_regex_patterns(self, custom_config_path: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Extract all regex patterns from the configuration.
        
        Args:
            custom_config_path: Optional path to custom configuration file
            
        Returns:
            List of dictionaries containing regex patterns and placeholders
        """
        config = self.get_config(custom_config_path)
        patterns = []
        
        for category, category_data in config.get('patterns').items():
            if isinstance(category_data, dict) and 'rules' in category_data:
                for rule in category_data['rules']:
                    if 'regex' in rule and 'placeholder' in rule:
                        patterns.append({
                            'name': rule.get('name', 'unknown'),
                            'regex': rule['regex'],
                            'placeholder': rule['placeholder'],
                            'category': category
                        })
        
        logger.info(f"Loaded {len(patterns)} regex patterns from configuration")
        return patterns
