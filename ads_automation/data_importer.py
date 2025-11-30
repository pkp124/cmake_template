"""
ADS Data Importer Module

Handles importing data from various sources into ADS.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List, Union
from loguru import logger
import skrf as rf


class ADSDataImporter:
    """
    Imports data from external sources into ADS.
    
    Supports:
    - S-parameter files (Touchstone format)
    - CSV data files
    - PyAEDT exported data
    - Custom data formats
    """
    
    def __init__(self, workspace_path: str):
        """
        Initialize Data Importer.
        
        Args:
            workspace_path: Path to ADS workspace
        """
        self.workspace_path = Path(workspace_path)
        self.data_dir = self.workspace_path / "data"
        self.data_dir.mkdir(exist_ok=True)
        
    def import_s_parameters(self, source_file: str, 
                           component_name: str,
                           description: str = "") -> bool:
        """
        Import S-parameters from Touchstone file.
        
        Args:
            source_file: Path to .s*p file
            component_name: Name for the component in ADS
            description: Optional description
            
        Returns:
            True if successful, False otherwise
        """
        try:
            source_path = Path(source_file)
            if not source_path.exists():
                logger.error(f"S-parameter file not found: {source_file}")
                return False
                
            # Read S-parameter file using scikit-rf
            network = rf.Network(str(source_path))
            
            # Copy to workspace data directory
            dest_path = self.data_dir / source_path.name
            network.write_touchstone(str(dest_path))
            
            logger.info(f"Imported S-parameters: {component_name}")
            logger.debug(f"Frequency range: {network.f[0]/1e9:.2f} - {network.f[-1]/1e9:.2f} GHz")
            logger.debug(f"Number of ports: {network.nports}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to import S-parameters: {e}")
            return False
    
    def import_csv_data(self, csv_file: str, 
                       variable_name: str,
                       column_mapping: Optional[Dict[str, str]] = None) -> bool:
        """
        Import data from CSV file.
        
        Args:
            csv_file: Path to CSV file
            variable_name: Name for the data variable in ADS
            column_mapping: Mapping of CSV columns to ADS variables
            
        Returns:
            True if successful, False otherwise
        """
        try:
            csv_path = Path(csv_file)
            if not csv_path.exists():
                logger.error(f"CSV file not found: {csv_file}")
                return False
                
            # Read CSV data
            df = pd.read_csv(csv_path)
            
            # Copy to workspace data directory
            dest_path = self.data_dir / csv_path.name
            df.to_csv(dest_path, index=False)
            
            logger.info(f"Imported CSV data: {variable_name}")
            logger.debug(f"Columns: {list(df.columns)}")
            logger.debug(f"Rows: {len(df)}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to import CSV data: {e}")
            return False
    
    def import_pyaedt_data(self, data_dict: Dict[str, np.ndarray],
                          dataset_name: str) -> bool:
        """
        Import data from PyAEDT simulation results.
        
        Args:
            data_dict: Dictionary of numpy arrays from PyAEDT
            dataset_name: Name for the dataset in ADS
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert PyAEDT data to ADS-compatible format
            output_path = self.data_dir / f"{dataset_name}.csv"
            
            # Create DataFrame from dictionary
            df = pd.DataFrame(data_dict)
            df.to_csv(output_path, index=False)
            
            logger.info(f"Imported PyAEDT data: {dataset_name}")
            logger.debug(f"Variables: {list(data_dict.keys())}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to import PyAEDT data: {e}")
            return False
    
    def convert_touchstone_to_ads_component(self, 
                                           touchstone_file: str,
                                           component_name: str,
                                           library_name: str = "imported") -> bool:
        """
        Convert Touchstone file to ADS component.
        
        Args:
            touchstone_file: Path to Touchstone file
            component_name: Name for the component
            library_name: Library to store the component
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read and validate Touchstone file
            network = rf.Network(touchstone_file)
            
            # Create component definition
            # This would use ADS Python API to create actual component
            logger.info(f"Converting Touchstone to ADS component: {component_name}")
            logger.debug(f"Library: {library_name}")
            
            # Copy to workspace
            dest_path = self.data_dir / Path(touchstone_file).name
            network.write_touchstone(str(dest_path))
            
            return True
        except Exception as e:
            logger.error(f"Failed to convert Touchstone file: {e}")
            return False
