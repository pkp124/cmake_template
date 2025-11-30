# API Reference

Complete API reference for the ADS Testbench Development Framework.

## PyAEDT Integration Module

### HFSSDataExtractor

Extract data from HFSS simulations.

#### Constructor

```python
HFSSDataExtractor(project_path: str, design_name: Optional[str] = None)
```

**Parameters:**
- `project_path`: Path to HFSS .aedt project file
- `design_name`: Name of design (uses active if None)

#### Methods

##### extract_s_parameters()

```python
extract_s_parameters(
    setup_name: Optional[str] = None,
    sweep_name: Optional[str] = None
) -> Dict[str, np.ndarray]
```

Extract S-parameter data.

**Returns:** Dictionary with frequency and S-parameter arrays

##### export_touchstone()

```python
export_touchstone(
    output_file: str,
    setup_name: Optional[str] = None,
    sweep_name: Optional[str] = None
) -> bool
```

Export S-parameters to Touchstone file.

**Returns:** True if successful

##### get_port_impedances()

```python
get_port_impedances() -> Dict[str, complex]
```

Get port impedances.

**Returns:** Dictionary of port names to impedances

##### close()

```python
close()
```

Close HFSS project and release resources.

---

### MaxwellDataExtractor

Extract data from Maxwell simulations.

#### Constructor

```python
MaxwellDataExtractor(project_path: str, design_name: Optional[str] = None)
```

#### Methods

##### extract_inductance_matrix()

```python
extract_inductance_matrix(setup_name: Optional[str] = None) -> np.ndarray
```

Extract inductance matrix.

**Returns:** Inductance matrix as numpy array

##### extract_resistance_matrix()

```python
extract_resistance_matrix(setup_name: Optional[str] = None) -> np.ndarray
```

Extract resistance matrix.

**Returns:** Resistance matrix as numpy array

---

### AEDTtoADSConverter

Convert AEDT data to ADS formats.

#### Constructor

```python
AEDTtoADSConverter(output_dir: Optional[str] = None)
```

#### Methods

##### convert_s_parameters()

```python
convert_s_parameters(
    s_param_dict: Dict[str, np.ndarray],
    output_file: str,
    format_type: str = "touchstone"
) -> bool
```

Convert S-parameters to specified format.

**Parameters:**
- `s_param_dict`: Dictionary with frequency and S-parameter data
- `output_file`: Output file path
- `format_type`: Format (touchstone, csv, matlab)

**Returns:** True if successful

---

## ADS Automation Module

### ADSController

Control ADS workspace and simulations.

#### Constructor

```python
ADSController(ads_install_path: Optional[str] = None)
```

#### Methods

##### open_workspace()

```python
open_workspace(workspace_path: str) -> bool
```

Open ADS workspace.

##### create_design()

```python
create_design(design_name: str, design_type: str = "schematic") -> bool
```

Create new design.

**Parameters:**
- `design_name`: Name for the design
- `design_type`: Type (schematic, layout, data_display)

##### run_simulation()

```python
run_simulation(
    simulation_name: str,
    parameters: Optional[Dict[str, Any]] = None
) -> bool
```

Run simulation.

---

### ADSDataImporter

Import data into ADS.

#### Constructor

```python
ADSDataImporter(workspace_path: str)
```

#### Methods

##### import_s_parameters()

```python
import_s_parameters(
    source_file: str,
    component_name: str,
    description: str = ""
) -> bool
```

Import S-parameters from Touchstone file.

##### import_csv_data()

```python
import_csv_data(
    csv_file: str,
    variable_name: str,
    column_mapping: Optional[Dict[str, str]] = None
) -> bool
```

Import data from CSV file.

##### import_pyaedt_data()

```python
import_pyaedt_data(
    data_dict: Dict[str, np.ndarray],
    dataset_name: str
) -> bool
```

Import data from PyAEDT results.

---

### TestbenchGenerator

Generate ADS testbenches.

#### Constructor

```python
TestbenchGenerator(
    workspace_path: str,
    template_dir: Optional[str] = None
)
```

#### Methods

##### generate_s_parameter_testbench()

```python
generate_s_parameter_testbench(
    component_file: str,
    testbench_name: str,
    freq_start: float,
    freq_stop: float,
    freq_points: int = 201
) -> bool
```

Generate S-parameter testbench.

##### generate_harmonic_balance_testbench()

```python
generate_harmonic_balance_testbench(
    circuit_file: str,
    testbench_name: str,
    fundamental_freq: float,
    harmonics: int = 7,
    power_sweep: Optional[List[float]] = None
) -> bool
```

Generate Harmonic Balance testbench.

##### generate_from_template()

```python
generate_from_template(
    template_name: str,
    testbench_name: str,
    parameters: Dict[str, Any]
) -> bool
```

Generate testbench from template.

---

## Workflow Module

### HFSStoADSWorkflow

Complete HFSS to ADS workflow automation.

#### Constructor

```python
HFSStoADSWorkflow(
    hfss_project: str,
    ads_workspace: str,
    output_dir: Optional[str] = None
)
```

#### Methods

##### run()

```python
run(
    component_name: str,
    create_testbench: bool = True,
    verify: bool = True
) -> bool
```

Run complete workflow.

---

### MaxwelltoADSWorkflow

Complete Maxwell to ADS workflow automation.

#### Constructor

```python
MaxwelltoADSWorkflow(
    maxwell_project: str,
    ads_workspace: str,
    output_dir: Optional[str] = None
)
```

#### Methods

##### run()

```python
run(
    component_name: str,
    extract_type: str = "all"
) -> bool
```

Run complete workflow.

**Parameters:**
- `component_name`: Name for component
- `extract_type`: Type of data (all, inductance, resistance)

---

## Utility Module

### Logger Configuration

#### setup_logger()

```python
setup_logger(
    log_file: str = "ads_testbench.log",
    level: str = "INFO",
    rotation: str = "10 MB",
    retention: int = 5
)
```

Set up logger with console and file output.

### File Utils

#### find_files()

```python
find_files(
    directory: str,
    pattern: str = "*",
    recursive: bool = True
) -> List[Path]
```

Find files matching pattern.

#### create_backup()

```python
create_backup(
    file_path: str,
    backup_dir: Optional[str] = None
) -> Optional[Path]
```

Create backup copy of file.

### Data Utils

#### load_config()

```python
load_config(config_file: str) -> Dict[str, Any]
```

Load configuration from YAML or JSON.

#### save_results()

```python
save_results(
    data: Dict[str, Any],
    output_file: str,
    format: str = "auto"
) -> bool
```

Save results to file.

#### validate_frequency_range()

```python
validate_frequency_range(
    freq_start: float,
    freq_stop: float,
    freq_points: int
) -> bool
```

Validate frequency range parameters.

---

## Type Definitions

Common types used throughout the API:

```python
# S-parameter data dictionary
SParamData = Dict[str, np.ndarray]  # Keys: 'frequency', 'S11_mag', 'S11_phase', etc.

# Configuration dictionary
Config = Dict[str, Any]

# Simulation parameters
SimParams = Dict[str, Union[float, int, str]]
```

## Constants

```python
# Default frequency units
FREQ_UNITS = ["Hz", "kHz", "MHz", "GHz"]

# Default formats
DATA_FORMATS = ["touchstone", "csv", "matlab", "json"]

# Design types
DESIGN_TYPES = ["schematic", "layout", "data_display"]
```
