"""
Setup script for ADS Testbench Development Framework
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text().splitlines()
    # Remove comments and empty lines
    requirements = [r.strip() for r in requirements if r.strip() and not r.startswith('#')]

setup(
    name="ads-testbench-framework",
    version="0.1.0",
    author="ADS Testbench Development Team",
    author_email="",
    description="ADS Testbench Development with PyAEDT Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'hfss-to-ads=workflows.hfss_to_ads_workflow:main',
            'maxwell-to-ads=workflows.maxwell_to_ads_workflow:main',
        ],
    },
    include_package_data=True,
    package_data={
        'testbenches': ['*.yaml'],
        'config': ['*.yaml', '*.template'],
    },
)
