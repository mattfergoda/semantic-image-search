import os

from dotenv import load_dotenv

load_dotenv()

ADMIN_PW = os.environ["ADMIN_PW"]


def verify_admin(pw):
    """Verify that the incoming password is the admin password."""

    return pw == ADMIN_PW


