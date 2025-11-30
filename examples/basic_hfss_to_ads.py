"""
Basic HFSS to ADS Example

This example demonstrates how to extract S-parameters from HFSS
and import them into ADS.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyaedt_integration.hfss_extractor import HFSSDataExtractor
from pyaedt_integration.data_converter import AEDTtoADSConverter
from ads_automation.data_importer import ADSDataImporter
from utils.logger_config import setup_logger


def main():
    """Main example function."""
    # Setup logging
    logger = setup_logger("logs/basic_hfss_to_ads.log")
    logger.info("Starting basic HFSS to ADS example")
    
    # Configuration
    hfss_project = "path/to/your/hfss_project.aedt"
    ads_workspace = "path/to/your/ads_workspace"
    component_name = "my_component"
    
    try:
        # Step 1: Extract S-parameters from HFSS
        logger.info("Extracting S-parameters from HFSS...")
        hfss_extractor = HFSSDataExtractor(hfss_project)
        
        # Get S-parameter data
        s_params = hfss_extractor.extract_s_parameters()
        logger.info(f"Extracted {len(s_params)} datasets")
        
        # Export to Touchstone
        touchstone_file = f"output/{component_name}.s2p"
        hfss_extractor.export_touchstone(touchstone_file)
        
        hfss_extractor.close()
        
        # Step 2: Convert to ADS format (optional additional processing)
        logger.info("Converting data format...")
        converter = AEDTtoADSConverter("output")
        
        # Convert if needed (Touchstone is already compatible)
        # converter.convert_s_parameters(s_params, f"{component_name}_converted.csv", "csv")
        
        # Step 3: Import to ADS
        logger.info("Importing to ADS...")
        ads_importer = ADSDataImporter(ads_workspace)
        
        ads_importer.import_s_parameters(
            source_file=touchstone_file,
            component_name=component_name,
            description="Imported from HFSS"
        )
        
        logger.info("Import complete!")
        
    except Exception as e:
        logger.error(f"Example failed: {e}")
        raise


if __name__ == "__main__":
    main()
