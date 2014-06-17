import uuid

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import connection
from django.test import Client
import pytest

from enumfields import Enum
from .models import MyModel


def test_choices():
    class Color(Enum):
        __order__ = 'RED GREEN BLUE'

        RED = 'r'
        GREEN = 'g'
        BLUE = 'b'

    COLOR_CHOICES = (
        ('r', 'Red'),
        ('g', 'Green'),
        ('b', 'Blue'),
    )
    assert Color.choices() == COLOR_CHOICES


def test_labels():
    class Color(Enum):
        RED = 'r'
        GREEN = 'g'

        class Labels:
            RED = 'A custom label'

    assert Color.RED.label == 'A custom label'
    assert Color.GREEN.label == 'Green'


@pytest.mark.django_db
def test_field_value():
    m = MyModel(color=MyModel.Color.RED)
    m.save()
    assert m.color == MyModel.Color.RED

    m = MyModel.objects.filter(color=MyModel.Color.RED)[0]
    assert m.color == MyModel.Color.RED


@pytest.mark.django_db
def test_db_value():
    m = MyModel(color=MyModel.Color.RED)
    m.save()
    cursor = connection.cursor()
    cursor.execute('SELECT color FROM %s WHERE id = %%s' % MyModel._meta.db_table, [m.pk])
    assert cursor.fetchone()[0] == MyModel.Color.RED.value


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

    response = superuser_client.post(url, follow=True, data={
        'color': MyModel.Color.RED.value,
        'taste': MyModel.Taste.UMAMI.value,
        'taste_int': MyModel.Taste.SWEET.value,
        'random_code': secret_uuid
    })
    response.render()
    text = response.content

    assert "This field is required" not in text
    assert "Select a valid choice" not in text
    assert MyModel.objects.filter(random_code=secret_uuid).exists(), "Object wasn't created in the database"



