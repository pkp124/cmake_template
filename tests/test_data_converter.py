"""
Unit tests for AEDT to ADS data converter
"""

import pytest
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyaedt_integration.data_converter import AEDTtoADSConverter


class TestAEDTtoADSConverter:
    """Test cases for AEDTtoADSConverter class"""
    
    @pytest.fixture
    def converter(self, tmp_path):
        """Create converter with temporary output directory"""
        return AEDTtoADSConverter(str(tmp_path))
    
    @pytest.fixture
    def sample_s_params(self):
        """Create sample S-parameter data"""
        freq = np.linspace(0, 10e9, 201)
        s11_mag = 0.1 * np.ones(201)
        s11_phase = np.zeros(201)
        s21_mag = 0.9 * np.ones(201)
        s21_phase = -45 * np.ones(201)
        
        return {
            'frequency': freq,
            'S11_mag': s11_mag,
            'S11_phase': s11_phase,
            'S21_mag': s21_mag,
            'S21_phase': s21_phase,
            'S12_mag': s21_mag,
            'S12_phase': s21_phase,
            'S22_mag': s11_mag,
            'S22_phase': s11_phase
        }
    
    def test_converter_initialization(self, tmp_path):
        """Test converter initialization"""
        converter = AEDTtoADSConverter(str(tmp_path))
        assert converter.output_dir == tmp_path
        assert tmp_path.exists()
    
    def test_convert_s_parameters_csv(self, converter, sample_s_params, tmp_path):
        """Test CSV conversion"""
        output_file = "test_data.csv"
        success = converter.convert_s_parameters(
            sample_s_params,
            output_file,
            format_type="csv"
        )
        
        assert success
        assert (tmp_path / output_file).exists()
    
    def test_convert_matrix_data(self, converter, tmp_path):
        """Test matrix data conversion"""
        matrix = np.array([
            [1.0e-6, 5.0e-7],
            [5.0e-7, 1.0e-6]
        ])
        
        output_file = "inductance.txt"
        success = converter.convert_matrix_data(
            matrix,
            output_file,
            matrix_type="inductance"
        )
        
        assert success
        assert (tmp_path / output_file).exists()
    
    def test_frequency_unit_conversion(self, converter):
        """Test frequency unit conversion"""
        freq_hz = np.array([1e9, 2e9, 3e9])
        
        freq_ghz = converter.convert_frequency_units(freq_hz, "Hz", "GHz")
        
        np.testing.assert_array_almost_equal(freq_ghz, [1.0, 2.0, 3.0])
