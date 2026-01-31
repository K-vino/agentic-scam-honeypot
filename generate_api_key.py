#!/usr/bin/env python3
"""Generate a secure random API key for the hackathon backend API."""

import secrets
import string


def generate_api_key(length: int = 36) -> str:
    """
    Generate a secure random API key.
    
    Args:
        length: Length of the API key (32-40 recommended)
    
    Returns:
        A secure random string containing only lowercase letters and numbers
    """
    # Use only lowercase letters and numbers
    alphabet = string.ascii_lowercase + string.digits
    # Use secrets.choice for cryptographically strong random selection
    return ''.join(secrets.choice(alphabet) for _ in range(length))


if __name__ == "__main__":
    # Generate a 36-character API key (within 32-40 range)
    api_key = generate_api_key(36)
    
    print(api_key)
    print()
    print("# .env file")
    print(f"API_KEY={api_key}")
    print()
    print("# HTTP request header")
    print(f"X-API-Key: {api_key}")
