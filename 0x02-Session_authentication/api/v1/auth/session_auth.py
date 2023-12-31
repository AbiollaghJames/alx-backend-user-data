#!/usr/bin/env python3
"""
Session Auth module
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User
from typing import Dict


class SessionAuth(Auth):
    """
    Session Authentication class
    """
    user_id_by_session_id: Dict[str, str] = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """
        returns a User instance based on a cookie value
        """
        cookie = self.session_cookie(request)
        session_user_id = self.user_id_for_session_id(cookie)
        u_id = User.get(session_user_id)
        return u_id

    def destroy_session(self, request=None):
        """
        deletes the user session / logout
        """
        cookie = self.session_cookie(request)

        if cookie is None:
            return False
        if not self.user_id_for_session_id(cookie):
            return False
        del self.user_id_by_session_id[cookie]
        return True
