#!/usr/bin/env python3
import json
import sys
import argparse
from pathlib import Path

def check_git_status(workspace_file, vscode_settings):
    """
    Checks the current status of git.enabled in workspace or settings file
    Returns a tuple of (file_type, status) or None if no relevant file found
    """
    if workspace_file.exists():
        try:
            data = json.loads(workspace_file.read_text())
            if 'settings' in data and 'git.enabled' in data['settings']:
                return (workspace_file.name, data['settings']['git.enabled'])
            else:
                return (workspace_file.name, None)
        except json.JSONDecodeError:
            return (workspace_file.name, None)
        except Exception as e:
            print(f"Error reading {workspace_file}: {e}")
            return None

    if vscode_settings.exists():
        try:
            data = json.loads(vscode_settings.read_text())
            if 'git.enabled' in data:
                return ('.vscode/settings.json', data['git.enabled'])
            else:
                return ('.vscode/settings.json', None)
        except json.JSONDecodeError:
            return ('.vscode/settings.json', None)
        except Exception as e:
            print(f"Error reading {vscode_settings}: {e}")
            return None

    # Check global VS Code settings
    global_settings = Path.home() / '.config' / 'Code' / 'User' / 'settings.json'
    if global_settings.exists():
        try:
            data = json.loads(global_settings.read_text())
            if 'git.enabled' in data:
                return ('User settings', data['git.enabled'])
            else:
                return ('User settings', None)
        except json.JSONDecodeError:
            return ('User settings', None)
        except Exception as e:
            print(f"Error reading {global_settings}: {e}")
            return None

    return None

def report_git_status():
    """
    Reports the current state of git.enabled setting
    """
    current_dir = Path.cwd()
    workspace_name = current_dir.name + ".code-workspace"
    workspace_path = current_dir / workspace_name
    vscode_settings = current_dir / '.vscode' / 'settings.json'
    
    status = check_git_status(workspace_path, vscode_settings)
    
    if status is None:
        print("No .code-workspace or .vscode/settings.json file found.")
        return
    
    file_type, git_enabled = status
    if git_enabled is None:
        print(f"Found {file_type} file, but git.enabled setting is not configured (which means it is enabled).")
    else:
        print(f"Current git.enabled setting in {file_type} is: {git_enabled}")

def set_git_enabled(value):
    """
    Sets git.enabled to the specified value (True or False)
    """
    current_dir = Path.cwd()
    workspace_name = current_dir.name + ".code-workspace"
    workspace_file = current_dir / workspace_name
    vscode_settings = current_dir / '.vscode' / 'settings.json'
    
    action_text = "enabled" if value else "disabled"
    
    # Try to set the value in the workspace file first
    try:
        if workspace_file.exists():
            data = json.loads(workspace_file.read_text())
        else:
            data = {}
            
        if 'settings' not in data:
            data['settings'] = {}

        data['settings']['git.enabled'] = value

        workspace_file.write_text(json.dumps(data, indent=4))
        print(f"Successfully set 'git.enabled': {value} in {workspace_file.name}")

    except Exception as e:
        try:
            # Ensure .vscode directory exists
            vscode_dir = vscode_settings.parent
            vscode_dir.mkdir(exist_ok=True, parents=True)
            
            # Try to read existing settings or create new ones
            try:
                if vscode_settings.exists():
                    data = json.loads(vscode_settings.read_text())
                else:
                    data = {}
            except json.JSONDecodeError:
                data = {}
                
            data['git.enabled'] = value
            
            vscode_settings.write_text(json.dumps(data, indent=4))
            print(f"Successfully set 'git.enabled': {value} in {vscode_settings.relative_to(current_dir)}")
        except Exception as e:
            print(f"An error occurred while updating VSCode settings: {e}")
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