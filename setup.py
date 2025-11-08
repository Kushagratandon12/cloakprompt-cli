#!/usr/bin/env python3
"""
Setup script for CloakPrompt.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="cloakprompt",
    version="1.0.0",
    author="Kushagra Tandon",
    author_email="kushagra.tandon.124@gmail.com",
    description="Secure text redaction for LLM interactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kushagratandon12/cloakprompt-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cloakprompt=cloakprompt.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cloakprompt": ["config/*.yaml"],
    },
    zip_safe=False,
    keywords="security, redaction, cli, llm, privacy, data-protection",
    project_urls={
        "Bug Reports": "https://github.com/Kushagratandon12/cloakprompt-cli/issues",
        "Source": "https://github.com/Kushagratandon12/cloakprompt-cli",
        "Documentation": "https://github.com/Kushagratandon12/cloakprompt-cli#readme",
    },
)
