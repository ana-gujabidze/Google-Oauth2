import pytest
from django.contrib.auth.models import Permission, User
from pytest_factoryboy import register
from rest_framework.test import APIClient


@pytest.fixture
def user():
    return User.objects.create_user(username="test_username", email="test@email.com")


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def add_permission():
    def f(user, permission):
        permission = Permission.objects.get(codename=permission)
        user.user_permissions.add(permission)

    return f
