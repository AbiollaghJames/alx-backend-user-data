#!/usr/bin/env python3
"""
Encyption module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    function that expects one string argument name
    `password` and returns a salted, hashed password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validate that the provided
    password matches the hashed password
    """
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True
    return False
