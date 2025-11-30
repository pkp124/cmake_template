# ADS Automation Guide

This guide explains how to use the ADS automation modules to control ADS simulations, import data, and generate testbenches.

## Overview

The ADS automation framework provides:
- **ADSController**: Control ADS workspace and simulations
- **ADSDataImporter**: Import data from external sources
- **TestbenchGenerator**: Generate testbenches automatically

## ADS Controller

### Opening a Workspace

```python
from ads_automation.ads_controller import ADSController

# Initialize controller
controller = ADSController(ads_install_path="/opt/keysight/ads2023")

# Open workspace
success = controller.open_workspace("/path/to/workspace")

if success:
    print("Workspace opened successfully")
```

### Creating Designs

```python
# Create schematic design
controller.create_design(
    design_name="amplifier",
    design_type="schematic"
)

# Create layout design
controller.create_design(
    design_name="filter_layout",
    design_type="layout"
)

# Create data display
controller.create_design(
    design_name="results_display",
    design_type="data_display"
)
```

### Running Simulations

```python
# Run simulation with default parameters
controller.run_simulation("S-Parameter Simulation")

# Run with custom parameters
parameters = {
    "FreqStart": 0.0,
    "FreqStop": 10e9,
    "NumPoints": 201
}

controller.run_simulation(
    simulation_name="Harmonic Balance",
    parameters=parameters
)
```

### Extracting Results

```python
# Extract specific results
results = controller.extract_results(
    result_names=["S11", "S21", "Gain"],
    output_format="csv"
)

# Process results
if results:
    for name, data in results.items():
        print(f"{name}: {data}")
```

## Data Importer

### Importing S-Parameters

```python
from ads_automation.data_importer import ADSDataImporter

# Create importer
importer = ADSDataImporter("/path/to/ads/workspace")

# Import Touchstone file
importer.import_s_parameters(
    source_file="component.s2p",
    component_name="rf_filter",
    description="Imported from HFSS simulation"
)
```

### Importing CSV Data

```python
# Import CSV data
column_mapping = {
    "Frequency": "freq",
    "S11_mag": "s11_magnitude",
    "S11_phase": "s11_phase"
}

importer.import_csv_data(
    csv_file="simulation_data.csv",
    variable_name="measured_data",
    column_mapping=column_mapping
)
```

### Importing PyAEDT Data

```python
import numpy as np

# PyAEDT extracted data
pyaedt_data = {
    "frequency": np.linspace(0, 10e9, 201),
    "S11_mag": np.random.random(201),
    "S11_phase": np.random.random(201) * 360
}

# Import to ADS
importer.import_pyaedt_data(
    data_dict=pyaedt_data,
    dataset_name="hfss_results"
)
```

### Converting to ADS Components

```python
# Convert Touchstone file to ADS component
importer.convert_touchstone_to_ads_component(
    touchstone_file="antenna.s2p",
    component_name="antenna_model",
    library_name="custom_components"
)
```

## Testbench Generator

### S-Parameter Testbench

```python
from ads_automation.testbench_generator import TestbenchGenerator

# Create generator
generator = TestbenchGenerator("/path/to/ads/workspace")

# Generate S-parameter testbench
generator.generate_s_parameter_testbench(
    component_file="data/filter.s2p",
    testbench_name="filter_sparam",
    freq_start=0.0,
    freq_stop=6e9,
    freq_points=301
)
```

### Harmonic Balance Testbench

```python
# Generate HB testbench for PA characterization
generator.generate_harmonic_balance_testbench(
    circuit_file="designs/power_amplifier.dsn",
    testbench_name="pa_characterization",
    fundamental_freq=2.4e9,
    harmonics=9,
    power_sweep=[-40, -30, -20, -10, 0, 10, 20]
)
```

### Template-Based Generation

```python
# Generate from template
mixer_parameters = {
    "lo_freq": 1.8e9,
    "rf_freq": 2.4e9,
    "if_freq": 600e6,
    "lo_power": 10.0,
    "harmonics": 9
}

generator.generate_from_template(
    template_name="mixer_testbench",
    testbench_name="downconverter_test",
    parameters=mixer_parameters
)
```

