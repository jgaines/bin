# Machine-Specific Script Validation Requirements

## Overview

This document defines requirements for a script validation system that ensures
certain scripts only run on certain machines or provides appropriate
warnings/confirmations when run elsewhere.  NOTE: This is not about security, it
is simply that some scripts will only work from certain machines.

## Background

The ~/bin repository is synchronized across multiple machines:

- **Primary work machine** (main development/work environment)
- **Home machine** (personal use)
- **john.eng.netscout.com** (Linux server for testing/Docker applications)

Some scripts contain work-specific configurations, access credentials, or
perform operations that should only occur on the primary work machine.  Some are
only appropriate on my home machine.

## Requirements

### Functional Requirements

#### FR-1: Machine Identification

- The system SHALL identify the current machine reliably
- Machine identification SHOULD use multiple factors:
  - Hostname
  - Network environment (IP ranges, domain)
  - User context
  - File system markers (specific directories/files that exist only on certain
    machines)

#### FR-2: Script Protection Modes

The system SHALL support multiple protection modes:

##### Mode 1: Hard Block

- Script exits immediately with error message
- No user override option
- For scripts with sensitive operations or credentials

##### Mode 2: Confirmation Required

- Script displays warning about running on non-primary machine
- Prompts user for confirmation (Y/N)
- Continues only with explicit user consent
- For scripts that could work but aren't recommended

##### Mode 3: Warning Only

- Displays informational message
- Continues execution automatically
- For scripts with minor compatibility concerns

#### FR-3: Integration Interface

- The validation system SHALL be easily callable from other scripts
- SHOULD support both sourcing (for exit behavior) and command execution
- MUST return appropriate exit codes for automated use

#### FR-4: Configuration Management

- Machine definitions SHOULD be configurable
- Protection rules SHOULD be definable per script or script category
- Configuration SHOULD be maintainable without modifying the core validation
  script

### Non-Functional Requirements

#### NFR-1: Performance

- Machine detection MUST complete within 100ms
- SHOULD cache detection results for repeated calls within the same session

#### NFR-2: Reliability

- MUST fail safely (default to most restrictive mode on detection failure)
- SHOULD handle network timeouts gracefully
- MUST not depend on external network services for basic functionality

#### NFR-3: Usability

- Error messages MUST clearly explain why the script cannot run
- Warning messages SHOULD provide context about potential issues
- Prompts MUST be clear and unambiguous

#### NFR-4: Maintainability

- Code SHOULD be well-documented
- Machine detection logic SHOULD be modular
- SHOULD follow established shell scripting best practices

## Use Cases

### UC-1: Work-Specific Script on Home Machine

```text
Given: User runs a work-specific script on home machine
When: Script calls validation with "hard-block" mode
Then: Script exits with message explaining it's work-only
```

### UC-2: General Script with Confirmation

```text
Given: User runs a script with confirmation mode on non-primary machine
When: Script calls validation with "confirm" mode
Then: User sees warning and Y/N prompt
And: Script continues only if user confirms
```

### UC-3: Automated Script Usage

```text
Given: Script is called from automation/cron
When: Running on non-primary machine with confirmation mode
Then: Script exits without prompting (non-interactive context)
And: Returns appropriate exit code for automation handling
```

## Implementation Considerations

### Machine Detection Strategy

1. **Primary Method**: Hostname pattern matching
2. **Secondary**: Network-based detection (domain, IP ranges)
3. **Tertiary**: File system markers (e.g., presence of work-specific
   directories)
4. **Fallback**: Environment variables or configuration files

### Integration Examples

```bash
#!/bin/bash
# Example usage in a script

# Source the validator for exit behavior
source "$(dirname "$0")/lib/machine-validator.sh"
validate_machine "hard-block" "This script contains work credentials"

# Or call as command for return code handling
if ! machine-validator check --mode=confirm --reason="May not work correctly"; then
    echo "User declined to continue"
    exit 1
fi
```

### Configuration Structure

```bash
# machine-config.conf
PRIMARY_HOSTNAMES=("work-laptop" "jgaines-dev")
HOME_HOSTNAMES=("home-desktop" "personal-laptop")
SERVER_HOSTNAMES=("john.eng.netscout.com")

WORK_DOMAINS=("netscout.com" "corp.local")
HOME_NETWORKS=("192.168.1.0/24" "10.0.0.0/8")
```

## Success Criteria

- Scripts can be easily protected with a single function call
- False positives/negatives in machine detection are minimized
- User experience is clear and not overly intrusive
- System is maintainable as machine configurations change
- Integration doesn't significantly impact script startup time

## Future Enhancements

- Integration with SSH key presence for additional validation
- Logging of script execution attempts across machines
- Central configuration management for enterprise environments
- Integration with version control hooks for automatic protection tagging
