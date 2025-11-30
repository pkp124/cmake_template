# Makefile for ADS Testbench Development Framework

.PHONY: help install test lint format clean docs

help:
	@echo "Available targets:"
	@echo "  install    - Install package and dependencies"
	@echo "  test       - Run tests"
	@echo "  lint       - Run linters"
	@echo "  format     - Format code with black"
	@echo "  clean      - Remove build artifacts"
	@echo "  docs       - Build documentation"

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=ads_automation --cov=pyaedt_integration --cov=utils --cov-report=html

lint:
	flake8 ads_automation/ pyaedt_integration/ workflows/ utils/
	pylint ads_automation/ pyaedt_integration/ workflows/ utils/

format:
	black ads_automation/ pyaedt_integration/ workflows/ utils/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/

docs:
	@echo "Documentation is in docs/ directory"
	@echo "Open docs/getting_started.md to begin"
