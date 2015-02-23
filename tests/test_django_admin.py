# -- encoding: UTF-8 --

import uuid

try:
    from django.contrib.auth import get_user_model
except ImportError:  # `get_user_model` only exists from Django 1.5 on.
    from django.contrib.auth.models import User
    get_user_model = lambda: User

from django.core.urlresolvers import reverse
from django.test import Client
import pytest
from enumfields import EnumIntegerField
from .models import MyModel


@pytest.fixture
def client():
    return Client()


SUPERUSER_USERNAME = "superuser"
SUPERUSER_PASS = "superpass"


@pytest.fixture
def superuser():
    return get_user_model().objects.create_superuser(username=SUPERUSER_USERNAME, password=SUPERUSER_PASS,
                                                     email="billgates@microsoft.com")


@pytest.fixture
def superuser_client(client, superuser):
    client.login(username=SUPERUSER_USERNAME, password=SUPERUSER_PASS)
    return client


@pytest.mark.django_db
@pytest.mark.urls('tests.urls')
def test_model_admin(superuser_client):
    url = reverse("admin:tests_mymodel_add")
    secret_uuid = str(uuid.uuid4())
    post_data = {
        'color': MyModel.Color.RED.value,
        'taste': MyModel.Taste.UMAMI.value,
        'taste_int': MyModel.Taste.SWEET.value,
        'random_code': secret_uuid
    }
    response = superuser_client.post(url, follow=True, data=post_data)
    response.render()
    text = response.content

    assert b"This field is required" not in text
    assert b"Select a valid choice" not in text
    try:
        inst = MyModel.objects.get(random_code=secret_uuid)
    except MyModel.DoesNotExist:
        assert False, "Object wasn't created in the database"
    assert inst.color == MyModel.Color.RED, "Redness not assured"
    assert inst.taste == MyModel.Taste.UMAMI, "Umami not there"
    assert inst.taste_int == MyModel.Taste.SWEET, "Not sweet enough"


def test_django_admin_lookup_value_for_integer_enum_field():
    field = EnumIntegerField(MyModel.Taste)

    assert field.get_prep_value(str(MyModel.Taste.BITTER)) == 3, "get_prep_value should be able to convert from strings"
