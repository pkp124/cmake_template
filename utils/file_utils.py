"""
File Utility Functions
"""

import shutil
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from loguru import logger


def find_files(directory: str, 
               pattern: str = "*",
               recursive: bool = True) -> List[Path]:
    """
    Find files matching pattern in directory.
    
    Args:
        directory: Directory to search
        pattern: Glob pattern
        recursive: Whether to search recursively
        
    Returns:
        List of matching file paths
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        logger.warning(f"Directory not found: {directory}")
        return []
    
    if recursive:
        files = list(dir_path.rglob(pattern))
    else:
        files = list(dir_path.glob(pattern))
    
    logger.debug(f"Found {len(files)} files matching '{pattern}' in {directory}")
    return files


def create_backup(file_path: str, 
                 backup_dir: Optional[str] = None) -> Optional[Path]:
    """
    Create a backup copy of a file.
    
    Args:
        file_path: Path to file to backup
        backup_dir: Directory for backup (if None, uses same directory)
        
    Returns:
        Path to backup file or None if failed
    """
    try:
        source = Path(file_path)
        if not source.exists():
            logger.warning(f"File not found: {file_path}")
            return None
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{source.stem}_{timestamp}{source.suffix}"
        
        if backup_dir:
            backup_path = Path(backup_dir) / backup_name
            backup_path.parent.mkdir(exist_ok=True)
        else:
            backup_path = source.parent / backup_name
        
        # Copy file
        shutil.copy2(source, backup_path)
        logger.info(f"Backup created: {backup_path}")
        
        return backup_path
        
    except Exception as e:
        logger.error(f"Failed to create backup: {e}")
        return None


def ensure_directory(directory: str) -> Path:
    """
    Ensure directory exists, create if necessary.
    
    Args:
        directory: Path to directory
        
    Returns:
        Path object
    """
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_file_info(file_path: str) -> dict:
    """
    Get file information.
    
    Args:
        file_path: Path to file
        
    Returns:
        Dictionary with file information
    """
    path = Path(file_path)
    
    if not path.exists():
        return {}
    
    stat = path.stat()
    
    return {
        "name": path.name,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime),
        "created": datetime.fromtimestamp(stat.st_ctime),
        "extension": path.suffix,
        "is_file": path.is_file(),
        "is_dir": path.is_dir()
    }
