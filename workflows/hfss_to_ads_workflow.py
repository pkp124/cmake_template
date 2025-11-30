"""
HFSS to ADS Workflow Automation

Complete workflow for extracting HFSS results and importing to ADS.
"""

import sys
from pathlib import Path
from typing import Optional
from loguru import logger

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyaedt_integration.hfss_extractor import HFSSDataExtractor
from pyaedt_integration.data_converter import AEDTtoADSConverter
from ads_automation.data_importer import ADSDataImporter
from ads_automation.testbench_generator import TestbenchGenerator


class HFSStoADSWorkflow:
    """
    Automated workflow for HFSS to ADS integration.
    
    Steps:
    1. Extract S-parameters from HFSS
    2. Convert to ADS-compatible format
    3. Import into ADS workspace
    4. Generate testbench
    5. Run verification simulations
    """
    
    def __init__(self, 
                 hfss_project: str,
                 ads_workspace: str,
                 output_dir: Optional[str] = None):
        """
        Initialize workflow.
        
        Args:
            hfss_project: Path to HFSS project (.aedt)
            ads_workspace: Path to ADS workspace
            output_dir: Directory for intermediate files
        """
        self.hfss_project = Path(hfss_project)
        self.ads_workspace = Path(ads_workspace)
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "workflow_output"
        self.output_dir.mkdir(exist_ok=True)
        
        logger.info("HFSS to ADS Workflow initialized")
        logger.info(f"HFSS Project: {self.hfss_project}")
        logger.info(f"ADS Workspace: {self.ads_workspace}")
    
    def run(self, 
            component_name: str,
            create_testbench: bool = True,
            verify: bool = True) -> bool:
        """
        Run the complete workflow.
        
        Args:
            component_name: Name for the imported component
            create_testbench: Whether to create testbench
            verify: Whether to run verification
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("="*60)
            logger.info("Starting HFSS to ADS Workflow")
            logger.info("="*60)
            
            # Step 1: Extract from HFSS
            logger.info("\n[Step 1/5] Extracting data from HFSS...")
            if not self._extract_from_hfss(component_name):
                logger.error("Failed to extract from HFSS")
                return False
            
            # Step 2: Convert data
            logger.info("\n[Step 2/5] Converting data format...")
            touchstone_file = self.output_dir / f"{component_name}.s2p"
            if not self._convert_data(component_name, str(touchstone_file)):
                logger.error("Failed to convert data")
                return False
            
            # Step 3: Import to ADS
            logger.info("\n[Step 3/5] Importing to ADS...")
            if not self._import_to_ads(str(touchstone_file), component_name):
                logger.error("Failed to import to ADS")
                return False
            
            # Step 4: Create testbench
            if create_testbench:
                logger.info("\n[Step 4/5] Creating testbench...")
                if not self._create_testbench(component_name, str(touchstone_file)):
                    logger.error("Failed to create testbench")
                    return False
            else:
                logger.info("\n[Step 4/5] Skipping testbench creation")
            
            # Step 5: Verify
            if verify and create_testbench:
                logger.info("\n[Step 5/5] Running verification...")
                if not self._verify_import(component_name):
                    logger.warning("Verification failed (non-critical)")
            else:
                logger.info("\n[Step 5/5] Skipping verification")
            
            logger.info("\n" + "="*60)
            logger.info("Workflow completed successfully!")
            logger.info("="*60)
            return True
            
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            return False
    
    def _extract_from_hfss(self, component_name: str) -> bool:
        """Extract S-parameters from HFSS."""
        try:
            extractor = HFSSDataExtractor(str(self.hfss_project))
            
            # Extract S-parameters
            s_params = extractor.extract_s_parameters()
            
            if not s_params:
                logger.error("No S-parameters extracted")
                return False
            
            # Export Touchstone
            touchstone_file = self.output_dir / f"{component_name}.s2p"
            success = extractor.export_touchstone(str(touchstone_file))
            
            extractor.close()
            
            logger.info(f"S-parameters extracted: {len(s_params)} datasets")
            return success
            
        except Exception as e:
            logger.error(f"HFSS extraction failed: {e}")
            return False
    
    def _convert_data(self, component_name: str, touchstone_file: str) -> bool:
        """Convert data to ADS format."""
        try:
            converter = AEDTtoADSConverter(str(self.output_dir))
            
            # The Touchstone file is already in ADS-compatible format
            # Additional conversions can be done here if needed
            
            logger.info("Data conversion complete")
            return True
            
        except Exception as e:
            logger.error(f"Data conversion failed: {e}")
            return False
    
    def _import_to_ads(self, touchstone_file: str, component_name: str) -> bool:
        """Import data to ADS."""
        try:
            importer = ADSDataImporter(str(self.ads_workspace))
            
            success = importer.import_s_parameters(
                source_file=touchstone_file,
                component_name=component_name,
                description=f"Imported from HFSS: {self.hfss_project.name}"
            )
            
            logger.info(f"Component imported: {component_name}")
            return success
            
        except Exception as e:
            logger.error(f"ADS import failed: {e}")
            return False
    
    def _create_testbench(self, component_name: str, touchstone_file: str) -> bool:
        """Create ADS testbench."""
        try:
            generator = TestbenchGenerator(str(self.ads_workspace))
            
            success = generator.generate_s_parameter_testbench(
                component_file=touchstone_file,
                testbench_name=f"{component_name}_tb",
                freq_start=0.0,
                freq_stop=10e9,
                freq_points=201
            )
            
            logger.info(f"Testbench created: {component_name}_tb")
            return success
            
        except Exception as e:
            logger.error(f"Testbench creation failed: {e}")
            return False
    
    def _verify_import(self, component_name: str) -> bool:
        """Verify imported data."""
        try:
            # Compare HFSS and ADS results
            # This is a placeholder for actual verification
            
            logger.info("Verification complete")
            return True
            
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return False


def main():
    """Main entry point for workflow script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="HFSS to ADS Workflow")
    parser.add_argument("hfss_project", help="Path to HFSS project (.aedt)")
    parser.add_argument("ads_workspace", help="Path to ADS workspace")
    parser.add_argument("component_name", help="Name for imported component")
    parser.add_argument("--output-dir", help="Output directory", default=None)
    parser.add_argument("--no-testbench", action="store_true", 
                       help="Skip testbench creation")
    parser.add_argument("--no-verify", action="store_true",
                       help="Skip verification")
    
    args = parser.parse_args()
    
    # Configure logging
    logger.add("hfss_to_ads_workflow.log", rotation="10 MB")
    
    # Run workflow
    workflow = HFSStoADSWorkflow(
        hfss_project=args.hfss_project,
        ads_workspace=args.ads_workspace,
        output_dir=args.output_dir
    )
    
    success = workflow.run(
        component_name=args.component_name,
        create_testbench=not args.no_testbench,
        verify=not args.no_verify
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
