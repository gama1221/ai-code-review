# Write your corrected implementation for Task 2 here.
# Do not modify `task2.py`.

from pickle import FALSE
import re
from typing import List, Optional, Union
import warnings

def count_valid_emails(
    emails: Union[List[str], List[Optional[str]]],
    *,
    require_tld: bool = True,
    allow_plus_addressing: bool = True,
    allow_ip_domains: bool = False,
    allow_unicode: bool = False
) -> int:
    """
    Count the number of valid email addresses in a list.
    
    Uses RFC 5322 compliant regex with configurable validation options.
    
    Args:
        emails: List of email addresses to validate
        require_tld: If True, requires domain to have a top-level domain (e.g., .com)
        allow_plus_addressing: If True, allows plus addressing (user+tag@domain.com)
        allow_ip_domains: If True, allows IP address domains (user@[192.168.1.1])
        allow_unicode: If True, allows Unicode characters in email addresses
        
    Returns:
        int: Number of valid email addresses in the input list
        
    Raises:
        TypeError: If emails is not a list
        ValueError: If emails contains non-string elements (excluding None)
    """
    # Input validation
    if not isinstance(emails, list):
        raise TypeError(f"Expected list, got {type(emails).__name__}")
    
    # Build appropriate regex pattern based on configuration
    local_part_pattern = r"[a-zA-Z0-9!#$%&.'*+/=?^_`{|}~-]+"
    
    if allow_plus_addressing:
        local_part_pattern = r"[a-zA-Z0-9!#$%&.'*+/=?^_`{|}~-]+(?:\+[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)?"
    
    if allow_unicode:
        local_part_pattern = r"[a-zA-Z0-9\u0080-\uFFFF!#$%&'*+/=?^_`{|}~-]+"
        if allow_plus_addressing:
            local_part_pattern = r"[a-zA-Z0-9\u0080-\uFFFF!#$%&'*+/=?^_`{|}~-]+(?:\+[a-zA-Z0-9\u0080-\uFFFF!#$%&'*+/=?^_`{|}~-]+)?"
    
    domain_part_pattern = r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+"
    
    if allow_ip_domains:
        domain_part_pattern = f"(?:{domain_part_pattern}|\\[[0-9]{1,3}(?:\\.[0-9]{1,3}){{3}}\\])"
    
    if not require_tld:
        domain_part_pattern = r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"
    
    # Compile regex pattern for performance
    email_pattern = re.compile(
        rf"^{local_part_pattern}@{domain_part_pattern}$",
        re.IGNORECASE | (re.UNICODE if allow_unicode else 0)
    )
    
    valid_count = 0
    
    for i, email in enumerate(emails):
        # Skip None values silently (treat as invalid)
        if email is None:
            warnings.warn(
                f"None value found at index {i}, treating as invalid email",
                UserWarning,
                stacklevel=2
            )
            continue
        
        # Validate element type
        if not isinstance(email, str):
            raise ValueError(
                f"Element at index {i} must be string, got {type(email).__name__}"
            )
        
        # Skip empty strings
        if not email.strip():
            continue
        
        # Check email length limits (RFC 5321)
        if len(email) > 254:  # RFC maximum total length
            continue
        
        # Split for local part length check (RFC 5321)
        parts = email.split('@', 1)
        if len(parts) != 2:
            continue
        
        local_part = parts[0]
        if len(local_part) > 64:  # RFC maximum local part length
            continue
        
        # Apply regex validation
        if email_pattern.match(email):
            valid_count += 1
            print(f"valid email {email}")
        else:
            # Optional: Log detailed validation failures for debugging
            pass
    
    return valid_count


# Try with this values

# 10 sample email inputs (valid + invalid edge cases)
# emails = [
#     "john.doe@example.com",          # valid
#     "user+tag@gmail.com",             # valid (plus addressing)
#     "admin@mail.co.uk",               # valid
#     "invalid-email",                  # invalid
#     "missing@domain",                 # invalid (no TLD)
#     "missing-at-symbol.com",          # invalid
#     "user@[192.168.1.1]",             # invalid by default (IP domain not allowed)
#     "",                               # invalid (empty)
#     None,                             # invalid (None)
#     "verylonglocalpart" * 10 + "@example.com"  # invalid (local part too long)
# ]

# result = count_valid_emails(
#     emails,
#     require_tld=True,
#     allow_plus_addressing=True,
#     allow_ip_domains=False,
#     allow_unicode=False
# )

# print("Total emails:", len(emails))
# print("Valid emails:", result)
