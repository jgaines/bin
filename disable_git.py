#!/usr/bin/env python3
import json
import os
import sys

def inject_disable_git():
    """
    Reads or creates a .code-workspace file in the current directory
    and injects '"git.enabled": false' into the 'settings' section.
    """
    current_dir = os.getcwd()
    workspace_file = os.path.basename(current_dir) + ".code-workspace"

    try:
        with open(workspace_file, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}  # Handle empty or invalid JSON

            if 'settings' not in data:
                data['settings'] = {}

            data['settings']['git.enabled'] = False

            f.seek(0)  # Go back to the beginning of the file
            json.dump(data, f, indent=4)
            f.truncate()  # Remove any remaining content if the new data is shorter

            print(f"Successfully injected 'git.enabled': false into {workspace_file}")

    except FileNotFoundError:
        try:
            with open('.vscode/settings.json', 'r+') as f:
                data = json.load(f)
                data['git.enabled'] = False
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                print(f"Successfully injected 'git.enabled': false into .vscode/settings.json")
        except FileNotFoundError:
            print("No .code-workspace or .vscode/settings.json file found.")
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    inject_disable_git()