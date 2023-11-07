#!/usr/bin/env python3
"""
Basic Auth module
"""

from .auth import Auth
import base64


class BasicAuth(Auth):
    """
    Implementation of Basic Auth
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization header
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if 'Basic' not in authorization_header:
            return None
        return authorization_header[6:]