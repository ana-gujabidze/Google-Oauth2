from typing import Tuple

from django.contrib.auth.models import User

from .google_provider import GoogleProvider
from .models import Profile


def authenticate_user(code: str, redirect_uri: str) -> User:
    google_provider = GoogleProvider
    access_token, id_token = google_provider.google_get_token(code=code, redirect_uri=redirect_uri)
    # validate ID token
    # google_provider.google_validate_id_token(id_token=id_token)
    user_profile = google_provider.google_get_user_profile(access_token=access_token)
    user_ext_id = user_profile['ext_id']

    try:
        profile = Profile.objects.get(ext_id=user_ext_id)
        user = profile.user
    except Profile.DoesNotExist:
        # Create User object
        user = User.objects.create(
            username=user_profile['username'],
            email=user_profile['email'],
            first_name=user_profile['first_name'],
            last_name=user_profile['last_name']
        )
        user.save()
        # Create Profile object
        profile = Profile(
            user=user,
            ext_id=user_ext_id
        )
        profile.save()
    return user
