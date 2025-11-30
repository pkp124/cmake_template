# Getting Started Guide

This guide will help you set up and start using the ADS Testbench Development framework with PyAEDT integration.

## Prerequisites

### Software Requirements

1. **Keysight ADS** (2023 or later)
   - Installed and licensed
   - Python API enabled

2. **Ansys Electronics Desktop** (2023 R1 or later)
   - HFSS, Maxwell, or other AEDT tools
   - PyAEDT compatible version

3. **Python** (3.8 or higher)
   - Recommended: Python 3.9 or 3.10
   - Virtual environment support

### Hardware Requirements

- 16 GB RAM minimum (32 GB recommended)
- Multi-core processor (4+ cores recommended)
- Sufficient disk space for simulation results

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy template
cp config/env.template config/.env

# Edit configuration
nano config/.env  # or use your preferred editor
```

Update the following in `config/.env`:

```bash
# ADS Installation
ADS_INSTALL_PATH=/opt/keysight/ads2023
ADS_DEFAULT_WORKSPACE=/path/to/ads/workspace

# AEDT Installation
AEDT_INSTALL_PATH=/opt/ansys/AnsysEM/v231/Linux64
AEDT_DEFAULT_PROJECT_PATH=/path/to/aedt/projects

# License Servers
ADS_LICENSE_SERVER=your_server@port
AEDT_LICENSE_SERVER=your_server@port
```

## Quick Start

### Example 1: Extract S-parameters from HFSS

```python
from pyaedt_integration.hfss_extractor import HFSSDataExtractor

# Connect to HFSS project
extractor = HFSSDataExtractor("my_project.aedt")

# Extract S-parameters
s_params = extractor.extract_s_parameters()

# Export to Touchstone
extractor.export_touchstone("output.s2p")

extractor.close()
```

### Example 2: Import to ADS

```python
from ads_automation.data_importer import ADSDataImporter

# Create importer
importer = ADSDataImporter("path/to/ads/workspace")

# Import S-parameters
importer.import_s_parameters(
    source_file="output.s2p",
    component_name="my_component"
)
```

### Example 3: Complete Workflow

```python
from workflows.hfss_to_ads_workflow import HFSStoADSWorkflow

# Create workflow
workflow = HFSStoADSWorkflow(
    hfss_project="my_project.aedt",
    ads_workspace="path/to/ads/workspace"
)

# Run complete workflow
workflow.run(
    component_name="my_component",
    create_testbench=True,
    verify=True
)
```

## Project Structure

```
├── ads_automation/       # ADS automation modules
│   ├── ads_controller.py
│   ├── data_importer.py
│   └── testbench_generator.py
├── pyaedt_integration/   # PyAEDT integration modules
│   ├── hfss_extractor.py
│   ├── maxwell_extractor.py
│   └── data_converter.py
├── workflows/            # Complete workflow scripts
│   ├── hfss_to_ads_workflow.py
│   └── maxwell_to_ads_workflow.py
├── examples/            # Example scripts
├── testbenches/         # Testbench templates
├── utils/               # Utility modules
├── config/              # Configuration files
└── docs/                # Documentation
```

## Running Examples

### Run from Python

```python
python examples/basic_hfss_to_ads.py
```

### Run Workflow Script

```bash
python workflows/hfss_to_ads_workflow.py \
    path/to/hfss_project.aedt \
    path/to/ads_workspace \
    component_name
```

## Next Steps

- Read the [PyAEDT Integration Guide](pyaedt_integration.md)
- Review [ADS Automation Guide](ads_automation.md)
- Explore [Workflow Examples](workflow_examples.md)
- Check out the [API Reference](api_reference.md)

## Troubleshooting

### PyAEDT Import Errors

If you get import errors for PyAEDT:

```bash
pip install --upgrade pyaedt
```

### ADS Python Path Issues

Ensure ADS Python path is in your environment:

```bash
export PYTHONPATH=$PYTHONPATH:/opt/keysight/ads2023/python
```

### License Server Connection

Verify license server connectivity:

```bash
# For ADS
lmstat -a -c your_server@port

# For AEDT
ansysli_util -status
```

## Support

For issues and questions:
- Check the documentation in `docs/`
- Review examples in `examples/`
- Open an issue on GitHub
