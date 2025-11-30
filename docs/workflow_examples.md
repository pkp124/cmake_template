# Workflow Examples

This document provides complete workflow examples for common design scenarios.

## Workflow 1: HFSS Antenna to ADS System Simulation

### Scenario
Design an antenna in HFSS and integrate it into a complete transceiver system simulation in ADS.

### Steps

#### 1. Extract Antenna S-Parameters from HFSS

```python
from pyaedt_integration.hfss_extractor import HFSSDataExtractor
from utils.logger_config import setup_logger

# Setup logging
logger = setup_logger("antenna_workflow.log")

# Extract from HFSS
extractor = HFSSDataExtractor("antenna_design.aedt", design_name="Patch_Antenna")

# Export S-parameters
extractor.export_touchstone("antenna.s1p")

# Get port impedance for reference
impedances = extractor.get_port_impedances()
logger.info(f"Antenna impedance: {impedances}")

extractor.close()
```

#### 2. Import to ADS and Create System

```python
from ads_automation import ADSDataImporter, ADSController

# Import antenna model
importer = ADSDataImporter("transceiver_system_wrk")
importer.import_s_parameters(
    source_file="antenna.s1p",
    component_name="patch_antenna",
    description="2.4 GHz patch antenna from HFSS"
)

# Create system-level schematic
controller = ADSController()
controller.open_workspace("transceiver_system_wrk")
controller.create_design("tx_chain", "schematic")

# Component would be available in ADS library
logger.info("Antenna imported and ready for system integration")
```

#### 3. Run System Simulation

```python
# Run harmonic balance for transmitter
controller.run_simulation("System_HB")

# Extract system-level results
results = controller.extract_results([
    "EIRP",
    "EVM",
    "Spectrum_Mask"
])

controller.close()
```

## Workflow 2: Maxwell Motor Model to ADS Power Electronics

### Scenario
Extract motor inductance model from Maxwell and use in ADS for power electronics simulation.

### Complete Workflow Script

```python
from workflows.maxwell_to_ads_workflow import MaxwelltoADSWorkflow
from utils.logger_config import setup_logger

# Setup
logger = setup_logger("motor_workflow.log")

# Create workflow
workflow = MaxwelltoADSWorkflow(
    maxwell_project="bldc_motor.aedt",
    ads_workspace="motor_drive_wrk",
    output_dir="motor_data"
)

# Run extraction and import
success = workflow.run(
    component_name="bldc_motor_model",
    extract_type="all"  # Extract L and R matrices
)

if success:
    logger.info("Motor model successfully imported to ADS")
else:
    logger.error("Workflow failed")
```

## Workflow 3: RF Frontend Design Flow

### Scenario
Complete RF frontend design: HFSS components → ADS integration → System simulation

### Step-by-Step Process

#### 1. Extract Multiple HFSS Components

```python
from pathlib import Path
from pyaedt_integration import HFSSDataExtractor
from pyaedt_integration import AEDTtoADSConverter

# Components to extract
components = {
    "lna_input_match.aedt": "lna_input",
    "bandpass_filter.aedt": "bp_filter",
    "coupler.aedt": "directional_coupler"
}

converter = AEDTtoADSConverter("rf_components")

for project_file, comp_name in components.items():
    print(f"Processing {comp_name}...")
    
    # Extract
    extractor = HFSSDataExtractor(project_file)
    touchstone = f"rf_components/{comp_name}.s2p"
    extractor.export_touchstone(touchstone)
    extractor.close()
```

#### 2. Import All Components to ADS

```python
from ads_automation import ADSDataImporter

importer = ADSDataImporter("rf_frontend_wrk")

for comp_name in components.values():
    touchstone = f"rf_components/{comp_name}.s2p"
    
    importer.import_s_parameters(
        source_file=touchstone,
        component_name=comp_name,
        description=f"EM component: {comp_name}"
    )
    
    print(f"Imported: {comp_name}")
```

#### 3. Create Testbenches for Each Component

```python
from ads_automation import TestbenchGenerator

generator = TestbenchGenerator("rf_frontend_wrk")

for comp_name in components.values():
    touchstone = f"rf_components/{comp_name}.s2p"
    
    # Create individual testbench
    generator.generate_s_parameter_testbench(
        component_file=touchstone,
        testbench_name=f"{comp_name}_tb",
        freq_start=2.0e9,
        freq_stop=2.5e9,
        freq_points=501
    )
    
    print(f"Created testbench: {comp_name}_tb")
```

#### 4. Run System-Level Analysis

```python
from ads_automation import ADSController

controller = ADSController()
controller.open_workspace("rf_frontend_wrk")

# Create system-level design
controller.create_design("rf_frontend_system", "schematic")

# Run cascade analysis
controller.run_simulation("Cascade Analysis")

# Extract system metrics
results = controller.extract_results([
    "System_Gain",
    "Noise_Figure",
    "IP3",
    "P1dB"
])

# Process results
print("System Performance:")
for metric, value in results.items():
    print(f"  {metric}: {value}")

controller.close()
```

