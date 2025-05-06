#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
# ]
# ///
"""Analyze Python usage across all my project spaces.

1. Read the list of project spaces as command line arguments.
2. Scan each space for python executables.
3. Generate a report of python usage across all spaces.
4. Print the report to the console.
"""
from typing import Any


import argparse
import os
import sys
from pathlib import Path
import subprocess
from collections import defaultdict


def find_python_executables(directory: Path) -> dict[Path, Path]:
    """Find all Python executables in the given directory.
    Returns a dict mapping the found executable to its resolved (symlink target) path.
    """
    python_files: dict[Path, Path] = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "python":
                file_path = Path(root) / file
                if os.access(file_path, os.X_OK):
                    resolved_path = file_path.resolve() if file_path.is_symlink() else file_path
                    python_files[file_path] = resolved_path
    return python_files


def get_python_version(file_path: Path) -> str:
    """Get the Python version used by the file."""
    try:
        # with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        #     first_line = f.readline().strip()
        #     if first_line.startswith('#!') and 'python' in first_line:
        #         return first_line.split('python')[-1].strip()
        
        # Try to execute the file with -V to get version
        try:
            result = subprocess.run([file_path, '-V'], 
                                   capture_output=True, 
                                   text=True,
                                   timeout=2)
            if result.stdout and 'Python' in result.stdout:
                return result.stdout.strip()
            if result.stderr and 'Python' in result.stderr:
                return result.stderr.strip()
        except (subprocess.SubprocessError, PermissionError):
            pass
        return "Unknown"
    except Exception as e:
        return f"Error: {str(e)}"


def analyze_project(project_path: Path):
    """Analyze a project for Python usage."""
    if not project_path.exists():
        print(f"Warning: Project path does not exist: {project_path}", file=sys.stderr)
        return None
    
    python_files = find_python_executables(project_path)
    results: dict[str, dict[str, str]] = {}
    
    for file_path, resolved_path in python_files.items():
        version = get_python_version(resolved_path)
        results[str(file_path)] = {
            "resolved": str(resolved_path),
            "version": version
        }
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Analyze Python usage across projects')
    _ = parser.add_argument('projects', nargs='+', type=Path, help='Project root directories to analyze')
    args = parser.parse_args()

    if not args.projects:
        print("No project root directories provided. Please specify at least one project root directory.")
        parser.print_help()
        sys.exit(1)
    
    all_results: dict[str, dict[str, dict[str, str]]] = {}
    version_count: defaultdict[str, int] = defaultdict(int)
    
    for project in args.projects:
        project_results = analyze_project(project)
        all_results[project] = project_results
        
        for _, info in project_results.items():
            version_count[info["version"]] += 1
    
    # Print report
    print("\nPYTHON USAGE REPORT")
    print("=" * 50)
    
    for project, results in all_results.items():
        print(f"\n{project}: {len(results)} Python executables")
        if results:
            for file_path, info in results.items():
                print(f"  {file_path} -> {info['resolved']}: {info['version']}")
    
    print("\nSUMMARY")
    print("=" * 50)
    total_files = sum(len(results) for results in all_results.values())
    print(f"Total Python executables found: {total_files}")
    
    if version_count:
        print("\nVersion distribution:")
        for version, count in sorted(version_count.items()):
            print(f"  {version}: {count} files ({count/total_files*100:.1f}%)")

if __name__ == "__main__":
    main()