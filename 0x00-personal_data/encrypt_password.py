#!/usr/bin/env python3
"""Password encryption module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: A salted, hashed password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates whether the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
