#!/usr/bin/env python3
import json
import os
import sys
import argparse

def check_git_status(workspace_file, vscode_settings):
    """
    Checks the current status of git.enabled in workspace or settings file
    Returns a tuple of (file_type, status) or None if no relevant file found
    """
    if os.path.exists(workspace_file):
        try:
            with open(workspace_file, 'r') as f:
                data = json.load(f)
                if 'settings' in data and 'git.enabled' in data['settings']:
                    return ('workspace', data['settings']['git.enabled'])
                else:
                    return ('workspace', None)
        except json.JSONDecodeError:
            return ('workspace', None)
        except Exception as e:
            print(f"Error reading {workspace_file}: {e}")
            return None

    if os.path.exists(vscode_settings):
        try:
            with open(vscode_settings, 'r') as f:
                data = json.load(f)
                if 'git.enabled' in data:
                    return ('vscode', data['git.enabled'])
                else:
                    return ('vscode', None)
        except json.JSONDecodeError:
            return ('vscode', None)
        except Exception as e:
            print(f"Error reading {vscode_settings}: {e}")
            return None

    # Check global VS Code settings
    global_settings = os.path.expanduser('~/.config/Code/User/settings.json')
    if os.path.exists(global_settings):
        try:
            with open(global_settings, 'r') as f:
                data = json.load(f)
                if 'git.enabled' in data:
                    return ('global', data['git.enabled'])
                else:
                    return ('global', None)
        except json.JSONDecodeError:
            return ('global', None)
        except Exception as e:
            print(f"Error reading {global_settings}: {e}")
            return None

    return None

def report_git_status():
    """
    Reports the current state of git.enabled setting
    """
    current_dir = os.getcwd()
    workspace_file = os.path.basename(current_dir) + ".code-workspace"
    vscode_settings = '.vscode/settings.json'
    
    status = check_git_status(workspace_file, vscode_settings)
    
    if status is None:
        print("No .code-workspace or .vscode/settings.json file found.")
        return
    
    file_type, git_enabled = status
    if git_enabled is None:
        print(f"Found {file_type} file, but git.enabled setting is not configured (which means it is enabled).")
    else:
        print(f"Current git.enabled setting in {file_type} file is: {git_enabled}")

def set_git_enabled(value):
    """
    Sets git.enabled to the specified value (True or False)
    """
    current_dir = os.getcwd()
    workspace_file = os.path.basename(current_dir) + ".code-workspace"
    vscode_settings = '.vscode/settings.json'
    
    action_text = "enabled" if value else "disabled"
    
    # Try to set the value in the workspace file first
    try:
        with open(workspace_file, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}  # Handle empty or invalid JSON

            if 'settings' not in data:
                data['settings'] = {}

            data['settings']['git.enabled'] = value

            f.seek(0)  # Go back to the beginning of the file
            json.dump(data, f, indent=4)
            f.truncate()  # Remove any remaining content if the new data is shorter

            print(f"Successfully set 'git.enabled': {value} in {workspace_file}")

    except FileNotFoundError:
        try:
            # Ensure .vscode directory exists
            os.makedirs(os.path.dirname(vscode_settings), exist_ok=True)
            
            # Try to open the file for reading and writing, or create it if it doesn't exist
            try:
                with open(vscode_settings, 'r') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {}
            except FileNotFoundError:
                data = {}
                
            data['git.enabled'] = value
            
            with open(vscode_settings, 'w') as f:
                json.dump(data, f, indent=4)
                
            print(f"Successfully set 'git.enabled': {value} in {vscode_settings}")
        except Exception as e:
            print(f"An error occurred while updating VSCode settings: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check or change git integration in VS Code")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--disable", "--off", "-d", action="store_true", help="Disable git integration")
    group.add_argument("--enable", "--on", "-e", action="store_true", help="Enable git integration")
    args = parser.parse_args()
    
    # Use appropriate function based on arguments
    if args.disable:
        set_git_enabled(False)
    elif args.enable:
        set_git_enabled(True)
    else:
        report_git_status()  # Just report status