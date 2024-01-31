import os

from passlib.context import CryptContext

ADMIN_PW = os.environ.get("ADMIN_PW")

pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_admin(hashed_password):
    """Verify that the plain password hashes to the correct admin password."""

    return pw_context.verify(ADMIN_PW, hashed_password)

