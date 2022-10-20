import pytest
from django.contrib.auth.models import User

PROFILE_ENDPOINT = "/api/auth/me/"


@pytest.mark.django_db
def test_successful_authentication(auth_client):
    """
    Test when test user can successfully login
    and profile information can be retrieved.
    """
    
    response = auth_client.get(PROFILE_ENDPOINT, format="json")
    
    expected_response = {'id': 1, 'username': 'test_username', 'email': 'test@email.com', 'first_name': '', 'last_name': ''}

    assert response.status_code == 200
    assert response.data == expected_response
