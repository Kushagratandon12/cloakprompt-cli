# 🔒 CloakPrompt CLI

[![PyPI version](https://badge.fury.io/py/cloakprompt.svg)](https://badge.fury.io/py/cloakprompt)

**Secure text redaction for LLM interactions**

CloakPrompt is a command-line tool that automatically detects and redacts sensitive information (API keys, passwords, emails, IPs, etc.) from text before sending it to Large Language Models (LLMs). This helps protect your privacy and security when using AI services.

## ✨ Features

- **Comprehensive Pattern Detection**: Pre-configured regex patterns for common sensitive data types
- **Multiple Input Sources**: Support for inline text, files, and stdin piping
- **Custom Configuration**: Extend or override default patterns with your own security rules
- **Rich Output**: Beautiful terminal interface with progress indicators and detailed reporting
- **Production Ready**: Well-tested, documented, and maintainable code
- **Privacy First**: No data is sent to external services - all processing happens locally

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Kushagratandon12/cloakprompt-cli.git
cd cloakprompt-cli

# Install the package with dependencies
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Basic Usage

```bash
# Redact inline text
cloakprompt redact --text "my secret key is AKIA1234567890ABCDEF"

# Redact a file
cloakprompt redact --file config.log

# Redact from stdin (piped input)
echo "secret data" | cloakprompt redact --stdin

# Use custom configuration
cloakprompt redact --file app.log --config security.yaml
```

## 📖 Detailed Usage

![img.png](document/image.png)

### Command Structure

```bash
cloakprompt redact [OPTIONS]
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--text TEXT` | `-t` | Text to redact (inline) |
| `--file PATH` | `-f` | File to redact |
| `--stdin` | | Read from stdin (piped input) |
| `--config PATH` | `-c` | Custom configuration file |
| `--verbose` | `-v` | Enable verbose logging |
| `--quiet` | `-q` | Suppress all output except errors |
| `--summary` | `-s` | Show pattern summary and exit |
| `--details` | `-d` | Show detailed redaction information |

### Examples

#### 1. Redact Inline Text
```bash
cloakprompt redact --text "My AWS key is AKIA1234567890ABCDEF and password is secret123"
```

**Output:**
```
🔒 CLOAKPROMPT
Secure text redaction for LLM interactions

✓ Redacted 2 sensitive items
My AWS key is <REDACT_AWS_ACCESS_KEY> and password is <REDACT_PASSWORD>
```

#### 2. Redact File Content
```bash
cloakprompt redact --file application.log
```

#### 3. Redact with Custom Configuration
```bash
cloakprompt redact --file config.yaml --config my-security-rules.yaml
```

#### 4. Redact from Stdin
```bash
cat sensitive.log | cloakprompt redact --stdin
```

#### 5. Show Pattern Summary
```bash
cloakprompt patterns
```

#### 6. Show Redaction Details
```bash
cloakprompt redact --text "secret data" --details
```

## 🛡️ Supported Patterns

CloakPrompt comes with pre-configured patterns for:

- **API Keys**: OpenAI, Google, Stripe, GitHub, Slack, etc.
- **AWS Credentials**: Access keys, secret keys
- **Database URLs**: PostgreSQL, MySQL, Redis, MongoDB, etc.
- **Tokens**: JWT, OAuth, Personal Access Tokens
- **Kubernetes**: Configs, secrets, service accounts
- **SSH Keys**: Private key files
- **Cloud Provider Keys**: Azure, GCP, DigitalOcean, etc.
- **PII**: Emails, phone numbers, IP addresses, credit cards
- **Generic Secrets**: Base64 encoded data, long random strings

## ⚙️ Configuration

### Default Configuration

The tool uses `cloakprompt/config/regex_cleanup.yaml` by default, which contains comprehensive patterns for common sensitive data types.

### Custom Configuration

Create your own `security.yaml` file to extend or override default patterns:

```yaml
# Example custom security.yaml
patterns:
  CUSTOM_PATTERNS:
    description: "Custom patterns for my organization"
    rules:
      - name: internal_api_key
        placeholder: <REDACT_INTERNAL_API_KEY>
        regex: '\binternal[_-]?api[_-]?key\s*[:=]\s*["'']?[A-Za-z0-9_\-]{20,}["'']?\b'
      
      - name: company_secret
        placeholder: <REDACT_COMPANY_SECRET>
        regex: '\bcompany[_-]?secret\s*[:=]\s*["'']?[A-Za-z0-9!@#$%^&*()_+=-]{8,}["'']?\b'
```

### Configuration Merging

Custom configurations are merged with the default configuration:
- New categories are added
- Existing rules are updated if they have the same name
- New rules are appended to existing categories

## 🏗️ Architecture

```
cloakprompt/
├── cli.py              # CLI entry point (Typer)
├── core/
│   ├── parser.py       # YAML configuration parser
│   └── redactor.py     # Text redaction engine
├── utils/
│   └── file_loader.py  # Input handling utilities
└── config/
    └── regex_cleanup.yaml  # Default patterns
```

### Core Components

- **`ConfigParser`**: Loads and merges YAML configuration files
- **`TextRedactor`**: Applies regex patterns to redact sensitive information
- **`InputLoader`**: Handles different input sources (text, file, stdin)
- **`CLI`**: Orchestrates the redaction process with rich terminal output

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=cloakprompt
```

## 📦 Development

### Project Structure

```
├── cloakprompt/           # Main package
│   ├── __init__.py       # Package initialization
│   ├── cli.py            # CLI entry point
│   ├── core/             # Core functionality
│   │   ├── __init__.py
│   │   ├── parser.py     # Configuration parser
│   │   └── redactor.py   # Text redactor
│   ├── utils/            # Utility functions
│   │   ├── __init__.py
│   │   └── file_loader.py # Input handling
│   └── config/           # Configuration files
│       └── regex_cleanup.yaml
├── pyproject.toml        # Project configuration and dependencies
├── setup.py              # Installation script (minimal, for backward compatibility)
└── README.md             # This file
```

### Adding New Patterns

1. Edit `cloakprompt/config/regex_cleanup.yaml`
2. Add new rules under appropriate categories
3. Test with sample data
4. Update documentation if needed

### Code Quality

The project uses:
- **Type hints** for better code quality
- **Comprehensive docstrings** for all functions
- **Logging** for debugging and monitoring
- **Error handling** for robust operation
- **Unit tests** for reliability

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Kushagratandon12/cloakprompt-cli/issues)
- **Documentation**: [GitHub README](https://github.com/Kushagratandon12/cloakprompt-cli#readme)

**Created by [Kushagra Tandon](https://github.com/Kushagratandon12)**

LLM Security | Prompt Redaction | AI Tools Developer

## 🔒 Security

- All processing happens locally - no data is sent to external services
- Regex patterns are designed to catch common sensitive data formats
- Custom configurations allow organization-specific security rules
- The tool is open source for transparency and community review

---

**Built with ❤️ for privacy and security in AI interactions**