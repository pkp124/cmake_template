"""
Data Utility Functions
"""

import json
import yaml
import pickle
from pathlib import Path
from typing import Any, Dict, Optional
from loguru import logger


def load_config(config_file: str) -> Dict[str, Any]:
    """
    Load configuration from YAML or JSON file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        config_path = Path(config_file)
        
        if not config_path.exists():
            logger.error(f"Config file not found: {config_file}")
            return {}
        
        with open(config_path, 'r') as f:
            if config_path.suffix in ['.yaml', '.yml']:
                config = yaml.safe_load(f)
            elif config_path.suffix == '.json':
                config = json.load(f)
            else:
                logger.error(f"Unsupported config format: {config_path.suffix}")
                return {}
        
        logger.info(f"Configuration loaded: {config_file}")
        return config
        
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return {}


def save_results(data: Dict[str, Any],
                output_file: str,
                format: str = "auto") -> bool:
    """
    Save results to file.
    
    Args:
        data: Data dictionary to save
        output_file: Path to output file
        format: Output format (auto, json, yaml, pickle)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Auto-detect format from extension
        if format == "auto":
            if output_path.suffix == '.json':
                format = 'json'
            elif output_path.suffix in ['.yaml', '.yml']:
                format = 'yaml'
            elif output_path.suffix in ['.pkl', '.pickle']:
                format = 'pickle'
            else:
                format = 'json'  # default
        
        # Save file
        with open(output_path, 'w' if format != 'pickle' else 'wb') as f:
            if format == 'json':
                json.dump(data, f, indent=2, default=str)
            elif format == 'yaml':
                yaml.dump(data, f, default_flow_style=False)
            elif format == 'pickle':
                pickle.dump(data, f)
        
        logger.info(f"Results saved: {output_file} ({format})")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save results: {e}")
        return False


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple configuration dictionaries.
    Later configs override earlier ones.
    
    Args:
        *configs: Configuration dictionaries to merge
        
    Returns:
        Merged configuration
    """
    merged = {}
    
    for config in configs:
        merged = _deep_merge(merged, config)
    
    return merged


def _deep_merge(dict1: dict, dict2: dict) -> dict:
    """Deep merge two dictionaries."""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def validate_frequency_range(freq_start: float,
                            freq_stop: float,
                            freq_points: int) -> bool:
    """
    Validate frequency range parameters.
    
    Args:
        freq_start: Start frequency
        freq_stop: Stop frequency
        freq_points: Number of points
        
    Returns:
        True if valid, False otherwise
    """
    if freq_start < 0:
        logger.error("Start frequency must be non-negative")
        return False
    
    if freq_stop <= freq_start:
        logger.error("Stop frequency must be greater than start frequency")
        return False
    
    if freq_points < 2:
        logger.error("Number of frequency points must be at least 2")
        return False
    
    return True
