# Contributing Guidelines

Thank you for your interest in contributing to the ADS Testbench Development Framework!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Development Setup

```bash
# Clone repository
git clone <your-fork-url>
cd <repository-name>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Code Style

### Python Style Guide

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Maximum line length: 100 characters

### Formatting

Use `black` for code formatting:

```bash
black ads_automation/ pyaedt_integration/ workflows/ utils/
```

### Linting

Use `flake8` for linting:

```bash
flake8 ads_automation/ pyaedt_integration/ workflows/ utils/
```

## Documentation

- Update docstrings for new functions/classes
- Add examples to documentation
- Update README.md if adding new features
- Add workflow examples for new capabilities

### Docstring Format

```python
def my_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When invalid input
    """
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ads_automation --cov=pyaedt_integration --cov=utils

# Run specific test file
pytest tests/test_data_converter.py

# Run specific test
pytest tests/test_data_converter.py::TestAEDTtoADSConverter::test_converter_initialization
```

### Writing Tests

- Write unit tests for new functions
- Use pytest fixtures for setup/teardown
- Aim for >80% code coverage
- Test both success and failure cases

Example:

```python
import pytest
from my_module import my_function

class TestMyFunction:
    """Test cases for my_function"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample test data"""
        return {"key": "value"}
    
    def test_success_case(self, sample_data):
        """Test successful execution"""
        result = my_function(sample_data)
        assert result == expected_value
    
    def test_error_case(self):
        """Test error handling"""
        with pytest.raises(ValueError):
            my_function(None)
```

## Commit Messages

Use clear, descriptive commit messages:

```
Add HFSS field data extraction feature

- Implement extract_field_data method in HFSSDataExtractor
- Add support for E-field and H-field quantities
- Include unit tests for field extraction
- Update documentation with examples
```

Format:
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description (if needed)
- List specific changes

## Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make Changes**
   - Write code
   - Add tests
   - Update documentation

3. **Test Changes**
   ```bash
   pytest
   flake8
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add my new feature"
   ```

5. **Push to Fork**
   ```bash
   git push origin feature/my-new-feature
   ```

6. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Describe your changes
   - Link related issues

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] All CI checks passing

## Adding New Features

### New Workflow

1. Create workflow script in `workflows/`
2. Implement workflow class
3. Add command-line interface
4. Create example in `examples/`
5. Add documentation in `docs/`
6. Write tests

### New Testbench Template

1. Create YAML file in `testbenches/`
2. Define template structure
3. Add example usage in documentation
4. Update testbench generator if needed

### New Extractor

1. Create extractor class in `pyaedt_integration/`
2. Implement extraction methods
3. Add to `__init__.py`
4. Write unit tests
5. Add examples and documentation

## Code Review

All submissions require review. We aim to:
- Provide constructive feedback
- Respond within 2-3 business days
- Help improve code quality

## Reporting Bugs

Use GitHub Issues to report bugs:

**Bug Report Template:**
```
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Step 1
2. Step 2
3. ...

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.9.7]
- ADS version: [e.g., 2023]
- AEDT version: [e.g., 2023 R1]
- PyAEDT version: [e.g., 0.7.0]

**Additional Context**
Any other relevant information
```

## Feature Requests

Use GitHub Issues for feature requests:

**Feature Request Template:**
```
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Implementation**
How could this be implemented?

**Alternatives Considered**
Other approaches you've considered

**Additional Context**
Any other relevant information
```

## Questions?

- Check documentation in `docs/`
- Review examples in `examples/`
- Open an issue for questions
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing!
