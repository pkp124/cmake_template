"""
Unit tests for utility functions
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.file_utils import find_files, ensure_directory, get_file_info
from utils.data_utils import validate_frequency_range, merge_configs


class TestFileUtils:
    """Test cases for file utilities"""
    
    def test_ensure_directory(self, tmp_path):
        """Test directory creation"""
        test_dir = tmp_path / "test" / "nested" / "dir"
        result = ensure_directory(str(test_dir))
        
        assert result.exists()
        assert result.is_dir()
    
    def test_find_files(self, tmp_path):
        """Test file finding"""
        # Create test files
        (tmp_path / "file1.txt").touch()
        (tmp_path / "file2.txt").touch()
        (tmp_path / "file3.csv").touch()
        
        # Find txt files
        txt_files = find_files(str(tmp_path), "*.txt", recursive=False)
        
        assert len(txt_files) == 2
    
    def test_get_file_info(self, tmp_path):
        """Test file info extraction"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        info = get_file_info(str(test_file))
        
        assert info["name"] == "test.txt"
        assert info["extension"] == ".txt"
        assert info["is_file"] == True


class TestDataUtils:
    """Test cases for data utilities"""
    
    def test_validate_frequency_range_valid(self):
        """Test valid frequency range"""
        assert validate_frequency_range(0.0, 10e9, 201) == True
    
    def test_validate_frequency_range_invalid_start(self):
        """Test invalid start frequency"""
        assert validate_frequency_range(-1.0, 10e9, 201) == False
    
    def test_validate_frequency_range_invalid_stop(self):
        """Test invalid stop frequency"""
        assert validate_frequency_range(10e9, 1e9, 201) == False
    
    def test_validate_frequency_range_invalid_points(self):
        """Test invalid number of points"""
        assert validate_frequency_range(0.0, 10e9, 1) == False
    
    def test_merge_configs(self):
        """Test configuration merging"""
        config1 = {"a": 1, "b": {"c": 2}}
        config2 = {"b": {"d": 3}, "e": 4}
        
        merged = merge_configs(config1, config2)
        
        assert merged["a"] == 1
        assert merged["b"]["c"] == 2
        assert merged["b"]["d"] == 3
        assert merged["e"] == 4
