# Python Version Compatibility Guide

## The Problem

There's a fundamental compatibility challenge when integrating PyAEDT with ADS:

### Version Requirements

| Tool | Python Version | Notes |
|------|---------------|-------|
| **PyAEDT** | 3.7+ (prefer 3.8+) | Modern Python required |
| **ADS 2020** | 3.6 or 2.7 | Older Python bundled |
| **ADS 2021** | 3.6 | Limited support |
| **ADS 2022** | 3.7 | Better compatibility |
| **ADS 2023+** | 3.8+ | Full compatibility ✓ |

### The Incompatibility

- **ADS Python API** is tied to the Python version bundled with ADS installation
- **PyAEDT** requires modern Python (3.7+, preferably 3.8+)
- **Older ADS versions** (pre-2022) use Python 3.6 or even 2.7
- **You cannot mix** different Python versions in the same environment

## Solutions

We provide **THREE approaches** depending on your ADS version:

---

## Solution 1: Decoupled Architecture (Recommended for ALL versions)

**Use separate Python environments** - PyAEDT and ADS run independently, communicate via files.

### Architecture

```
┌─────────────────────┐         ┌─────────────────────┐
│  PyAEDT Environment │         │   ADS Environment   │
│   (Python 3.8+)     │         │  (ADS bundled Py)   │
│                     │         │                     │
│  - Extract HFSS     │         │  - Import S2P       │
│  - Export .s2p      │────────▶│  - Run simulations  │
│  - Generate data    │  Files  │  - Create testbench │
└─────────────────────┘         └─────────────────────┘
```

### Setup

#### Environment 1: PyAEDT (Modern Python)

```bash
# Create PyAEDT environment
python3.9 -m venv venv_pyaedt
source venv_pyaedt/bin/activate
pip install -r requirements_pyaedt.txt
```

#### Environment 2: ADS (ADS Python)

```bash
# Use ADS bundled Python
/opt/keysight/ads2023/python/bin/python -m pip install -r requirements_ads.txt
```

### Workflow

```bash
# Step 1: Extract from HFSS (PyAEDT environment)
source venv_pyaedt/bin/activate
python scripts/extract_from_hfss.py --project antenna.aedt --output antenna.s2p

# Step 2: Import to ADS (ADS environment)
/opt/keysight/ads2023/python/bin/python scripts/import_to_ads.py --file antenna.s2p
```

### Advantages
✓ Works with **any ADS version**  
✓ No version conflicts  
✓ Easy to debug  
✓ Industry standard approach  

---

## Solution 2: ADS 2023+ with Compatible Python (Simplest)

**If you have ADS 2023 or later**, it includes Python 3.8+, which is compatible with PyAEDT.

### Verification

```bash
# Check ADS Python version
/opt/keysight/ads2023/python/bin/python --version
# Should show Python 3.8 or higher
```

### Setup

```bash
# Use ADS Python for everything
export ADS_PYTHON=/opt/keysight/ads2023/python/bin/python
$ADS_PYTHON -m pip install pyaedt numpy pandas scikit-rf
```

### Workflow

```python
# Single environment - both PyAEDT and ADS work!
from pyaedt import Hfss
from ads_automation import ADSController

# Extract from HFSS
hfss = Hfss("project.aedt")
hfss.export_touchstone("output.s2p")

# Import to ADS
ads = ADSController()
ads.import_s_parameters("output.s2p")
```

### Advantages
✓ Single environment  
✓ Simpler code  
✓ Direct integration  

### Requirements
⚠️ **Requires ADS 2023 or later**

---

## Solution 3: File-Based Integration (Universal)

**Use files as the integration point** - No direct API calls between tools.

### Architecture

```
HFSS/Maxwell  →  Export Files  →  ADS
    ↓                              ↓
  PyAEDT            .s2p          Manual/Script
 Scripting         .csv           Import
                   .mat
```

### PyAEDT Script (Any Python 3.8+)

```python
# extract_data.py
from pyaedt import Hfss

hfss = Hfss("project.aedt")
hfss.export_touchstone("output.s2p")
print("Exported to output.s2p")
```

### ADS Script (ADS Python or Manual)

```python
# import_data.py - Run with ADS Python
import os

# Use ADS API (if available) or manual import
ads_workspace = "/path/to/workspace"
os.system(f"cp output.s2p {ads_workspace}/data/")
print("Import to ADS workspace data folder")
```

