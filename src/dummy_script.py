import re

# Test commit
def validate_email(email: str) -> bool:
    """
    Validates an email address format.

    This function checks if the provided string matches a standard email format:
    - Contains local part and domain part separated by @
    - Local part can contain letters, numbers, dots, hyphens, and underscores
    - Domain part must contain at least one dot and valid TLD

    Args:
        email: String to validate as email address

    Returns:
        True if email format is valid, False otherwise

    Examples:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid.email")
        False
        >>> validate_email("test.user@domain.co.uk")
        True
    """
    if not isinstance(email, str):
        return False

    if not email or len(email) > 254:  # RFC 5321 limit
        return False

    # Basic email regex pattern
    pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(pattern, email):
        return False

    # Additional checks
    local_part, domain_part = email.split("@", 1)

    # Local part validation
    if len(local_part) > 64:  # RFC 5321 limit
        return False
    if local_part.startswith(".") or local_part.endswith("."):
        return False
    if ".." in local_part:
        return False

    # Domain part validation
    if len(domain_part) > 253:  # RFC 5321 limit
        return False
    if domain_part.startswith(".") or domain_part.endswith("."):
        return False
    if ".." in domain_part:
        return False

    # Check TLD (top-level domain)
    parts = domain_part.split(".")
    if len(parts) < 2:
        return False
    # TLD must be at least 2 characters
    return len(parts[-1]) >= 2
