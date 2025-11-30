"""
AEDT to ADS Data Converter Module

Converts data formats between AEDT and ADS.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Tuple
from loguru import logger
import skrf as rf


class AEDTtoADSConverter:
    """
    Converts data from AEDT format to ADS-compatible formats.
    
    Handles:
    - S-parameter format conversion
    - Matrix data conversion
    - Field data conversion
    - Unit conversions
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize converter.
        
        Args:
            output_dir: Directory for output files (if None, uses current directory)
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.output_dir.mkdir(exist_ok=True)
        
    def convert_s_parameters(self,
                           s_param_dict: Dict[str, np.ndarray],
                           output_file: str,
                           format_type: str = "touchstone") -> bool:
        """
        Convert S-parameter data to ADS format.
        
        Args:
            s_param_dict: Dictionary with frequency and S-parameter data
            output_file: Path to output file
            format_type: Output format (touchstone, csv, matlab)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Converting S-parameters to {format_type} format")
            
            if format_type == "touchstone":
                return self._write_touchstone(s_param_dict, output_file)
            elif format_type == "csv":
                return self._write_csv(s_param_dict, output_file)
            elif format_type == "matlab":
                return self._write_matlab(s_param_dict, output_file)
            else:
                logger.error(f"Unknown format: {format_type}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to convert S-parameters: {e}")
            return False
    
    def _write_touchstone(self, 
                         s_param_dict: Dict[str, np.ndarray],
                         output_file: str) -> bool:
        """Write S-parameters in Touchstone format."""
        try:
            freq = s_param_dict['frequency']
            
            # Determine number of ports
            s_params = [k for k in s_param_dict.keys() if k.startswith('S')]
            num_ports = int(np.sqrt(len(s_params) / 2))  # /2 for mag and phase
            
            # Create network using scikit-rf
            s_matrix = np.zeros((len(freq), num_ports, num_ports), dtype=complex)
            
            for i in range(num_ports):
                for j in range(num_ports):
                    mag_key = f"S{i+1}{j+1}_mag"
                    phase_key = f"S{i+1}{j+1}_phase"
                    
                    if mag_key in s_param_dict and phase_key in s_param_dict:
                        mag = s_param_dict[mag_key]
                        phase = s_param_dict[phase_key]
                        s_matrix[:, i, j] = mag * np.exp(1j * np.deg2rad(phase))
            
            # Create Network object
            network = rf.Network(frequency=rf.Frequency.from_f(freq, unit='Hz'),
                                s=s_matrix)
            
            # Write Touchstone file
            output_path = self.output_dir / output_file
            network.write_touchstone(str(output_path))
            
            logger.info(f"Touchstone file written: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write Touchstone file: {e}")
            return False
    
    def _write_csv(self,
                   data_dict: Dict[str, np.ndarray],
                   output_file: str) -> bool:
        """Write data in CSV format."""
        try:
            df = pd.DataFrame(data_dict)
            output_path = self.output_dir / output_file
            df.to_csv(output_path, index=False)
            
            logger.info(f"CSV file written: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write CSV file: {e}")
            return False
    
    def _write_matlab(self,
                     data_dict: Dict[str, np.ndarray],
                     output_file: str) -> bool:
        """Write data in MATLAB format."""
        try:
            from scipy.io import savemat
            
            output_path = self.output_dir / output_file
            savemat(str(output_path), data_dict)
            
            logger.info(f"MATLAB file written: {output_path}")
            return True
            
        except ImportError:
            logger.error("scipy not installed for MATLAB export")
            return False
        except Exception as e:
            logger.error(f"Failed to write MATLAB file: {e}")
            return False
    
    def convert_matrix_data(self,
                           matrix: np.ndarray,
                           output_file: str,
                           matrix_type: str = "inductance") -> bool:
        """
        Convert matrix data (L, R, C) to ADS format.
        
        Args:
            matrix: Numpy array containing matrix data
            output_file: Path to output file
            matrix_type: Type of matrix (inductance, resistance, capacitance)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Converting {matrix_type} matrix")
            
            # Write matrix in ADS-compatible format
            output_path = self.output_dir / output_file
            
            # Create header
            header = f"# {matrix_type.upper()} Matrix\n"
            header += f"# Size: {matrix.shape[0]}x{matrix.shape[1]}\n"
            
            # Write matrix
            with open(output_path, 'w') as f:
                f.write(header)
                np.savetxt(f, matrix, fmt='%.6e')
            
            logger.info(f"Matrix file written: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to convert matrix data: {e}")
            return False
    
    def convert_frequency_units(self,
                               freq_array: np.ndarray,
                               from_unit: str,
                               to_unit: str) -> np.ndarray:
        """
        Convert frequency units.
        
        Args:
            freq_array: Frequency array
            from_unit: Source unit (Hz, kHz, MHz, GHz)
            to_unit: Target unit (Hz, kHz, MHz, GHz)
            
        Returns:
            Converted frequency array
        """
        units = {
            'Hz': 1,
            'kHz': 1e3,
            'MHz': 1e6,
            'GHz': 1e9
        }
        
        if from_unit not in units or to_unit not in units:
            logger.error(f"Unknown units: {from_unit}, {to_unit}")
            return freq_array
        
        conversion_factor = units[from_unit] / units[to_unit]
        return freq_array * conversion_factor
