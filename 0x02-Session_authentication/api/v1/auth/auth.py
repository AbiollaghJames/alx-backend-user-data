#!/usr/bin/env python3
"""
Authentication module
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    manage the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        check string params if they need auth
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        path = path.rstrip("/")
        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and path.startswith(excluded_path[:-1]):
                return False
            elif path == excluded_path.rstrip("/"):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Holds the header information
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Defines current user
        """
        return None
