from flask import session
from dash.exceptions import PreventUpdate

# utils for auth to be used 
def get_session_user_id():
    return session.get('user_id', None)


def get_session_access_type():
    return session.get('access_type', None)


def require_auth():
    user_id = get_session_user_id()
    if user_id is None:
        raise PreventUpdate
    return user_id


def require_role(min_access_type):
    user_id = require_auth()
    access_type = get_session_access_type()
    if access_type is None or access_type < min_access_type:
        raise PreventUpdate
    return user_id, access_type


def verify_user_owns_data(target_user_id):
    user_id = require_auth()
    if user_id != target_user_id:
        raise PreventUpdate
    return user_id
