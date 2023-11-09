#!/usr/bin/env python3
"""
Flask view that handles all routes
for the Session authentication
"""
from flask import jsonify, request
from werkzeug import exceptions
from api.v1.views import app_views
from models.user import User
from os import abort, environ, getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """
    logs user to a session
    """
    u_email = request.form.get('email', None)
    u_password = request.form.get('password', None)

    if u_email is None or u_email == "":
        return jsonify({"error": "email missing"}), 400
    if u_password is None or u_password == "":
        return jsonify({"error": "password missing"}), 400

    valid_user = User.search({'email': u_email})

    if not valid_user:
        return jsonify({"error": "no user found for this email"}), 404

    valid_user = valid_user[0]

    if not valid_user.is_valid_password(u_password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(valid_user.id)
    cookie = getenv('SESSION_NAME')
    user_dict = jsonify(valid_user.to_json())

    user_dict.set_cookie(cookie, session_id)
    return user_dict


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False
)
def logout() -> str:
    """Logs out user
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
