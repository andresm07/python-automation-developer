"""
Authentication utilities for the Fake Enterprise API.

Supports two authentication mechanisms:

1. API Key authentication (Labs 1-2)
2. OAuth-style Client Credentials (Lab 3+)
"""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta

from ..response import Response


class AuthManager:
    """
    Simulates an OAuth2 authorization server.
    """

    CLIENTS = {  # noqa: RUF012
        "training-client": "training-secret",
    }

    TOKENS: dict[str, dict] = {}  # noqa: RUF012

    TOKEN_DURATION_MINUTES = 30

    @classmethod
    def authenticate(
        cls,
        client_id: str,
        client_secret: str,
    ) -> str | None:
        expected_secret = cls.CLIENTS.get(client_id)

        if expected_secret != client_secret:
            return None

        token = secrets.token_hex(32)

        cls.TOKENS[token] = {
            "client_id": client_id,
            "expires": datetime.now()
            + timedelta(minutes=cls.TOKEN_DURATION_MINUTES),
        }

        return token

    @classmethod
    def validate_token(
        cls,
        token: str | None,
    ) -> bool:
        if token is None:
            return False

        token_info = cls.TOKENS.get(token)

        if token_info is None:
            return False

        if datetime.now() > token_info["expires"]:
            del cls.TOKENS[token]

            return False

        return True


def check_authentication(config) -> Response | None:
    """
    Accept either:

    - Valid API Key
    - Valid Bearer Token

    Returns:
        None if authenticated.
        Response(401) otherwise.
    """

    # Legacy API Key authentication
    if config.client_api_key == config.expected_api_key:
        return None

    # OAuth-style token authentication
    if AuthManager.validate_token(config.access_token):
        return None

    return Response(
        status_code=401,
        error="Unauthorized",
    )
