import pytest
from django.contrib.auth.models import User

GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
LOGIN_ENDPOINT = "/api/auth/login/"
REFRESH_ENDPOINT = "/api/auth/refresh/"


def test_invalid_token(client):

    payload = {"refresh_token": "dummy_token"}

    response = client.post(REFRESH_ENDPOINT, payload, format="json")
    error_message = {"error": {"code": "invalid_request", "message": "Token is invalid or expired"}}

@pytest.mark.django_db
def test_successful_token_refresh(requests_mock, client):
    """
    Test when /api/auth/login/ returns valid token,
    tokens can be refreshed.
    """
    
    requests_mock.post(
        GOOGLE_ACCESS_TOKEN_OBTAIN_URL,
        json={
            "access_token": "test_access_token",
            "id_token": "test_id_token"
        },
        status_code=200
    )

    requests_mock.get(
        GOOGLE_USER_INFO_URL,
        json={
            'sub': '116904257072438399006',
            'email': "test@email.com",
            'givenName': "test_fname",
            'familyName': "test_lname",
            'name': "test_username"
        },
        status_code=200
    )

    payload = {
        "code": "test_code",
        "redirect_uri": "test_redirect_uri"
    }

    login_response = client.post(LOGIN_ENDPOINT, data=payload, format="json")

    refresh_response = client.post(REFRESH_ENDPOINT, data={"refresh_token": login_response.data["refresh_token"]}, format="json")
    
    user = User.objects.get(username="test_username")

    expected_response = {'id': 1, 'username': 'test_username', 'email': 'test@email.com', 'first_name': 'test_fname', 'last_name': 'test_lname'}

    profile_params = {'id': user.id, 'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}

    assert refresh_response.status_code == 200
    assert refresh_response.data["user"] == expected_response
    assert "access_token" in refresh_response.data
    assert "refresh_token" in refresh_response.data
    assert profile_params == refresh_response.data["user"]

    assert login_response.data["access_token"] == login_response.data["access_token"]
    assert login_response.data["refresh_token"] == login_response.data["refresh_token"]
