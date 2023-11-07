#!/usr/bin/env python3
"""
Authentication module
"""

from flask import request
from typing import List, TypeVar


class Auth():
    """
    manage the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        check string params if they need auth
        """
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True

        new_path = path.rstrip('/')
        if new_path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """
        Holds the header information
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Defines current user
        """
        return None
