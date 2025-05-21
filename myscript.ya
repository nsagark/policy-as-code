#!/usr/bin/env python3

import sys
import fnmatch
import argparse
import os
import subprocess

def install_package(package_name):
    """Install a package with user permission and suppress warnings."""
    print(f"{package_name} package is not installed. This package is required for better output formatting.")
    response = input(f"Would you like to install {package_name}? (y/n): ").lower()
    if response == 'y':
        try:
            # Suppress pip warnings by redirecting stderr
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet", "--no-warn-script-location", package_name],
                stderr=subprocess.DEVNULL
            )
            print(f"{package_name} installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package_name}: {e}")
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
        print(f"Error: File '{file_path}' does not exist")
        sys.exit(1)

    try:
        import yaml
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
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
            print("\nPolicy Violations Report:")
            print(tabulate(results_table, headers=headers, tablefmt="grid"))
            print(f"\nTotal violations found: {len(results_table)}")
        except ImportError:
            if install_package("tabulate"):
                from tabulate import tabulate
                print("\nPolicy Violations Report:")
                print(tabulate(results_table, headers=headers, tablefmt="grid"))
                print(f"\nTotal violations found: {len(results_table)}")
            else:
                print("\nShowing plain output:")
                for row in results_table:
                    print(" ".join(row))
    else:
        print("No policy violations found.")

def main():
    # Check and install PyYAML if needed
    if not check_and_install_pyyaml():
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Process Kyverno policy report and filter results.')
    parser.add_argument('input_file', help='Path to the policy report YAML file')
    parser.add_argument('exclude_namespaces', nargs='*', help='Namespaces to exclude (supports wildcards)')
    args = parser.parse_args()

    # Process the report
    process_policy_report(args.input_file, args.exclude_namespaces)

if __name__ == '__main__':
    main() 
