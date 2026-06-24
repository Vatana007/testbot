import os
import sys
import unittest
from datetime import timedelta
from unittest.mock import patch

# Set up paths so we can import backend.auth
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

# Set mock env variables BEFORE importing auth to ensure they take effect
os.environ["ADMIN_USERNAME"] = "testadmin"
os.environ["ADMIN_PASSWORD"] = "testpass123"
os.environ["API_SECRET_KEY"] = "super-secret-key-for-unit-testing"

import backend.auth as auth
from jose import jwt
from fastapi import HTTPException


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.username = "testadmin"
        self.password = "testpass123"
        os.environ["ADMIN_USERNAME"] = self.username
        os.environ["ADMIN_PASSWORD"] = self.password
        os.environ["API_SECRET_KEY"] = "super-secret-key-for-unit-testing"

    def test_authenticate_user_success(self):
        """Test authentication with correct credentials."""
        # Whitespace handling is done in authenticate_user
        user = auth.authenticate_user(self.username, self.password)
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], self.username)
        self.assertEqual(user["role"], "admin")

    def test_authenticate_user_fail(self):
        """Test authentication failures with wrong credentials or unknown users."""
        self.assertIsNone(auth.authenticate_user(self.username, "wrongpass"))
        self.assertIsNone(auth.authenticate_user("unknownuser", self.password))

    def test_authenticate_user_stripping(self):
        """Test that authenticate_user strips leading and trailing whitespaces."""
        user = auth.authenticate_user(f"  {self.username}  ", f"  {self.password}  ")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], self.username)

    def test_create_access_token(self):
        """Verify that JWT tokens encode data correctly and hold expiration times."""
        payload = {"sub": "testuser", "role": "teacher"}
        token = auth.create_access_token(payload, expires_delta=timedelta(minutes=15))
        
        # Decode and verify token
        decoded = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        self.assertEqual(decoded["sub"], "testuser")
        self.assertEqual(decoded["role"], "teacher")
        self.assertIn("exp", decoded)

    def test_get_current_user_valid(self):
        """Test extraction of current user from a valid active JWT token."""
        payload = {"sub": "someuser", "role": "admin"}
        token = auth.create_access_token(payload)
        
        user_info = auth.get_current_user(token)
        self.assertEqual(user_info["username"], "someuser")
        self.assertEqual(user_info["role"], "admin")

    def test_get_current_user_invalid(self):
        """Test that get_current_user raises 401 Unauthorized for malformed/signature-invalid tokens."""
        with self.assertRaises(HTTPException) as ctx:
            auth.get_current_user("invalid.token.string")
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertEqual(ctx.exception.detail, "Could not validate credentials")

    def test_require_admin_role_enforcement(self):
        """Test admin role checks; allow admins but block others with 403 Forbidden."""
        admin_user = {"username": "admin_one", "role": "admin"}
        teacher_user = {"username": "teacher_one", "role": "teacher"}

        # Admin passes check
        self.assertEqual(auth.require_admin(admin_user), admin_user)

        # Teacher raises 403
        with self.assertRaises(HTTPException) as ctx:
            auth.require_admin(teacher_user)
        self.assertEqual(ctx.exception.status_code, 403)
        self.assertEqual(ctx.exception.detail, "Admin access required")


if __name__ == "__main__":
    unittest.main()
