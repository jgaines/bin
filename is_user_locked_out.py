"""
From Bard, this is a passable start to a script that can check if a user is locked out of Active Directory.

What it should do is be able to accept any of user:
    sAMAccountName - no space, @ or comma in it
    email address  - check for @ in it
    "first last"   - if there's a space in it but no comma
    "last, first"  - if there's a comma in it
and look a user up by that and determine their lockout status.  I'm not sure if we have lockoutDuration in our
data.  I don't see it in the normal ldapsearch output.
"""
import ldap

def is_locked_out(user_dn):
    """
    Determines if the user with the given DN is locked out.

    Args:
        user_dn (str): The DN of the user.

    Returns:
        bool: True if the user is locked out, False otherwise.
    """

    conn = ldap.initialize("ldap://localhost")
    conn.bind_anonymous()

    result = conn.search(user_dn, ldap.SCOPE_BASE, "(objectClass=user)")

    if not result:
        return False

    attrs = result[0][1]

    lockout_time = attrs.get("lockoutTime")
    lockout_duration = attrs.get("lockoutDuration")

    if lockout_time is None or lockout_duration is None:
        return False

    current_time = ldap.explode_dn(conn.whoami())[0][0]

    return lockout_time + lockout_duration < current_time


user_dn = "CN=user,DC=example,DC=com"

is_locked_out(user_dn)
