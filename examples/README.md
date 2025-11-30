# Examples

This directory contains example scripts demonstrating various features of the ADS Testbench Development Framework.

## Available Examples

### 1. basic_hfss_to_ads.py
Basic example showing how to extract S-parameters from HFSS and import to ADS.

**Usage:**
```bash
python basic_hfss_to_ads.py
```

**What it does:**
- Connects to HFSS project
- Extracts S-parameters
- Exports to Touchstone format
- Imports into ADS workspace

### 2. automated_workflow_example.py
Complete automated workflow using the HFSStoADSWorkflow class.

**Usage:**
```bash
python automated_workflow_example.py
```

**What it does:**
- Runs complete HFSS to ADS workflow
- Creates testbench automatically
- Runs verification

### 3. testbench_generation_example.py
Demonstrates automatic testbench generation for various simulation types.

**Usage:**
```bash
python testbench_generation_example.py
```

**What it does:**
- Generates S-parameter testbench
- Generates Harmonic Balance testbench
- Generates testbench from template

## Customizing Examples

All examples use placeholder paths. Update these variables before running:

```python
# Update these paths
hfss_project = "path/to/your/hfss_project.aedt"
ads_workspace = "path/to/your/ads_workspace"
```

## Creating Your Own Examples

1. Copy an existing example
2. Modify for your use case
3. Update paths and parameters
4. Test with your data

## Tips

- Start with `basic_hfss_to_ads.py` if you're new
- Use `automated_workflow_example.py` for production workflows
- Check logs in the `logs/` directory for debugging
- See `docs/workflow_examples.md` for more complex scenarios

## Need Help?

- Check documentation in `docs/`
- Review testbench templates in `testbenches/`
- Open an issue on GitHub
