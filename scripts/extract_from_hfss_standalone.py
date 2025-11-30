#!/usr/bin/env python
"""
Standalone HFSS Data Extraction Script

This script can run in a PyAEDT-only environment (Python 3.8+)
without requiring ADS Python.

Usage:
    python extract_from_hfss_standalone.py --project antenna.aedt --output antenna.s2p
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyaedt_integration import HFSSDataExtractor
from utils.logger_config import setup_logger


def main():
    """Main extraction function."""
    parser = argparse.ArgumentParser(
        description="Extract S-parameters from HFSS project"
    )
    parser.add_argument(
        "--project",
        required=True,
        help="Path to HFSS .aedt project file"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output Touchstone file path"
    )
    parser.add_argument(
        "--design",
        default=None,
        help="Design name (uses active if not specified)"
    )
    parser.add_argument(
        "--setup",
        default=None,
        help="Setup name (uses first if not specified)"
    )
    parser.add_argument(
        "--sweep",
        default=None,
        help="Sweep name (uses first if not specified)"
    )
    parser.add_argument(
        "--log",
        default="hfss_extract.log",
        help="Log file path"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger(args.log)
    
    try:
        logger.info("="*60)
        logger.info("HFSS Data Extraction - Standalone Mode")
        logger.info("="*60)
        logger.info(f"Project: {args.project}")
        logger.info(f"Output: {args.output}")
        
        # Create extractor
        logger.info("Connecting to HFSS...")
        extractor = HFSSDataExtractor(args.project, design_name=args.design)
        
        # Export Touchstone
        logger.info("Exporting S-parameters...")
        success = extractor.export_touchstone(
            output_file=args.output,
            setup_name=args.setup,
            sweep_name=args.sweep
        )
        
        if success:
            logger.info(f"✓ Successfully exported to: {args.output}")
            logger.info("File ready for import to ADS")
        else:
            logger.error("✗ Export failed")
            return 1
        
        # Close
        extractor.close()
        
        logger.info("="*60)
        logger.info("Extraction Complete!")
        logger.info("="*60)
        logger.info("\nNext step:")
        logger.info(f"  Import {args.output} to ADS workspace")
        
        return 0
        
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
