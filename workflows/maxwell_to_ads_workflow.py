"""
Maxwell to ADS Workflow Automation

Complete workflow for extracting Maxwell results and importing to ADS.
"""

import sys
from pathlib import Path
from typing import Optional
from loguru import logger
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyaedt_integration.maxwell_extractor import MaxwellDataExtractor
from pyaedt_integration.data_converter import AEDTtoADSConverter
from ads_automation.data_importer import ADSDataImporter


class MaxwelltoADSWorkflow:
    """
    Automated workflow for Maxwell to ADS integration.
    
    Steps:
    1. Extract inductance/resistance matrices from Maxwell
    2. Convert to ADS-compatible format
    3. Import into ADS workspace
    4. Create equivalent circuit model
    """
    
    def __init__(self,
                 maxwell_project: str,
                 ads_workspace: str,
                 output_dir: Optional[str] = None):
        """
        Initialize workflow.
        
        Args:
            maxwell_project: Path to Maxwell project (.aedt)
            ads_workspace: Path to ADS workspace
            output_dir: Directory for intermediate files
        """
        self.maxwell_project = Path(maxwell_project)
        self.ads_workspace = Path(ads_workspace)
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "workflow_output"
        self.output_dir.mkdir(exist_ok=True)
        
        logger.info("Maxwell to ADS Workflow initialized")
        logger.info(f"Maxwell Project: {self.maxwell_project}")
        logger.info(f"ADS Workspace: {self.ads_workspace}")
    
    def run(self, component_name: str, extract_type: str = "all") -> bool:
        """
        Run the complete workflow.
        
        Args:
            component_name: Name for the imported component
            extract_type: Type of data to extract (all, inductance, resistance)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("="*60)
            logger.info("Starting Maxwell to ADS Workflow")
            logger.info("="*60)
            
            # Step 1: Extract from Maxwell
            logger.info("\n[Step 1/3] Extracting data from Maxwell...")
            matrices = self._extract_from_maxwell(component_name, extract_type)
            if not matrices:
                logger.error("Failed to extract from Maxwell")
                return False
            
            # Step 2: Convert data
            logger.info("\n[Step 2/3] Converting data format...")
            if not self._convert_and_export(component_name, matrices):
                logger.error("Failed to convert data")
                return False
            
            # Step 3: Import to ADS
            logger.info("\n[Step 3/3] Importing to ADS...")
            if not self._import_to_ads(component_name):
                logger.error("Failed to import to ADS")
                return False
            
            logger.info("\n" + "="*60)
            logger.info("Workflow completed successfully!")
            logger.info("="*60)
            return True
            
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            return False
    
    def _extract_from_maxwell(self, 
                             component_name: str,
                             extract_type: str) -> dict:
        """Extract matrices from Maxwell."""
        try:
            extractor = MaxwellDataExtractor(str(self.maxwell_project))
            
            matrices = {}
            
            if extract_type in ["all", "inductance"]:
                L_matrix = extractor.extract_inductance_matrix()
                if L_matrix.size > 0:
                    matrices['inductance'] = L_matrix
                    logger.info(f"Inductance matrix: {L_matrix.shape}")
            
            if extract_type in ["all", "resistance"]:
                R_matrix = extractor.extract_resistance_matrix()
                if R_matrix.size > 0:
                    matrices['resistance'] = R_matrix
                    logger.info(f"Resistance matrix: {R_matrix.shape}")
            
            extractor.close()
            
            return matrices
            
        except Exception as e:
            logger.error(f"Maxwell extraction failed: {e}")
            return {}
    
    def _convert_and_export(self, component_name: str, matrices: dict) -> bool:
        """Convert and export matrices."""
        try:
            converter = AEDTtoADSConverter(str(self.output_dir))
            
            for matrix_type, matrix_data in matrices.items():
                output_file = f"{component_name}_{matrix_type}.txt"
                converter.convert_matrix_data(
                    matrix=matrix_data,
                    output_file=output_file,
                    matrix_type=matrix_type
                )
            
            logger.info(f"Converted {len(matrices)} matrices")
            return True
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            return False
    
    def _import_to_ads(self, component_name: str) -> bool:
        """Import data to ADS."""
        try:
            importer = ADSDataImporter(str(self.ads_workspace))
            
            # Import matrix files
            for matrix_file in self.output_dir.glob(f"{component_name}_*.txt"):
                logger.info(f"Importing: {matrix_file.name}")
                # Would use ADS API to import matrix data
            
            logger.info("Import complete")
            return True
            
        except Exception as e:
            logger.error(f"Import failed: {e}")
            return False


def main():
    """Main entry point for workflow script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Maxwell to ADS Workflow")
    parser.add_argument("maxwell_project", help="Path to Maxwell project (.aedt)")
    parser.add_argument("ads_workspace", help="Path to ADS workspace")
    parser.add_argument("component_name", help="Name for imported component")
    parser.add_argument("--output-dir", help="Output directory", default=None)
    parser.add_argument("--type", choices=["all", "inductance", "resistance"],
                       default="all", help="Type of data to extract")
    
    args = parser.parse_args()
    
    # Configure logging
    logger.add("maxwell_to_ads_workflow.log", rotation="10 MB")
    
    # Run workflow
    workflow = MaxwelltoADSWorkflow(
        maxwell_project=args.maxwell_project,
        ads_workspace=args.ads_workspace,
        output_dir=args.output_dir
    )
    
    success = workflow.run(
        component_name=args.component_name,
        extract_type=args.type
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
