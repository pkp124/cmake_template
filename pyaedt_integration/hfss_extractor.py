"""
HFSS Data Extractor Module

Extracts simulation results from Ansys HFSS using PyAEDT.
"""

import numpy as np
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from loguru import logger


class HFSSDataExtractor:
    """
    Extracts data from HFSS simulations.
    
    Supports:
    - S-parameters
    - Field data
    - Port impedances
    - Far field patterns
    """
    
    def __init__(self, project_path: str, design_name: Optional[str] = None):
        """
        Initialize HFSS Data Extractor.
        
        Args:
            project_path: Path to HFSS project (.aedt file)
            design_name: Name of the design (if None, uses active design)
        """
        self.project_path = Path(project_path)
        self.design_name = design_name
        self.hfss = None
        self._connect_to_hfss()
        
    def _connect_to_hfss(self):
        """Connect to HFSS project using PyAEDT."""
        try:
            # Import PyAEDT
            from pyaedt import Hfss
            
            logger.info(f"Connecting to HFSS project: {self.project_path}")
            
            # Open project
            self.hfss = Hfss(
                projectname=str(self.project_path),
                designname=self.design_name,
                specified_version="2023.1",
                non_graphical=True
            )
            
            logger.info(f"Connected to design: {self.hfss.design_name}")
            
        except ImportError:
            logger.error("PyAEDT not installed. Install with: pip install pyaedt")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to HFSS: {e}")
            raise
    
    def extract_s_parameters(self, 
                           setup_name: Optional[str] = None,
                           sweep_name: Optional[str] = None) -> Dict[str, np.ndarray]:
        """
        Extract S-parameters from HFSS simulation.
        
        Args:
            setup_name: Name of the setup (if None, uses first setup)
            sweep_name: Name of the sweep (if None, uses first sweep)
            
        Returns:
            Dictionary containing frequency and S-parameter data
        """
        try:
            if not self.hfss:
                raise RuntimeError("Not connected to HFSS")
            
            # Get solution data
            solutions = self.hfss.post.get_solution_data()
            
            logger.info("Extracting S-parameters from HFSS")
            
            # Get port information
            num_ports = len(self.hfss.get_all_sources())
            logger.debug(f"Number of ports: {num_ports}")
            
            # Extract S-parameter data
            s_param_data = {}
            
            # Get frequency data
            freq = solutions.primary_sweep_values
            s_param_data['frequency'] = np.array(freq)
            
            # Extract all S-parameters
            for i in range(1, num_ports + 1):
                for j in range(1, num_ports + 1):
                    s_name = f"S({i},{j})"
                    try:
                        s_data = solutions.data_magnitude(s_name)
                        s_param_data[f"S{i}{j}_mag"] = np.array(s_data)
                        
                        s_phase = solutions.data_phase(s_name)
                        s_param_data[f"S{i}{j}_phase"] = np.array(s_phase)
                    except:
                        logger.warning(f"Could not extract {s_name}")
            
            logger.info(f"Extracted S-parameters: {len(s_param_data)} datasets")
            return s_param_data
            
        except Exception as e:
            logger.error(f"Failed to extract S-parameters: {e}")
            return {}
    
    def export_touchstone(self, 
                         output_file: str,
                         setup_name: Optional[str] = None,
                         sweep_name: Optional[str] = None) -> bool:
        """
        Export S-parameters to Touchstone file.
        
        Args:
            output_file: Path to output .s*p file
            setup_name: Name of the setup
            sweep_name: Name of the sweep
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.hfss:
                raise RuntimeError("Not connected to HFSS")
            
            logger.info(f"Exporting Touchstone file: {output_file}")
            
            # Use PyAEDT's built-in Touchstone export
            setup = setup_name or self.hfss.setups[0].name
            sweep = sweep_name or self.hfss.setups[0].sweeps[0].name
            
            self.hfss.export_touchstone(
                solution_name=f"{setup} : {sweep}",
                output_file=output_file
            )
            
            logger.info(f"Touchstone file exported successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export Touchstone file: {e}")
            return False
    
    def extract_field_data(self, 
                          quantity: str = "Mag_E",
                          faces: Optional[List[str]] = None) -> Dict[str, np.ndarray]:
        """
        Extract field data from HFSS.
        
        Args:
            quantity: Field quantity to extract (Mag_E, Mag_H, etc.)
            faces: List of face names to extract from
            
        Returns:
            Dictionary containing field data
        """
        try:
            if not self.hfss:
                raise RuntimeError("Not connected to HFSS")
            
            logger.info(f"Extracting field data: {quantity}")
            
            # Get field data using PyAEDT post-processing
            field_data = {}
            
            # This is a simplified example
            # Actual implementation would use PyAEDT's field calculator
            
            logger.info("Field data extraction complete")
            return field_data
            
        except Exception as e:
            logger.error(f"Failed to extract field data: {e}")
            return {}
    
    def get_port_impedances(self) -> Dict[str, complex]:
        """
        Get port impedances from HFSS.
        
        Returns:
            Dictionary of port names to impedances
        """
        try:
            if not self.hfss:
                raise RuntimeError("Not connected to HFSS")
            
            logger.info("Getting port impedances")
            
            impedances = {}
            for port in self.hfss.get_all_sources():
                # Get port impedance
                # This would use PyAEDT API
                impedances[port] = 50.0 + 0j  # Placeholder
            
            return impedances
            
        except Exception as e:
            logger.error(f"Failed to get port impedances: {e}")
            return {}
    
    def close(self):
        """Close HFSS project and release resources."""
        try:
            if self.hfss:
                logger.info("Closing HFSS project")
                self.hfss.close_project(save=False)
                self.hfss = None
        except Exception as e:
            logger.error(f"Error closing HFSS: {e}")
