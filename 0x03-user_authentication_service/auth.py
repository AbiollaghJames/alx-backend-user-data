#!/usr/bin/env python3
"""
Hash Password module
"""
import bcrypt
import uuid
from db import DB
from user import User
from typing import Union
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    takes in a password string arguments
    and returns bytes
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generates a users uuid
    """
    new_uuid = str(uuid.uuid4())
    return new_uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register user if doesn't exist
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Checks password match
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_psswd = user.hashed_password
            passwd = password.encode('utf-8')
            return bcrypt.checkpw(passwd, hashed_psswd)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[None, str]:
        """Creates session and return uuid as str
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = str(_generate_uuid())
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(session_id: str) -> str:
        """Returns user from session_id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(user_id: int) -> None:
        """Destroy session by updating session_id to None
        """
        pass
