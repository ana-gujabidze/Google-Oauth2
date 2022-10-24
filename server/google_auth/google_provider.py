from typing import Any, Dict, Tuple

import requests
from django.conf import settings
from django.core.exceptions import ValidationError


class GoogleProvider:
    """
    Get access and refresh tokens from Google OAuth2 using Google
    code and redirect_uri provided by client.
    """

    GOOGLE_ID_TOKEN_INFO_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    @classmethod
    def google_get_token(cls, code: str, redirect_uri: str) -> Tuple[str, str]:
        url = cls.GOOGLE_ACCESS_TOKEN_OBTAIN_URL
        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        response = requests.post(url, data=data)

        if not response.ok:
            raise ValidationError("Failed to obtain access token from Google.")

        payload = response.json()

        return (payload["access_token"], payload["id_token"])

    @classmethod
    def google_get_user_profile(cls, access_token: str) -> Dict[str, Any]:
        response = requests.get(cls.GOOGLE_USER_INFO_URL, params={"access_token": access_token})

        if not response.ok:
            raise ValidationError("Failed to obtain user profile from Google.")

        payload = response.json()

        user_profile = {
            "ext_id": payload.get("sub"),
            "email": payload.get("email", ""),
            "first_name": payload.get("givenName", ""),
            "last_name": payload.get("familyName", ""),
            "username": payload.get("name", ""),
        }

        return user_profile

    def google_validate_id_token(cls, id_token: str) -> bool:
        response = requests.get(cls.GOOGLE_ID_TOKEN_INFO_URL, params={"id_token": id_token})

        if not response.ok:
            raise ValidationError("ID token is invalid.")

        audience = response.json()["aud"]

        if audience != settings.GOOGLE_OAUTH2_CLIENT_ID:
            raise ValidationError("Invalid audience.")

        return True
