#!/usr/bin/env python3
"""
Encyption module
"""

import bcrypt


def hash_password(password):
    """
    function that expects one string argument name
    `password` and returns a salted, hashed password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
