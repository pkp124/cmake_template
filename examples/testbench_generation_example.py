"""
Testbench Generation Example

This example demonstrates how to generate various types of
ADS testbenches automatically.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ads_automation.testbench_generator import TestbenchGenerator
from utils.logger_config import setup_logger


def main():
    """Main example function."""
    # Setup logging
    logger = setup_logger("logs/testbench_generation.log")
    logger.info("Starting testbench generation example")
    
    # Configuration
    ads_workspace = "path/to/your/ads_workspace"
    
    try:
        # Create testbench generator
        generator = TestbenchGenerator(ads_workspace)
        
        # Example 1: S-parameter testbench
        logger.info("Generating S-parameter testbench...")
        generator.generate_s_parameter_testbench(
            component_file="data/filter.s2p",
            testbench_name="filter_sparam_tb",
            freq_start=0.0,
            freq_stop=10e9,
            freq_points=201
        )
        
        # Example 2: Harmonic Balance testbench
        logger.info("Generating Harmonic Balance testbench...")
        generator.generate_harmonic_balance_testbench(
            circuit_file="designs/amplifier.dsn",
            testbench_name="amplifier_hb_tb",
            fundamental_freq=2.4e9,
            harmonics=7,
            power_sweep=[-30, -20, -10, 0, 10]
        )
        
        # Example 3: Testbench from template
        logger.info("Generating testbench from template...")
        generator.generate_from_template(
            template_name="mixer_testbench",
            testbench_name="my_mixer_tb",
            parameters={
                "lo_freq": 1.8e9,
                "rf_freq": 2.4e9,
                "if_freq": 600e6
            }
        )
        
        logger.info("All testbenches generated successfully!")
        
    except Exception as e:
        logger.error(f"Example failed: {e}")
        raise


if __name__ == "__main__":
    main()
