from unittest.mock import patch
import os
import sys

MODULE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

import auth_check

def test_auth_check_decorator_authenticated():
    # Mock the session to simulate an authenticated user
    with patch('auth_check.session', {'user_id': 1}):
        @auth_check.auth_check
        def protected_route():
            return "Access granted"

        result = protected_route()
        assert result == "Access granted"


def test_auth_check_decorator_unauthenticated():
    # Mock the session to simulate an unauthenticated user
    with patch('auth_check.session', {}):
        @auth_check.auth_check
        def protected_route():
            return "Access granted"

        result = protected_route()
        assert result == ("Unauthorized", 401)