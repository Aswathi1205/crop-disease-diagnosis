"""
Configuration Loader for Open/Closed Principle (OCP)

This module provides extensible configuration loading through abstract interfaces,
allowing new configuration sources without modifying existing code.
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path


class ConfigLoader(ABC):
    """Abstract base class for configuration loaders"""
    
    @abstractmethod
    def load(self, path: str) -> Dict[str, Any]:
        """
        Load configuration from source.
        
        Args:
            path: Path to configuration source
            
        Returns:
            Configuration dictionary
        """
        pass


class JsonConfigLoader(ConfigLoader):
    """Concrete implementation for loading JSON configuration files"""
    
    def load(self, path: str) -> Dict[str, Any]:
        """
        Load configuration from JSON file.
        
        Args:
            path: Path to JSON file
            
        Returns:
            Configuration dictionary
            
        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file is not valid JSON
        """
        config_path = Path(path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {str(e)}")
        except Exception as e:
            raise IOError(f"Failed to load configuration: {str(e)}")


# Future extensibility examples (not implemented):
# class YamlConfigLoader(ConfigLoader):
#     """Load configuration from YAML files"""
#     pass
#
# class EnvironmentConfigLoader(ConfigLoader):
#     """Load configuration from environment variables"""
#     pass
