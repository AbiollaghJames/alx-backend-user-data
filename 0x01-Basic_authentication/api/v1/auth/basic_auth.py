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
    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        returns the Base64 part of the Authorization header
        """
        if authorization_header is None or not isinstance(
            authorization_header, str
        ):
            return None
        if 'Basic' not in authorization_header:
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None
        try:
            decoded_byte = base64.b64decode(base64_authorization_header)
            decoded_text = decoded_byte.decode('utf-8')
        except Exception:
            return None
        return decoded_text

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        returns the user email and password
        from the Base64 decoded value.
        """
        if decode_base64_authorization_header is None or not isinstance(
            decoded_base64_authorization_header, str
        ):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        u_name, passwd = decoded_base64_authorization_header.split(':', 1)
        return (u_name, passwd)