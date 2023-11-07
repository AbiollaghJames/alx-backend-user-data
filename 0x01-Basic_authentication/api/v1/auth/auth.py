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
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False

    def authorization_header(self, request=None) -> str:
        """
        Holds the header information
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Defines current user
        """
        return None
