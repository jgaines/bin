# Security Considerations for ~/bin Scripts

This document outlines security considerations for the scripts in this repository.

## Credential Files

Several scripts in this repository reference external credential files:

- `~/.ssh/ldap_bind_password` - Used by samaccountname script
- `~/.ssh/bad` - Used by membersof script
- `~/.ssh/bb-prod-token` - Used by engt-permissions.sh script
- `~/.keys/.vaultpw.txt` - Used by swarm script

### Security Recommendations

1. **Ensure proper file permissions**: All credential files should have 600 permissions (readable only by owner)
   ```bash
   chmod 600 ~/.ssh/ldap_bind_password ~/.ssh/bad ~/.ssh/bb-prod-token ~/.keys/.vaultpw.txt
   ```

2. **Regular credential rotation**: Consider regularly rotating credentials stored in these files

3. **Secure storage**: Keep credential files outside of any Git repositories

4. **Consider using a password manager**: For more secure credential management

## Script Improvements

Scripts have been improved with:

- Credential file existence checks
- Permission validation for credential files
- Input sanitization for user-provided arguments
- Error handling for failed operations
- Logging of connection attempts (without sensitive data)

## Internal Identifiers

Be aware that some scripts contain internal identifiers:
- Hostnames and server URLs
- Service account names
- LDAP paths and configurations

These might be considered sensitive information depending on your organization's security policies.

## Additional Security Measures

- Consider encrypting credential files when not in use
- Use locked-down permissions for all scripts (chmod 700)
- Regularly audit script contents before sharing
- Consider switching to a more secure authentication method (like SSH keys) where possible
