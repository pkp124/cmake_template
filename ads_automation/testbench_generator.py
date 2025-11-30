"""
ADS Testbench Generator Module

Generates ADS testbenches from templates and specifications.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from loguru import logger
import yaml


class TestbenchGenerator:
    """
    Generates ADS testbenches automatically.
    
    Supports:
    - S-parameter testbenches
    - Harmonic balance simulations
    - Transient simulations
    - Custom testbench templates
    """
    
    def __init__(self, workspace_path: str, template_dir: Optional[str] = None):
        """
        Initialize Testbench Generator.
        
        Args:
            workspace_path: Path to ADS workspace
            template_dir: Path to testbench templates (optional)
        """
        self.workspace_path = Path(workspace_path)
        self.template_dir = Path(template_dir) if template_dir else Path(__file__).parent.parent / "testbenches"
        
    def generate_s_parameter_testbench(self, 
                                       component_file: str,
                                       testbench_name: str,
                                       freq_start: float,
                                       freq_stop: float,
                                       freq_points: int = 201) -> bool:
        """
        Generate S-parameter testbench.
        
        Args:
            component_file: Path to component S-parameter file
            testbench_name: Name for the testbench
            freq_start: Start frequency (Hz)
            freq_stop: Stop frequency (Hz)
            freq_points: Number of frequency points
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Generating S-parameter testbench: {testbench_name}")
            
            config = {
                "type": "s_parameter",
                "component_file": component_file,
                "frequency": {
                    "start": freq_start,
                    "stop": freq_stop,
                    "points": freq_points
                },
                "measurements": [
                    "S11", "S12", "S21", "S22"
                ]
            }
            
            # Create testbench using ADS API
            # This is a placeholder for actual implementation
            testbench_path = self.workspace_path / f"{testbench_name}_dsn"
            testbench_path.mkdir(exist_ok=True)
            
            # Save configuration
            config_file = testbench_path / "config.yaml"
            with open(config_file, 'w') as f:
                yaml.dump(config, f)
            
            logger.info(f"Testbench created at: {testbench_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate S-parameter testbench: {e}")
            return False
    
    def generate_harmonic_balance_testbench(self,
                                           circuit_file: str,
                                           testbench_name: str,
                                           fundamental_freq: float,
                                           harmonics: int = 7,
                                           power_sweep: Optional[List[float]] = None) -> bool:
        """
        Generate Harmonic Balance testbench.
        
        Args:
            circuit_file: Path to circuit design
            testbench_name: Name for the testbench
            fundamental_freq: Fundamental frequency (Hz)
            harmonics: Number of harmonics to simulate
            power_sweep: List of input power levels (dBm)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Generating Harmonic Balance testbench: {testbench_name}")
            
            config = {
                "type": "harmonic_balance",
                "circuit_file": circuit_file,
                "fundamental_freq": fundamental_freq,
                "harmonics": harmonics,
                "power_sweep": power_sweep or [-20, -10, 0, 10]
            }
            
            testbench_path = self.workspace_path / f"{testbench_name}_dsn"
            testbench_path.mkdir(exist_ok=True)
            
            config_file = testbench_path / "config.yaml"
            with open(config_file, 'w') as f:
                yaml.dump(config, f)
            
            logger.info(f"Testbench created at: {testbench_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate Harmonic Balance testbench: {e}")
            return False
    
    def generate_from_template(self,
                              template_name: str,
                              testbench_name: str,
                              parameters: Dict[str, Any]) -> bool:
        """
        Generate testbench from template.
        
        Args:
            template_name: Name of the template
            testbench_name: Name for the testbench
            parameters: Dictionary of parameters to fill in template
            
        Returns:
            True if successful, False otherwise
        """
        try:
            template_file = self.template_dir / f"{template_name}.yaml"
            if not template_file.exists():
                logger.error(f"Template not found: {template_name}")
                return False
            
            # Load template
            with open(template_file, 'r') as f:
                template = yaml.safe_load(f)
            
            logger.info(f"Generating testbench from template: {template_name}")
            
            # Merge parameters with template
            testbench_config = {**template, **parameters}
            testbench_config["name"] = testbench_name
            
            # Create testbench
            testbench_path = self.workspace_path / f"{testbench_name}_dsn"
            testbench_path.mkdir(exist_ok=True)
            
            config_file = testbench_path / "config.yaml"
            with open(config_file, 'w') as f:
                yaml.dump(testbench_config, f)
            
            logger.info(f"Testbench created at: {testbench_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate testbench from template: {e}")
            return False