## Workflow 4: Automated Batch Processing

### Scenario
Process multiple HFSS designs in batch mode and import to ADS

```python
from pathlib import Path
from workflows.hfss_to_ads_workflow import HFSStoADSWorkflow
import pandas as pd

# Configuration
hfss_project_dir = Path("hfss_designs")
ads_workspace = "component_library_wrk"
results_file = "batch_results.csv"

# Process all HFSS projects
results = []

for hfss_file in hfss_project_dir.glob("*.aedt"):
    print(f"\n{'='*60}")
    print(f"Processing: {hfss_file.name}")
    print(f"{'='*60}")
    
    component_name = hfss_file.stem
    
    # Create workflow
    workflow = HFSStoADSWorkflow(
        hfss_project=str(hfss_file),
        ads_workspace=ads_workspace,
        output_dir=f"batch_output/{component_name}"
    )
    
    # Run workflow
    success = workflow.run(
        component_name=component_name,
        create_testbench=True,
        verify=True
    )
    
    # Record result
    results.append({
        "component": component_name,
        "file": hfss_file.name,
        "success": success,
        "timestamp": pd.Timestamp.now()
    })

# Save results summary
df = pd.DataFrame(results)
df.to_csv(results_file, index=False)

print(f"\n{'='*60}")
print(f"Batch processing complete!")
print(f"Results saved to: {results_file}")
print(f"Success rate: {df['success'].sum()}/{len(df)}")
print(f"{'='*60}")
```

## Workflow 5: Parameterized Design Sweep

### Scenario
Sweep design parameters in HFSS and import all variations to ADS

```python
from pyaedt_integration import HFSSDataExtractor

# Connect to parametric HFSS design
extractor = HFSSDataExtractor("parametric_filter.aedt")

# Get parametric variations
hfss = extractor.hfss
variations = hfss.available_variations.nominal_w_values_dict

print(f"Available variations: {variations}")

# Extract each variation
for var_name, var_values in variations.items():
    for value in var_values:
        print(f"Processing {var_name} = {value}")
        
        # Set variation
        hfss[var_name] = value
        
        # Export with variation in name
        output_name = f"filter_{var_name}_{value}.s2p"
        extractor.export_touchstone(output_name)

extractor.close()
```

## Workflow 6: Verification and Comparison

### Scenario
Compare HFSS results with ADS simulation to verify import accuracy

```python
import numpy as np
import matplotlib.pyplot as plt
from pyaedt_integration import HFSSDataExtractor
from ads_automation import ADSController
import skrf as rf

# Extract from HFSS
hfss_extractor = HFSSDataExtractor("filter.aedt")
hfss_extractor.export_touchstone("filter_hfss.s2p")
hfss_extractor.close()

# Simulate in ADS
ads_controller = ADSController()
ads_controller.open_workspace("verification_wrk")
ads_controller.run_simulation("S-Parameter Simulation")
ads_results = ads_controller.extract_results(["S11", "S21"])
ads_controller.close()

# Load HFSS Touchstone
hfss_network = rf.Network("filter_hfss.s2p")

# Compare
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(hfss_network.f / 1e9, 20*np.log10(np.abs(hfss_network.s[:, 0, 0])), 
         label='HFSS', linewidth=2)
# Plot ADS results (would need to process ads_results)
plt.xlabel('Frequency (GHz)')
plt.ylabel('S11 (dB)')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(hfss_network.f / 1e9, 20*np.log10(np.abs(hfss_network.s[:, 1, 0])),
         label='HFSS', linewidth=2)
# Plot ADS results
plt.xlabel('Frequency (GHz)')
plt.ylabel('S21 (dB)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('verification_comparison.png', dpi=300)
print("Comparison plot saved: verification_comparison.png")
```

## Best Practices for Workflows

### 1. Always Use Version Control

```bash
git init
git add .
git commit -m "Initial workflow setup"
```

### 2. Document Your Workflows

Create a workflow README:

```markdown
# My RF Frontend Workflow

## Purpose
Import HFSS components and simulate RF frontend

## Steps
1. Run extract_components.py
2. Run import_to_ads.py
3. Run system_simulation.py

## Expected Output
- Component library in ADS
- System simulation results
```

### 3. Use Configuration Files

```yaml
# workflow_config.yaml
components:
  - name: lna
    hfss_file: lna.aedt
    freq_range: [2.0e9, 2.5e9]
  - name: mixer
    hfss_file: mixer.aedt
    freq_range: [1.5e9, 3.0e9]

ads_workspace: rf_system_wrk
output_dir: workflow_results
```

### 4. Implement Error Recovery

```python
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        workflow.run(component_name="my_component")
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt < max_retries - 1:
            time.sleep(10)  # Wait before retry
        else:
            raise
```

## Additional Resources

- Check `examples/` directory for more code examples
- Review `testbenches/` for template examples
- See individual module documentation in `docs/`
