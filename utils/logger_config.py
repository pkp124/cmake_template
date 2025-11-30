"""
Logger Configuration Utilities
"""

import sys
from pathlib import Path
from loguru import logger


def setup_logger(log_file: str = "ads_testbench.log",
                level: str = "INFO",
                rotation: str = "10 MB",
                retention: int = 5):
    """
    Set up loguru logger with console and file output.
    
    Args:
        log_file: Path to log file
        level: Logging level
        rotation: Log rotation size
        retention: Number of rotated logs to keep
    """
    # Remove default handler
    logger.remove()
    
    # Add console handler with colors
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        colorize=True
    )
    
    # Add file handler
    log_path = Path(log_file)
    log_path.parent.mkdir(exist_ok=True)
    
    logger.add(
        log_file,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation=rotation,
        retention=retention,
        compression="zip"
    )
    
    logger.info(f"Logger initialized: {log_file}")
    return logger
