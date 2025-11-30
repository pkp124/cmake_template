#!/usr/bin/env python
"""
Python and ADS Compatibility Checker

Checks Python version compatibility for PyAEDT and ADS integration.
"""

import sys
import subprocess
import platform
from pathlib import Path


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_python_version():
    """Check current Python version."""
    print_header("Current Python Environment")
    
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    
    major, minor = sys.version_info.major, sys.version_info.minor
    version_str = f"{major}.{minor}"
    
    print(f"\nVersion: Python {version_str}")
    
    # Check PyAEDT compatibility
    pyaedt_compatible = (major, minor) >= (3, 7)
    pyaedt_recommended = (major, minor) >= (3, 8)
    
    if pyaedt_recommended:
        print("✓ PyAEDT: Fully compatible (Python 3.8+)")
    elif pyaedt_compatible:
        print("⚠ PyAEDT: Compatible but 3.8+ recommended")
    else:
        print("✗ PyAEDT: NOT compatible (requires Python 3.7+)")
    
    return pyaedt_compatible


def find_ads_python():
    """Try to find ADS Python installations."""
    print_header("ADS Python Search")
    
    # Common ADS installation paths
    if platform.system() == "Windows":
        base_paths = [
            Path("C:/Program Files/Keysight"),
            Path("C:/ADS"),
        ]
        python_exe = "python/python.exe"
    else:  # Linux/Unix
        base_paths = [
            Path("/opt/keysight"),
            Path("/usr/local/keysight"),
            Path.home() / "ADS",
        ]
        python_exe = "python/bin/python"
    
    ads_versions = ["ADS2024", "ADS2023", "ADS2022", "ADS2021", "ADS2020"]
    
    found_installations = []
    
    for base in base_paths:
        if not base.exists():
            continue
            
        for version in ads_versions:
            ads_path = base / version.lower()
            python_path = ads_path / python_exe
            
            if python_path.exists():
                try:
                    # Get Python version
                    result = subprocess.run(
                        [str(python_path), "--version"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if result.returncode == 0:
                        py_version = result.stdout.strip() or result.stderr.strip()
                        found_installations.append({
                            'version': version,
                            'path': str(python_path),
                            'python_version': py_version
                        })
                        print(f"✓ Found {version}:")
                        print(f"  Path: {python_path}")
                        print(f"  {py_version}")
                except Exception as e:
                    print(f"⚠ Found {version} but couldn't check version: {e}")
    
    if not found_installations:
        print("✗ No ADS Python installations found")
        print("\nPlease specify your ADS installation path manually:")
        print("  Linux: /opt/keysight/ads2023/python/bin/python")
        print("  Windows: C:\\Program Files\\Keysight\\ADS2023\\python\\python.exe")
    
    return found_installations


def check_pyaedt_installation():
    """Check if PyAEDT is installed."""
    print_header("PyAEDT Installation Check")
    
    try:
        import pyaedt
        print(f"✓ PyAEDT is installed")
        print(f"  Version: {pyaedt.__version__}")
        return True
    except ImportError:
        print("✗ PyAEDT is NOT installed")
        print("\nTo install PyAEDT:")
        print("  pip install pyaedt")
        return False


def check_dependencies():
    """Check required dependencies."""
    print_header("Required Dependencies Check")
    
    dependencies = {
        'numpy': 'Data processing',
        'pandas': 'Data handling',
        'matplotlib': 'Visualization',
        'scipy': 'Scientific computing',
        'skrf': 'RF network analysis (scikit-rf)',
        'yaml': 'Configuration (PyYAML)',
        'loguru': 'Logging'
    }
    
    installed = []
    missing = []
    
    for package, description in dependencies.items():
        try:
            if package == 'skrf':
                import skrf
                version = skrf.__version__
            elif package == 'yaml':
                import yaml
                version = yaml.__version__ if hasattr(yaml, '__version__') else 'installed'
            else:
                module = __import__(package)
                version = module.__version__
            
            installed.append(package)
            print(f"✓ {package:12} {version:10} - {description}")
        except ImportError:
            missing.append(package)
            print(f"✗ {package:12} {'missing':10} - {description}")
    
    return installed, missing


def provide_recommendations(pyaedt_ok, ads_found):
    """Provide setup recommendations."""
    print_header("Recommendations")
    
    current_py = f"{sys.version_info.major}.{sys.version_info.minor}"
    
    if not ads_found:
        print("⚠ Could not detect ADS installation")
        print("\nOption 1: Specify ADS path manually")
        print("  Edit config/.env with your ADS installation path")
        print("\nOption 2: File-based integration (no ADS Python needed)")
        print("  Use PyAEDT to export files, import to ADS manually")
        
    elif pyaedt_ok and current_py >= "3.8":
        print("✓ Your Python is compatible with both PyAEDT and modern ADS")
        print("\nRecommended Setup: SINGLE ENVIRONMENT")
        print("  1. Install all dependencies:")
        print("     pip install -r requirements.txt")
        print("  2. Use this Python for both PyAEDT and ADS automation")
        print("\nIf you have ADS 2023+, you can use ADS Python for everything:")
        for ads in ads_found:
            if '2023' in ads['version'] or '2024' in ads['version']:
                print(f"\n  {ads['path']} -m pip install -r requirements.txt")
    
    else:
        print("⚠ Python version compatibility issue detected")
        print("\nRecommended Setup: DECOUPLED ARCHITECTURE")
        print("\n1. Create PyAEDT environment (Python 3.8+):")
        print("   python3.9 -m venv venv_pyaedt")
        print("   source venv_pyaedt/bin/activate")
        print("   pip install -r requirements_pyaedt.txt")
        print("\n2. Use ADS Python for ADS automation:")
        if ads_found:
            print(f"   {ads_found[0]['path']} -m pip install -r requirements_ads.txt")
        print("\n3. Run PyAEDT and ADS scripts separately")
        print("   See docs/python_compatibility.md for details")


def main():
    """Main compatibility check."""
    print("\n" + "=" * 70)
    print("  ADS Testbench Framework - Python Compatibility Checker")
    print("=" * 70)
    
    # Check Python version
    pyaedt_ok = check_python_version()
    
    # Find ADS installations
    ads_found = find_ads_python()
    
    # Check PyAEDT
    pyaedt_installed = check_pyaedt_installation()
    
    # Check dependencies
    installed, missing = check_dependencies()
    
    # Provide recommendations
    provide_recommendations(pyaedt_ok, ads_found)
    
    # Final summary
    print_header("Summary")
    print(f"Current Python: {sys.version_info.major}.{sys.version_info.minor}")
    print(f"PyAEDT Compatible: {'Yes' if pyaedt_ok else 'No'}")
    print(f"PyAEDT Installed: {'Yes' if pyaedt_installed else 'No'}")
    print(f"ADS Installations Found: {len(ads_found)}")
    print(f"Dependencies Installed: {len(installed)}/{len(installed) + len(missing)}")
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
    
    print("\nFor detailed compatibility information, see:")
    print("  docs/python_compatibility.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
