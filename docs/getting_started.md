# Getting Started Guide

This guide will help you set up and start using the ADS Testbench Development framework with PyAEDT integration.

## Prerequisites

### ⚠️ CRITICAL: Python Version Compatibility

**Before you start, understand the Python version requirements:**

PyAEDT and ADS may require **different Python versions** depending on your ADS release:

| Your ADS Version | Python Requirement | Integration Method |
|-----------------|-------------------|-------------------|
| ADS 2023+ | Python 3.8+ bundled | ✓ Single environment |
| ADS 2022 | Python 3.7 bundled | ⚠️ May need separate envs |
| ADS 2020-2021 | Python 3.6 bundled | ⚠️ Separate environments |
| ADS 2019 or older | Python 2.7/3.6 | ✗ File-based only |

**Action Required:**
1. Run `python check_compatibility.py` to check your setup
2. Read [Python Compatibility Guide](python_compatibility.md)
3. Choose the appropriate installation method

### Software Requirements

1. **Keysight ADS**
   - **ADS 2023 or later** (Recommended - Python 3.8+ included)
   - **OR ADS 2020-2022** (Use decoupled architecture)
   - Installed and licensed
   - Python API enabled

2. **Ansys Electronics Desktop** (2023 R1 or later)
   - HFSS, Maxwell, or other AEDT tools
   - PyAEDT compatible version

3. **Python** 
   - **Python 3.8 or higher** for PyAEDT
   - May need separate environment for ADS (see compatibility guide)

### Hardware Requirements

- 16 GB RAM minimum (32 GB recommended)
- Multi-core processor (4+ cores recommended)
- Sufficient disk space for simulation results

## Installation

### Step 0: Check Compatibility (REQUIRED)

```bash
# Run compatibility checker
python check_compatibility.py
```

This will tell you which installation method to use.

---

### Method A: Single Environment (ADS 2023+ only)

Use this if you have ADS 2023 or later with Python 3.8+.

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Method B: Decoupled Architecture (ADS 2022 or earlier)

Use this if you have older ADS versions.

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

#### 2. Create PyAEDT Environment

```bash
# Create PyAEDT environment with Python 3.8+
python3.9 -m venv venv_pyaedt

# Activate
source venv_pyaedt/bin/activate  # Linux/Mac
# or
venv_pyaedt\Scripts\activate  # Windows

# Install PyAEDT requirements
pip install -r requirements_pyaedt.txt
```

#### 3. Install ADS Requirements

```bash
# Use ADS bundled Python
/opt/keysight/ads2022/python/bin/python -m pip install -r requirements_ads.txt

# Windows example:
# "C:\Program Files\Keysight\ADS2022\python\python.exe" -m pip install -r requirements_ads.txt
```

#### 4. Usage Pattern

```bash
# For PyAEDT operations (use PyAEDT environment)
source venv_pyaedt/bin/activate
python scripts/extract_from_hfss.py

# For ADS operations (use ADS Python)
/opt/keysight/ads2022/python/bin/python scripts/import_to_ads.py
```

---

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
