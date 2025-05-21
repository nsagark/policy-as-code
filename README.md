# Kyverno Policy Report Analyzer

A Python script to analyze and format Kyverno policy violation reports from Kubernetes clusters. This tool helps in identifying and displaying policy violations in a clear, tabulated format.

## Introduction

This script processes Kyverno policy reports (in YAML format) and provides a clear view of policy violations. It supports:
- Filtering violations by namespace
- Wildcard namespace exclusions
- Formatted table output
- Plain text output option

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- Access to a Kyverno policy report YAML file

### Python Version Check

To check your Python version, run:
```bash
python3 --version
```

If your Python version is below 3.6, you'll need to upgrade. Here's how:

#### For macOS:
```bash
brew install python@3.9
```

#### For Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3.9
```

#### For Windows:
Download and install from [Python's official website](https://www.python.org/downloads/)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Make the script executable:
```bash
chmod +x myscript.py
```

## Usage

### Basic Usage

```bash
./myscript.py <policy-report-file> [namespace-exclusions...]
```

### Examples

1. View all violations:
```bash
./myscript.py clusteroutput.yaml
```

2. Exclude specific namespaces:
```bash
./myscript.py clusteroutput.yaml kyverno nirmata
```

3. Use wildcards for namespace exclusions:
```bash
./myscript.py clusteroutput.yaml kyverno* *test* nirmata*
```

### Output Format

The script provides two output formats:

1. **Table Format** (default if tabulate is installed):
```
+----------------+--------------------------+------------+-----------------------------------------+--------------------+----------+
| Policy         | Rule                     | Kind       | Resource Name                           | Namespace          | Status   |
+================+==========================+============+=========================================+====================+==========+
| require-labels | check-for-labels         | Pod        | local-path-provisioner-57c5987fd4-gqk2b | local-path-storage | fail     |
+----------------+--------------------------+------------+-----------------------------------------+--------------------+----------+
```

2. **Plain Text Format** (fallback if tabulate is not installed):
```
require-labels check-for-labels Pod local-path-provisioner-57c5987fd4-gqk2b local-path-storage fail
```

## Package Dependencies

The script requires two optional Python packages:
- `pyyaml`: For YAML file processing
- `tabulate`: For formatted table output

The script will prompt to install these packages if they're not present. You can choose to:
- Install both for the best experience (table output)
- Install only pyyaml for basic functionality (plain text output)
- Decline installation of either package

## Troubleshooting

### Common Issues

1. **Permission Denied**
```bash
chmod +x myscript.py
```

2. **Python Version Issues**
If you see syntax errors, ensure you're using Python 3.6+:
```bash
python3 --version
```

3. **Package Installation Fails**
Try installing packages manually:
```bash
pip3 install pyyaml tabulate
```

4. **File Not Found**
Ensure the policy report file exists and the path is correct:
```bash
ls -l clusteroutput.yaml
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Your chosen license]

## Author

[Your name/organization] 
