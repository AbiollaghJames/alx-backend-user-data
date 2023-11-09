#!/usr/bin/env python3
"""
SessionExpAuth module
"""
from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Adds expiraion date to sessionID
    """
    def __init__(self):
        """constructor"""
        try:
            session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """
        Creates a session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {'user_id': user_id, 'created_at': datetime.now()}
        SessionAuth.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        user ID for session ID
        """
        if session_id is None:
            return None
        if session_id not in SessionAuth.user_id_by_session_id.keys():
            return None
        session_dict = SessionAuth.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict["user_id"]
        if "created_at" not in session_dict.keys():
            return None
        create_time = session_dict["created_at"]
        time_delta = timedelta(seconds=self.session_duration)
        if (create_time + time_delta) < datetime.now():
            return None
        return session_dict["user_id"]
