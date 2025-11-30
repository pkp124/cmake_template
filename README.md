# ADS Testbench Development with PyAEDT Integration

A comprehensive Python-based framework for Advanced Design System (ADS) testbench development with PyAEDT integration for system-level circuit design simulations.

## Overview

This project provides automation tools and workflows for:
- System-level simulations of circuit designs using ADS Python APIs
- Integration of PyAEDT (Ansys Electronics Desktop) results into ADS workflows
- Automated testbench generation and execution
- Data extraction, processing, and visualization
- Seamless workflow between Ansys AEDT and Keysight ADS

## Features

- **PyAEDT Integration**: Extract simulation results from HFSS, Maxwell, Q3D, and other AEDT tools
- **ADS Automation**: Python scripts for automated ADS design and simulation control
- **Data Pipeline**: Automated data conversion between AEDT and ADS formats
- **Testbench Templates**: Ready-to-use testbench templates for common RF/microwave designs
- **Result Analysis**: Comprehensive data analysis and visualization tools
- **Workflow Orchestration**: End-to-end automation scripts for complete design flows

## Project Structure

```
├── ads_automation/          # ADS automation scripts and utilities
├── pyaedt_integration/      # PyAEDT integration modules
├── workflows/               # Complete workflow automation scripts
├── testbenches/            # ADS testbench templates
├── examples/               # Example projects and tutorials
├── utils/                  # Common utilities and helpers
├── config/                 # Configuration files
├── docs/                   # Documentation
└── tests/                  # Unit tests
```

## Quick Start

### ⚠️ Important: Python Version Compatibility

**PyAEDT and ADS have different Python requirements!**

- **PyAEDT**: Requires Python 3.7+ (preferably 3.8+)
- **ADS 2023+**: Includes Python 3.8+ ✓ Compatible
- **ADS 2020-2022**: May use Python 3.6 or 3.7 ⚠️ Limited compatibility
- **ADS 2019 or older**: Uses Python 2.7 or 3.6 ✗ Not compatible

**Before installing, run the compatibility checker:**
```bash
python check_compatibility.py
```

See **[Python Compatibility Guide](docs/python_compatibility.md)** for detailed solutions.

### Prerequisites

- **Python 3.8 or higher** (for PyAEDT)
- **Keysight ADS** (2023+ recommended, or use decoupled architecture)
- **Ansys Electronics Desktop 2023 R1 or later** (for PyAEDT)
- Required Python packages (see appropriate requirements file)

### Installation

**IMPORTANT: Choose the right installation method for your ADS version!**

#### Option 1: ADS 2023+ (Single Environment - Recommended)

If you have ADS 2023 or later with Python 3.8+:

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Check compatibility first
python check_compatibility.py

# Install all dependencies (if compatible)
pip install -r requirements.txt

# Set up environment variables
cp config/env.template config/.env
# Edit config/.env with your ADS and AEDT installation paths
```

#### Option 2: Older ADS Versions (Decoupled Architecture)

If you have ADS 2022 or earlier:

```bash
# Create separate PyAEDT environment
python3.9 -m venv venv_pyaedt
source venv_pyaedt/bin/activate
pip install -r requirements_pyaedt.txt

# Install ADS requirements in ADS Python
/path/to/ads/python/bin/python -m pip install -r requirements_ads.txt
```

**See [Python Compatibility Guide](docs/python_compatibility.md) for detailed instructions.**

### Basic Usage

```python
# Example: Extract S-parameters from HFSS and import to ADS
from pyaedt_integration.hfss_extractor import HFSSDataExtractor
from ads_automation.data_importer import ADSDataImporter

# Extract data from HFSS
hfss_extractor = HFSSDataExtractor("path/to/hfss_project.aedt")
s_params = hfss_extractor.extract_s_parameters()

# Import to ADS
ads_importer = ADSDataImporter("path/to/ads_workspace")
ads_importer.import_s_parameters(s_params, "component_name")
```

## Workflows

### 1. HFSS to ADS Workflow
Extract EM simulation results from HFSS and integrate into ADS for system-level analysis.

### 2. Maxwell to ADS Workflow
Import motor/inductor models from Maxwell into ADS for power electronics simulations.

### 3. Automated Testbench Generation
Generate ADS testbenches automatically from design specifications.

## Documentation

- [Getting Started Guide](docs/getting_started.md)
- [PyAEDT Integration Guide](docs/pyaedt_integration.md)
- [ADS Automation Guide](docs/ads_automation.md)
- [Workflow Examples](docs/workflow_examples.md)
- [API Reference](docs/api_reference.md)

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Consult the documentation in the `docs/` folder
- Check the examples in the `examples/` folder
