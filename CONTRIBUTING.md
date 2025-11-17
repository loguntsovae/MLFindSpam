# Contributing to SMS Spam Classifier

First off, thank you for considering contributing to SMS Spam Classifier! It's people like you that make this project a great learning resource for the ML community.

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include Python version, OS, and dependency versions**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain which behavior you expected to see instead**
- **Explain why this enhancement would be useful**

### Pull Requests

Please follow these steps to have your contribution considered:

1. **Fork the repo** and create your branch from `main`
2. **If you've added code that should be tested**, add tests
3. **If you've changed APIs**, update the documentation
4. **Ensure the test suite passes** (`make test`)
5. **Make sure your code follows the existing style**
6. **Write a clear commit message**

## Development Process

### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/your-username/spam_classifier.git
cd spam_classifier

# Install dependencies
pip install -r requirements.txt

# Run tests
make test
```

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage

# Run specific test file
pytest tests/test_predict.py -v
```

### Code Style

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Write self-documenting code

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add support for multilingual spam detection

- Implement language detection using langdetect
- Add training data for Spanish and French
- Update documentation with language support info

Fixes #123
```

### Documentation

- Update README.md if you change functionality
- Update relevant files in `/docs` directory
- Add docstrings to new functions and classes
- Include code examples where appropriate

## Project Structure

```
spam_classifier/
├── src/           # Source code
├── tests/         # Test files
├── ui/            # Web interface
├── docs/          # Documentation
└── data/          # Data files
```

## Testing Guidelines

- Write tests for all new features
- Maintain test coverage above 80%
- Test edge cases and error conditions
- Use descriptive test names
- Keep tests independent and isolated

## Areas for Contribution

Here are some areas where contributions would be particularly valuable:

### Features
- Additional ML models (SVM, Random Forest, Neural Networks)
- Support for other languages
- Real-time spam detection
- API endpoint for integration
- Mobile app interface
- Batch processing support

### Improvements
- Enhanced text preprocessing
- Better feature engineering
- Model hyperparameter tuning
- Performance optimization
- Error handling
- Logging system

### Documentation
- More usage examples
- Video tutorials
- Architecture diagrams
- API documentation
- Deployment guides

### Testing
- Integration tests
- Performance tests
- Edge case coverage
- Mock data generation

## Questions?

Feel free to open an issue with the tag `question` if you have any questions about contributing.

## Recognition

Contributors will be recognized in the project README and release notes.

Thank you for your interest in improving SMS Spam Classifier! 🎉
