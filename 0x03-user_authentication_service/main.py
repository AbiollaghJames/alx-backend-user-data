#!/usr/bin/env python3
"""Main file module
"""

import requests
from auth import Auth

AUTH = Auth()


def register_user(email: str, password: str) -> None:
    """Tests register_user
    """
    data = {'email': email, 'password': password}
    response = requests.post('http://127.0.0.1:5000/users', data=data)
    assert response.status_code == 200
    assert response.json() == {'email': email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests log in wrong password
    """
    data = {'email': email, 'password': password}
    response = requests.post('http://127.0.0.1:5000/sessions', data=data)
    assert response.status_code == 401, f"status code:{response.status_code}"


def log_in(email: str, password: str) -> str:
    """Tests login
    """
    data = {'email': email, 'password': password}
    response = requests.post('http://127.0.0.1:5000/sessions', data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}


def profile_unlogged() -> None:
    """Tests profile unlogged
    """
    response = requests.get('http://127.0.0.1:5000/profile')
    assert response.status_code == 403, f"status code: {response.status_code}"


def profile_logged(session_id: str) -> None:
    """Tests profile logged
    """
    data = {'session_id': session_id}
    response = requests.post('http://127.0.0.1:5000/profile', data=data)
    user = AUTH.get_user_from_session_id(session_id)
    assert response.status_code == 200
    assert response.json() == {"email": user.email}


def log_out(session_id: str) -> None:
    """Tests logging out
    """
    data = {'session_id': session_id}
    response = requests.delete('http://127.0.0.1:5000/sessions', data=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Tests reset password method
    """
    data = {'email': email}
    response = requests.post('http://127.0.0.1:5000/reset_password', data=data)
    user = AUTH._db.find_user_by(email=email)
    assert response.status_code == 200
    assert response.json() == {'email': email, "reset_token": user.reset_token}


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests update password
    """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = request.put('http://127.0.0.1:5000/reset_password', data=data)
    assert response.status_code == 200
    assert response.json() == {'email': email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
