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

import argparse
import os
import sys
from pathlib import Path
import subprocess
from collections import defaultdict
from os.path import expanduser
from typing import cast


def find_python_executables(directory: Path, ignore: list[str], verbose: int) -> dict[Path, Path]:
    """Find all Python executables in the given directory, ignoring specified folders."""
    python_files: dict[Path, Path] = {}
    for root, dirs, files in os.walk(directory):
        # Remove ignored directories from the walk
        dirs[:] = [d for d in dirs if d not in ignore]
        if verbose >= 3:
            print(f"Scanning directory: {root}")
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
            result = subprocess.run([file_path, "-V"], capture_output=True, text=True, timeout=2)
            if result.stdout and "Python" in result.stdout:
                return result.stdout.strip().replace("Python ", "")
            if result.stderr and "Python" in result.stderr:
                return result.stderr.strip().replace("Python ", "")
        except (subprocess.SubprocessError, PermissionError):
            pass
        return "Unknown"
    except Exception as e:
        return f"Error: {str(e)}"


def analyze_project(project_path: Path, ignore: list[str], verbose: int):
    """Analyze a project for Python usage, ignoring specified folders."""
    if not project_path.exists():
        print(f"Warning: Project path does not exist: {project_path}", file=sys.stderr)
        return None

    if verbose >= 2:
        print(f"Analyzing project: {project_path}")

    python_files = find_python_executables(project_path, ignore, verbose)
    results: dict[str, dict[str, str]] = {}

    for file_path, resolved_path in python_files.items():
        version = get_python_version(resolved_path)
        results[str(file_path)] = {"resolved": str(resolved_path), "version": version}
    return results


class MyArgs(argparse.Namespace):
    projects: list[Path] = []
    ignore: list[str] = []
    verbose: int = 0


def version_key(version_str: str) -> list[float | int | str]:
    """Create a key for sorting version strings properly."""
    # Handle unknown or error versions
    if version_str.startswith("Unknown") or version_str.startswith("Error"):
        return [float("inf")]  # Place at the end

    # Extract version numbers, handling both '3.10.2' and similar formats
    try:
        return [int(x) if x.isdigit() else x for x in version_str.split(".")]
    except Exception:
        return [version_str]  # Return as is if parsing fails


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python usage across projects", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    _ = parser.add_argument("projects", nargs="+", type=Path, help="Project root directories to analyze")
    _ = parser.add_argument(
        "--ignore",
        nargs="*",
        default=[
            ".cache",
            ".coverage",
            ".git",
            ".idea",
            ".magic",
            ".mypy_cache",
            ".pytest_cache",
            ".tox",
            ".vscode",
            ".zed",
            "__pycache__",
        ],
        help="Directories to ignore",
    )
    _ = parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity level (use multiple times for more detail)",
    )
    args: MyArgs = cast(MyArgs, parser.parse_args())

    if not args.projects:
        print("No project root directories provided. Please specify at least one project root directory.")
        parser.print_help()
        sys.exit(1)

    all_results: dict[Path, dict[str, dict[str, str]]] = {}
    version_count: defaultdict[str, int] = defaultdict(int)

    for project in args.projects:
        project_results = analyze_project(project, args.ignore, args.verbose)
        if project_results is None:
            print(f"Skipping project {project} due to errors.")
            continue
        all_results[project] = project_results

        for _, info in project_results.items():
            version_count[info["version"]] += 1

    if args.verbose >= 1:
        print("Ignored directories:", args.ignore)

    # Print report
    print("\nPYTHON USAGE REPORT")
    print("=" * 50)

    home_dir = expanduser("~")
    for project, results in all_results.items():
        compact_project = str(project).replace(home_dir, "~")
        print(f"\n{compact_project}: {len(results)} Python executables")
        if results:
            max_version_length = max(len(info["version"]) for info in results.values())

            # Sort by resolved path
            sorted_paths = sorted(results.items(), key=lambda x: x[1]["resolved"])

            for file_path, info in sorted_paths:
                compact_file_path = file_path.replace(home_dir, "~")
                compact_resolved_path = info["resolved"].replace(home_dir, "~")
                print(f"  {info['version']:<{max_version_length}} {compact_resolved_path} <- {compact_file_path}")

    print("\nSUMMARY")
    print("=" * 50)
    total_files = sum(len(results) for results in all_results.values())
    print(f"Total Python executables found: {total_files}")

    if version_count:
        print("\nVersion distribution:")
        # Sort by version numbers properly
        for version, count in sorted(version_count.items(), key=lambda x: version_key(x[0])):
            print(f"  {version}: {count} files ({count / total_files * 100:.1f}%)")


if __name__ == "__main__":
    main()
