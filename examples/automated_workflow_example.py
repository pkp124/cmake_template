"""
Automated Workflow Example

This example demonstrates using the complete automated workflow
for HFSS to ADS integration.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflows.hfss_to_ads_workflow import HFSStoADSWorkflow
from utils.logger_config import setup_logger


def main():
    """Main example function."""
    # Setup logging
    logger = setup_logger("logs/automated_workflow.log")
    logger.info("Starting automated workflow example")
    
    # Configuration
    hfss_project = "path/to/your/hfss_project.aedt"
    ads_workspace = "path/to/your/ads_workspace"
    component_name = "rf_filter"
    output_dir = "workflow_output"
    
    try:
        # Create workflow instance
        workflow = HFSStoADSWorkflow(
            hfss_project=hfss_project,
            ads_workspace=ads_workspace,
            output_dir=output_dir
        )
        
        # Run complete workflow
        # This will:
        # 1. Extract S-parameters from HFSS
        # 2. Convert to ADS format
        # 3. Import to ADS workspace
        # 4. Create testbench
        # 5. Run verification
        success = workflow.run(
            component_name=component_name,
            create_testbench=True,
            verify=True
        )
        
        if success:
            logger.info("Workflow completed successfully!")
        else:
            logger.error("Workflow failed!")
            
    except Exception as e:
        logger.error(f"Example failed: {e}")
        raise


if __name__ == "__main__":
    main()
