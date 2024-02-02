import os

from auth import verify_admin

ADMIN_PW = os.environ["ADMIN_PW"]


def test_verify_admin_okay():
    """Test verifying the admin with correct pw"""

    assert verify_admin(ADMIN_PW)

def test_verify_admin_unauth():
    """Test verifying the admin with incorrect pw"""

    assert verify_admin("let me in") is False
