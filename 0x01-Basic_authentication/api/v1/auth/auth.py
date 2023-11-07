#!/usr/bin/env python3
"""
Authentication module
"""

from flask import request
from typing import List, TypeVar
import fnmatch


class Auth():
    """
    manage the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        check string params if they need auth
        """
        if path is None or not excluded_paths:
            return True

        new_path = path.rstrip('/')
        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(new_path, excluded_path):
                return False
        return True

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
