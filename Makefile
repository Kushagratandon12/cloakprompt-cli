# Makefile for CloakPrompt CLI

.PHONY: help install install-dev test lint format clean demo run-cli

# Default target
help:
	@echo "🔒 CloakPrompt CLI - Available commands:"
	@echo ""
	@echo "Installation:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  test         Run tests"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code with black"
	@echo "  demo         Run demonstration script"
	@echo ""
	@echo "CLI:"
	@echo "  run-cli      Run the CLI tool directly"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean        Clean up generated files"
	@echo "  help         Show this help message"

# Install production dependencies
install:
	pip install -r requirements.txt
	pip install -e .

# Install development dependencies
install-dev:
	pip install -r requirements.txt
	pip install -e .
	pip install pytest pytest-cov black flake8 mypy

# Run tests
test:
	python -m pytest tests/ -v --cov=cloakprompt

# Run linting
lint:
	flake8 cloakprompt/ --max-line-length=88 --extend-ignore=E203,W503
	mypy cloakprompt/ --ignore-missing-imports

# Format code
format:
	black cloakprompt/ --line-length=88
	black test_example.py --line-length=88

# Run demo script
demo:
	python test_example.py

# Run CLI directly
run-cli:
	python -m cloakprompt.cli --help

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type f -name ".coverage.*" -delete

# Quick test of the CLI
test-cli:
	@echo "Testing CLI functionality..."
	@echo "1. Testing help command..."
	python -m cloakprompt.cli --help
	@echo ""
	@echo "2. Testing patterns command..."
	python -m cloakprompt.cli patterns
	@echo ""
	@echo "3. Testing redaction with sample text..."
	echo "My AWS key is AKIA1234567890ABCDEF" | python -m cloakprompt.cli redact --stdin --quiet
	@echo ""
	@echo "✅ CLI tests completed!"

# Install and test everything
all: install-dev test lint format demo test-cli
	@echo "🎉 All tasks completed successfully!"

