# PyAEDT Integration Guide

This guide explains how to use PyAEDT to extract data from Ansys AEDT tools and integrate with ADS workflows.

## Overview

PyAEDT is a Python library that provides a high-level interface to Ansys Electronics Desktop (AEDT). This framework uses PyAEDT to:

- Extract S-parameters from HFSS
- Extract inductance/resistance matrices from Maxwell
- Export field data
- Convert AEDT results to ADS-compatible formats

## HFSS Integration

### Basic S-Parameter Extraction

```python
from pyaedt_integration.hfss_extractor import HFSSDataExtractor

# Initialize extractor
extractor = HFSSDataExtractor("my_antenna.aedt", design_name="HFSSDesign1")

# Extract S-parameters
s_params = extractor.extract_s_parameters(
    setup_name="Setup1",
    sweep_name="Sweep1"
)

# Data format: dictionary with frequency and S-parameter arrays
print(f"Frequency range: {s_params['frequency'][0]} - {s_params['frequency'][-1]} Hz")
print(f"Available data: {list(s_params.keys())}")
```

### Export to Touchstone

```python
# Export S-parameters to Touchstone format
extractor.export_touchstone(
    output_file="antenna.s2p",
    setup_name="Setup1",
    sweep_name="Sweep1"
)
```

### Extract Port Impedances

```python
# Get port impedances
impedances = extractor.get_port_impedances()

for port, z in impedances.items():
    print(f"{port}: {z.real:.2f} + {z.imag:.2f}j Ω")
```

### Field Data Extraction

```python
# Extract electric field magnitude
field_data = extractor.extract_field_data(
    quantity="Mag_E",
    faces=["Radiation_Box"]
)
```

## Maxwell Integration

### Extract Inductance Matrix

```python
from pyaedt_integration.maxwell_extractor import MaxwellDataExtractor

# Initialize extractor
extractor = MaxwellDataExtractor("motor.aedt", design_name="Maxwell3DDesign1")

# Extract inductance matrix
L_matrix = extractor.extract_inductance_matrix(setup_name="Setup1")

print(f"Inductance matrix shape: {L_matrix.shape}")
print(f"Self inductance L11: {L_matrix[0,0]:.6e} H")
```

### Extract Resistance Matrix

```python
# Extract resistance matrix
R_matrix = extractor.extract_resistance_matrix(setup_name="Setup1")

print(f"Resistance matrix:\n{R_matrix}")
```

### Force and Torque Extraction

```python
# Extract force/torque data for specific objects
force_data = extractor.extract_force_torque(
    object_names=["Rotor", "Stator"],
    setup_name="Setup1"
)

for obj_name, data in force_data.items():
    print(f"{obj_name}:")
    print(f"  Force: {data['force']}")
    print(f"  Torque: {data['torque']}")
```

## Data Conversion

### Convert S-Parameters to ADS Format

```python
from pyaedt_integration.data_converter import AEDTtoADSConverter

# Initialize converter
converter = AEDTtoADSConverter(output_dir="converted_data")

# Convert to Touchstone (ADS compatible)
converter.convert_s_parameters(
    s_param_dict=s_params,
    output_file="component.s2p",
    format_type="touchstone"
)

# Or convert to CSV
converter.convert_s_parameters(
    s_param_dict=s_params,
    output_file="component_data.csv",
    format_type="csv"
)

# Or convert to MATLAB format
converter.convert_s_parameters(
    s_param_dict=s_params,
    output_file="component_data.mat",
    format_type="matlab"
)
```

### Convert Matrix Data

```python
# Convert inductance matrix to ADS format
converter.convert_matrix_data(
    matrix=L_matrix,
    output_file="inductance.txt",
    matrix_type="inductance"
)
```

### Unit Conversion

```python
# Convert frequency units
freq_ghz = converter.convert_frequency_units(
    freq_array=freq_hz,
    from_unit="Hz",
    to_unit="GHz"
)
```

## Advanced Usage

### Custom Solution Data Extraction

```python
# Access PyAEDT object directly for advanced operations
hfss = extractor.hfss

# Get all available results
results = hfss.post.available_report_quantities()
print(f"Available quantities: {results}")

# Create custom report
hfss.post.create_report(
    expressions=["S(1,1)", "S(2,1)"],
    setup_sweep_name="Setup1 : Sweep1",
    domain="Sweep"
)
```

### Batch Processing

```python
from pathlib import Path

# Process multiple HFSS projects
project_dir = Path("hfss_projects")

for project_file in project_dir.glob("*.aedt"):
    print(f"Processing: {project_file.name}")
    
    extractor = HFSSDataExtractor(str(project_file))
    
    # Extract and export
    output_file = f"output/{project_file.stem}.s2p"
    extractor.export_touchstone(output_file)
    
    extractor.close()
```

### Parametric Sweep Data

```python
# Extract data from parametric sweep
solutions = hfss.post.get_solution_data(
    expressions=["S(1,1)"],
    variations={"length": ["All"]},
    setup_sweep_name="Setup1 : Sweep1"
)

# Process parametric data
for variation in solutions.variations:
    print(f"Variation: {variation}")
```

## Integration with ADS Workflow

### Complete HFSS to ADS Pipeline

```python
from workflows.hfss_to_ads_workflow import HFSStoADSWorkflow

# Create automated workflow
workflow = HFSStoADSWorkflow(
    hfss_project="filter_design.aedt",
    ads_workspace="system_simulation",
    output_dir="workflow_data"
)

# Execute workflow
success = workflow.run(
    component_name="rf_filter",
    create_testbench=True,
    verify=True
)
```

## Best Practices

### 1. Resource Management

Always close extractors when done:

```python
try:
    extractor = HFSSDataExtractor("project.aedt")
    # ... operations ...
finally:
    extractor.close()
```

### 2. Error Handling

Check for valid data:

```python
s_params = extractor.extract_s_parameters()

if not s_params or 'frequency' not in s_params:
    print("Failed to extract S-parameters")
    return

if len(s_params['frequency']) == 0:
    print("No frequency data found")
    return
```

### 3. Non-Graphical Mode

For batch processing, use non-graphical mode (enabled by default):

```python
# Non-graphical mode is faster and doesn't require display
extractor = HFSSDataExtractor(
    "project.aedt",
    design_name="Design1"
)  # non_graphical=True by default
```

### 4. Logging

Enable detailed logging for debugging:

```python
from utils.logger_config import setup_logger

logger = setup_logger("hfss_extraction.log", level="DEBUG")
```

## Troubleshooting

### PyAEDT Version Compatibility

Ensure PyAEDT version matches your AEDT installation:

```bash
pip install pyaedt==0.7.0  # for AEDT 2023 R1
```

### AEDT License Issues

If you encounter license errors:
- Verify license server is accessible
- Check available licenses: `ansysli_util -status`
- Ensure AEDT is properly installed

### Data Extraction Errors

If extraction fails:
- Verify solution exists and is up to date
- Check setup and sweep names
- Ensure project has valid results

## Reference

- [PyAEDT Documentation](https://aedt.docs.pyansys.com/)
- [HFSS User Guide](https://www.ansys.com/products/electronics/ansys-hfss)
- [Maxwell User Guide](https://www.ansys.com/products/electronics/ansys-maxwell)
