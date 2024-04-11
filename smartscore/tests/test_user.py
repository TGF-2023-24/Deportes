import pytest 

from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create(
        username="testuser",
        password="testpassword",
        email="prueba@gmail.com"
        )
    assert User.objects.count() == 1
    assert user.__str__() == "testuser"

