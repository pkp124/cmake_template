# Standalone Scripts

These scripts can run independently in separate Python environments, making them ideal for **decoupled architecture** setups where PyAEDT and ADS use different Python versions.

## Scripts

### extract_from_hfss_standalone.py

Extracts S-parameters from HFSS using PyAEDT (Python 3.8+ environment).

**Usage:**
```bash
# Activate PyAEDT environment
source venv_pyaedt/bin/activate

# Run extraction
python scripts/extract_from_hfss_standalone.py \
    --project /path/to/antenna.aedt \
    --output antenna.s2p \
    --design "HFSSDesign1" \
    --log logs/hfss_extract.log
```

**Arguments:**
- `--project`: Path to HFSS .aedt project file (required)
- `--output`: Output Touchstone file path (required)
- `--design`: Design name (optional, uses active design)
- `--setup`: Setup name (optional, uses first setup)
- `--sweep`: Sweep name (optional, uses first sweep)
- `--log`: Log file path (default: hfss_extract.log)

### import_to_ads_standalone.py

Imports data to ADS workspace (runs with ADS Python).

**Usage:**
```bash
# Use ADS Python directly
/opt/keysight/ads2023/python/bin/python scripts/import_to_ads_standalone.py \
    --workspace /path/to/ads_workspace \
    --file antenna.s2p \
    --name patch_antenna \
    --description "2.4 GHz patch antenna" \
    --log logs/ads_import.log
```

**Arguments:**
- `--workspace`: Path to ADS workspace directory (required)
- `--file`: Path to data file (.s*p or .csv) (required)
- `--name`: Component name in ADS (required)
- `--description`: Component description (optional)
- `--log`: Log file path (default: ads_import.log)

## Typical Workflow

### For Users with Different Python Versions

If your ADS uses older Python (3.6 or 3.7) incompatible with PyAEDT:

#### Step 1: Extract from HFSS (PyAEDT environment)

```bash
# Create and activate PyAEDT environment (one-time setup)
python3.9 -m venv venv_pyaedt
source venv_pyaedt/bin/activate
pip install -r requirements_pyaedt.txt

# Extract data
python scripts/extract_from_hfss_standalone.py \
    --project designs/filter.aedt \
    --output output/filter.s2p
```

#### Step 2: Import to ADS (ADS Python)

```bash
# Use ADS Python
/opt/keysight/ads2022/python/bin/python scripts/import_to_ads_standalone.py \
    --workspace /path/to/ads_workspace \
    --file output/filter.s2p \
    --name bandpass_filter
```

### For Users with Compatible Python (ADS 2023+)

If your ADS has Python 3.8+, you can use the unified workflow scripts in `workflows/`:

```bash
# Single environment works!
python workflows/hfss_to_ads_workflow.py \
    designs/filter.aedt \
    /path/to/ads_workspace \
    bandpass_filter
```

## Batch Processing Example

Extract multiple HFSS designs:

```bash
#!/bin/bash
# batch_extract.sh

source venv_pyaedt/bin/activate

for project in designs/*.aedt; do
    name=$(basename "$project" .aedt)
    echo "Extracting $name..."
    
    python scripts/extract_from_hfss_standalone.py \
        --project "$project" \
        --output "output/${name}.s2p" \
        --log "logs/${name}_extract.log"
done

echo "Extraction complete! Files in output/"
```

Import to ADS:

```bash
#!/bin/bash
# batch_import.sh

ADS_PYTHON="/opt/keysight/ads2023/python/bin/python"
WORKSPACE="/path/to/ads_workspace"

for file in output/*.s2p; do
    name=$(basename "$file" .s2p)
    echo "Importing $name..."
    
    $ADS_PYTHON scripts/import_to_ads_standalone.py \
        --workspace "$WORKSPACE" \
        --file "$file" \
        --name "$name" \
        --log "logs/${name}_import.log"
done

echo "Import complete!"
```

## Integration with CI/CD

These standalone scripts are ideal for automated workflows:

```yaml
# .gitlab-ci.yml example
extract_hfss:
  stage: extract
  image: python:3.9
  script:
    - pip install -r requirements_pyaedt.txt
    - python scripts/extract_from_hfss_standalone.py 
        --project $CI_PROJECT_DIR/designs/antenna.aedt
        --output artifacts/antenna.s2p
  artifacts:
    paths:
      - artifacts/*.s2p

import_ads:
  stage: import
  dependencies:
    - extract_hfss
  script:
    - $ADS_PYTHON scripts/import_to_ads_standalone.py
        --workspace $ADS_WORKSPACE
        --file artifacts/antenna.s2p
        --name antenna_$CI_COMMIT_SHORT_SHA
```

## Troubleshooting

### PyAEDT Import Error

```
ImportError: No module named 'pyaedt'
```

**Solution:** Ensure you're using the PyAEDT environment:
```bash
source venv_pyaedt/bin/activate
which python  # Should show venv_pyaedt path
```

### ADS Python Not Found

```
bash: /opt/keysight/ads2023/python/bin/python: No such file or directory
```

**Solution:** Find your ADS Python installation:
```bash
# Linux
find /opt -name "python" -path "*/ads*/bin/*" 2>/dev/null

# Or run compatibility checker
python check_compatibility.py
```

### Permission Denied

```
Permission denied: '/path/to/ads_workspace/data'
```

**Solution:** Check workspace permissions:
```bash
chmod -R u+w /path/to/ads_workspace
```

## See Also

- [Python Compatibility Guide](../docs/python_compatibility.md)
- [Getting Started Guide](../docs/getting_started.md)
- [Workflow Examples](../docs/workflow_examples.md)
