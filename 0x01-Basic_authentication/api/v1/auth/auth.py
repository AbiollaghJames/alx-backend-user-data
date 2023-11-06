#!/usr/bin/env python3

from flask import request
from typing import List, TypeVar


class Auth():
    """
    manage the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Just returns False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Just returns None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Defines current user
        """
        return None
