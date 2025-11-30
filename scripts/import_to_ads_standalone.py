#!/usr/bin/env python
"""
Standalone ADS Data Import Script

This script can run with ADS Python (any version that supports ADS API)
without requiring PyAEDT.

Usage:
    /path/to/ads/python/bin/python import_to_ads_standalone.py \
        --workspace /path/to/ads/workspace \
        --file component.s2p \
        --name my_component
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ads_automation import ADSDataImporter
from utils.logger_config import setup_logger


def main():
    """Main import function."""
    parser = argparse.ArgumentParser(
        description="Import data to ADS workspace"
    )
    parser.add_argument(
        "--workspace",
        required=True,
        help="Path to ADS workspace directory"
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to Touchstone (.s*p) or CSV file"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Component name in ADS"
    )
    parser.add_argument(
        "--description",
        default="",
        help="Component description"
    )
    parser.add_argument(
        "--log",
        default="ads_import.log",
        help="Log file path"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger(args.log)
    
    try:
        logger.info("="*60)
        logger.info("ADS Data Import - Standalone Mode")
        logger.info("="*60)
        logger.info(f"Workspace: {args.workspace}")
        logger.info(f"File: {args.file}")
        logger.info(f"Component: {args.name}")
        
        # Create importer
        logger.info("Initializing ADS importer...")
        importer = ADSDataImporter(args.workspace)
        
        # Determine file type and import
        file_path = Path(args.file)
        
        if file_path.suffix in ['.s1p', '.s2p', '.s3p', '.s4p']:
            logger.info("Importing S-parameter file...")
            success = importer.import_s_parameters(
                source_file=args.file,
                component_name=args.name,
                description=args.description or f"Imported from {file_path.name}"
            )
        elif file_path.suffix == '.csv':
            logger.info("Importing CSV file...")
            success = importer.import_csv_data(
                csv_file=args.file,
                variable_name=args.name
            )
        else:
            logger.error(f"Unsupported file type: {file_path.suffix}")
            logger.error("Supported types: .s1p, .s2p, .s3p, .s4p, .csv")
            return 1
        
        if success:
            logger.info(f"✓ Successfully imported: {args.name}")
            logger.info(f"Data location: {args.workspace}/data/")
        else:
            logger.error("✗ Import failed")
            return 1
        
        logger.info("="*60)
        logger.info("Import Complete!")
        logger.info("="*60)
        logger.info("\nNext step:")
        logger.info("  Open ADS and use the imported component in your design")
        
        return 0
        
    except Exception as e:
        logger.error(f"Import failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
