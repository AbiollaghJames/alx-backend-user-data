#!/usr/bin/env python3
"""
Session DB module
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAut):
    """
    session DB class
    """
    def create_session(self, user_id=None):
        """
        stores new instance of UserSession and return
        session ID
        """
        session_id = super().create_session(user_id)
        if user_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ gets user_id from session_id """
        if session_id is None:
            return None
        UserSession.load_from_file()
        valid_user = UserSession.search({'session_id': session_id})
        if not valid_user:
            return None
        valid_user = valid_user[0]
        start_time = valid_user.created_at
        time_delta = timedelta(seconds=self.session_duration)
        if (start_time + time_delta) < datetime.now():
            return None
        return valid_user.user_id

    def destroy_session(self, request=None):
        """ Destroy usersession from session id  """
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        if not self.user_id_for_session_id(cookie):
            return False
        user_session = UserSession.search({'session_id': cookie})
        if not user_session:
            return False
        user_session = user_session[0]
        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
