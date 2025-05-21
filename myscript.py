#!/usr/bin/env python3

import sys
import fnmatch
import argparse
import os
import subprocess
import datetime
import logging

def setup_logging():
    """Setup logging configuration to write to both file and console."""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Generate timestamp for log file
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'logs/policy_report_{timestamp}.log'
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return log_file

def install_package(package_name):
    """Install a package with user permission and suppress warnings."""
    logging.info(f"{package_name} package is not installed. This package is required for better output formatting.")
    response = input(f"Would you like to install {package_name}? (y/n): ").lower()
    if response == 'y':
        try:
            # Suppress pip warnings by redirecting stderr
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet", "--no-warn-script-location", package_name],
                stderr=subprocess.DEVNULL
            )
            logging.info(f"{package_name} installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install {package_name}: {e}")
            return False
    return False

def check_and_install_pyyaml():
    """Check if PyYAML is installed, if not, ask user and install it."""
    try:
        import yaml
        return True
    except ImportError:
        return install_package("pyyaml")

def matches_any_pattern(namespace, patterns):
    """Check if namespace matches any of the exclusion patterns."""
    return any(fnmatch.fnmatch(namespace, pattern) for pattern in patterns)

def process_policy_report(file_path, exclude_namespaces):
    """Process the policy report and filter results."""
    if not os.path.exists(file_path):
        logging.error(f"Error: File '{file_path}' does not exist")
        sys.exit(1)

    try:
        import yaml
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        sys.exit(1)

    # List to store results for tabulate
    results_table = []
    headers = ["Policy", "Rule", "Kind", "Resource Name", "Namespace", "Status"]

    # Process each result
    for result in data.get('results', []):
        # Skip if not a failure
        if result.get('result') != 'fail':
            continue

        # Get resource details
        for resource in result.get('resources', []):
            namespace = resource.get('namespace', '')
            
            # Skip if namespace matches any exclusion pattern
            if exclude_namespaces and matches_any_pattern(namespace, exclude_namespaces):
                continue

            # Add to results table
            results_table.append([
                result.get('policy', 'N/A'),
                result.get('rule', 'N/A'),
                resource.get('kind', 'N/A'),
                resource.get('name', 'N/A'),
                namespace,
                result.get('result', 'N/A')
            ])

    # Print results using tabulate
    if results_table:
        try:
            from tabulate import tabulate
            logging.info("\nPolicy Violations Report:")
            logging.info(tabulate(results_table, headers=headers, tablefmt="grid"))
            logging.info(f"\nTotal violations found: {len(results_table)}")
        except ImportError:
            if install_package("tabulate"):
                from tabulate import tabulate
                logging.info("\nPolicy Violations Report:")
                logging.info(tabulate(results_table, headers=headers, tablefmt="grid"))
                logging.info(f"\nTotal violations found: {len(results_table)}")
            else:
                logging.info("\nShowing plain output:")
                for row in results_table:
                    logging.info(" ".join(row))
    else:
        logging.info("No policy violations found.")

def main():
    # Setup logging
    log_file = setup_logging()
    logging.info(f"Starting policy report analysis. Log file: {log_file}")

    # Check and install PyYAML if needed
    if not check_and_install_pyyaml():
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Process Kyverno policy report and filter results.')
    parser.add_argument('input_file', help='Path to the policy report YAML file')
    parser.add_argument('exclude_namespaces', nargs='*', help='Namespaces to exclude (supports wildcards)')
    args = parser.parse_args()

    # Log the command line arguments
    logging.info(f"Input file: {args.input_file}")
    if args.exclude_namespaces:
        logging.info(f"Excluding namespaces: {', '.join(args.exclude_namespaces)}")

    # Process the report
    process_policy_report(args.input_file, args.exclude_namespaces)

if __name__ == '__main__':
    main() 