### Or Manual
1. Run PyAEDT script to generate .s2p files
2. Manually import to ADS via GUI or copy to workspace

### Advantages
✓ Works with **any ADS version** (even 2020, 2019)  
✓ No Python version issues  
✓ Simple and reliable  
✓ Easy for team collaboration  

---

## Implementation in This Framework

This framework is designed to support **all three solutions**:

### 1. Separate Requirements Files

```bash
requirements_pyaedt.txt   # For PyAEDT environment (Python 3.8+)
requirements_ads.txt      # For ADS environment (ADS Python)
requirements.txt          # Full set (if compatible)
```

### 2. Modular Design

```
pyaedt_integration/    # Can run standalone
    ├── hfss_extractor.py
    └── data_converter.py

ads_automation/        # Can run standalone
    ├── data_importer.py
    └── testbench_generator.py
```

### 3. File-Based Workflows

Our workflows are designed to work via files:

```python
# Step 1: PyAEDT (Python 3.9)
from pyaedt_integration import HFSSDataExtractor
extractor = HFSSDataExtractor("project.aedt")
extractor.export_touchstone("component.s2p")

# Step 2: ADS (ADS Python - separate process/environment)
from ads_automation import ADSDataImporter
importer = ADSDataImporter("workspace")
importer.import_s_parameters("component.s2p")
```

---

## Recommended Setup by ADS Version

### ADS 2023 or Later ✓

```bash
# Use ADS Python (3.8+) for everything
pip install -r requirements.txt
# Single environment works!
```

### ADS 2022

```bash
# Check Python version first
/opt/keysight/ads2022/python/bin/python --version

# If 3.7+:
pip install -r requirements.txt

# If older:
# Use Solution 1 (Decoupled)
```

### ADS 2020-2021

```bash
# Use Solution 1 (Decoupled Architecture)
# Separate PyAEDT and ADS environments
```

### ADS 2019 or Older

```bash
# Use Solution 3 (File-Based)
# PyAEDT extracts data to files
# Manually import to ADS or use basic file copy
```

---

## Quick Compatibility Check

Run this script to check your environment:

```python
# check_compatibility.py
import sys
import subprocess

print("Python Version Check")
print("=" * 60)
print(f"Current Python: {sys.version}")
print(f"Version: {sys.version_info.major}.{sys.version_info.minor}")

# Check if PyAEDT compatible
pyaedt_ok = sys.version_info >= (3, 7)
print(f"PyAEDT Compatible: {'✓ Yes' if pyaedt_ok else '✗ No (need 3.7+)'}")

# Try to find ADS
ads_paths = [
    "/opt/keysight/ads2023/python/bin/python",
    "/opt/keysight/ads2022/python/bin/python",
    "C:\\Program Files\\Keysight\\ADS2023\\python\\python.exe"
]

print("\nADS Python Search:")
for path in ads_paths:
    try:
        result = subprocess.run([path, "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Found: {path}")
            print(f"  Version: {result.stdout.strip()}")
    except:
        pass

print("\nRecommendation:")
if sys.version_info >= (3, 8):
    print("✓ Your Python is compatible with both PyAEDT and ADS 2023+")
    print("  Use Solution 2 (Single Environment)")
elif sys.version_info >= (3, 7):
    print("⚠ Your Python works with PyAEDT but check ADS version")
    print("  Use Solution 1 or 2 depending on ADS Python")
else:
    print("✗ Your Python is too old for PyAEDT")
    print("  Use Solution 1 (Decoupled Architecture)")
```

---

## Summary

| Your ADS Version | Recommended Solution | Setup Complexity |
|-----------------|---------------------|------------------|
| ADS 2023+ | Solution 2 (Single Env) | ⭐ Easy |
| ADS 2022 | Solution 1 or 2 | ⭐⭐ Medium |
| ADS 2020-2021 | Solution 1 (Decoupled) | ⭐⭐⭐ Medium |
| ADS 2019 or older | Solution 3 (File-Based) | ⭐⭐ Easy |

## Need Help?

1. Check your ADS and Python versions
2. Run `check_compatibility.py`
3. Choose the appropriate solution
4. See `docs/getting_started.md` for detailed setup

The framework is designed to be **flexible** and work with your specific environment!