## Complete Workflow Examples

### Example 1: Import and Test Component

```python
from ads_automation import ADSController, ADSDataImporter, TestbenchGenerator

# Initialize modules
controller = ADSController()
importer = ADSDataImporter("/path/to/workspace")
generator = TestbenchGenerator("/path/to/workspace")

# Open workspace
controller.open_workspace("/path/to/workspace")

# Import component
importer.import_s_parameters(
    source_file="filter.s2p",
    component_name="bandpass_filter"
)

# Create testbench
generator.generate_s_parameter_testbench(
    component_file="filter.s2p",
    testbench_name="filter_test",
    freq_start=1e9,
    freq_stop=3e9,
    freq_points=201
)

# Run simulation
controller.run_simulation("S-Parameter Simulation")

# Extract results
results = controller.extract_results(
    result_names=["S11", "S21"],
    output_format="csv"
)

# Clean up
controller.close()
```

### Example 2: Batch Component Import

```python
from pathlib import Path

# Import multiple components
component_dir = Path("touchstone_files")
importer = ADSDataImporter("/path/to/workspace")

for s_file in component_dir.glob("*.s2p"):
    print(f"Importing: {s_file.name}")
    
    importer.import_s_parameters(
        source_file=str(s_file),
        component_name=s_file.stem,
        description=f"Imported from {s_file.name}"
    )
```

## Advanced Features

### Custom Testbench Templates

Create your own testbench templates in `testbenches/`:

```yaml
# my_custom_template.yaml
name: custom_testbench
type: harmonic_balance
description: My custom testbench

# Define parameters
fundamental_freq: 2.4e9
harmonics: 7

# Define measurements
measurements:
  - name: output_power
    type: power
  - name: efficiency
    type: pae
```

Use the template:

```python
generator.generate_from_template(
    template_name="my_custom_template",
    testbench_name="my_test",
    parameters={"fundamental_freq": 5.8e9}
)
```

### Simulation Automation

```python
# Automated simulation sweep
frequencies = [1e9, 2.4e9, 5.8e9]

for freq in frequencies:
    # Create testbench
    generator.generate_harmonic_balance_testbench(
        circuit_file="amplifier.dsn",
        testbench_name=f"amp_test_{freq/1e9:.1f}GHz",
        fundamental_freq=freq,
        harmonics=7
    )
    
    # Run simulation
    controller.run_simulation("Harmonic Balance")
    
    # Extract results
    results = controller.extract_results(["Pout", "Gain"])
    
    # Process results...
```

## Best Practices

### 1. Error Handling

Always check return values:

```python
success = controller.open_workspace(workspace_path)
if not success:
    print("Failed to open workspace")
    return

success = controller.run_simulation("sim_name")
if not success:
    print("Simulation failed")
    return
```

### 2. Resource Cleanup

Close controllers when done:

```python
try:
    controller = ADSController()
    # ... operations ...
finally:
    controller.close()
```

### 3. Workspace Organization

Organize your workspace:

```
ads_workspace/
├── designs/          # Design files
├── data/            # Data files (S2P, CSV)
├── testbenches/     # Testbench designs
└── results/         # Simulation results
```

### 4. Logging

Enable logging for debugging:

```python
from utils.logger_config import setup_logger

logger = setup_logger("ads_automation.log")
```

## Troubleshooting

### ADS Python API Not Found

Ensure ADS Python path is set:

```bash
export PYTHONPATH=$PYTHONPATH:/opt/keysight/ads2023/python
```

### Workspace Locked

If workspace is locked:
- Close ADS GUI
- Remove lock files in workspace directory
- Try again

### Simulation Failures

Check:
- Design has all required components
- Simulation parameters are valid
- Frequency ranges are reasonable
- Convergence settings are appropriate

## Reference

- [ADS Documentation](https://www.keysight.com/us/en/lib/resources/training-materials/pathwave-design-ads-training.html)
- [ADS Python API Guide](https://edadocs.software.keysight.com/kkbopen/ads-python-api-594193627.html)
- Testbench templates in `testbenches/`
